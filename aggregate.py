#!/usr/bin/env python3
"""Aggregate public disposable/temporary email-domain blocklists into one list.

Stdlib only. Reads sources.txt, fetches each source, parses + normalizes the
domains, unions/dedupes/sorts them, and writes domains.txt, domains.json and
metadata.json. A source that fails to fetch is skipped with a warning; the run
aborts (writing nothing) only if MORE than half the sources fail, so a bad
fetch day can never truncate the published list.

Run: python3 aggregate.py
"""
import json
import re
import sys
import urllib.request
import urllib.error

SOURCES_FILE = "sources.txt"
TIMEOUT = 45  # seconds per source
UA = "disposable-email-domains-aggregator (+https://github.com/mehrtat/disposable-email-domain)"

# A domain: 2+ dot-separated labels, letters/digits/hyphen (underscore tolerated),
# labels 1-63 chars not starting/ending with a hyphen, TLD starting with a letter
# (covers punycode xn-- TLDs). Anchored, already-lowercased ASCII input.
_LABEL = r"[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?"
_DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?:%s\.)+[a-z][a-z0-9-]{1,}$" % _LABEL)


def read_sources(path):
    urls = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


def fetch(url):
    """Return decoded body text, or raise on network/HTTP error."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def raw_tokens(body):
    """Yield raw domain-ish tokens from a body that is either newline text or a
    JSON array of strings."""
    stripped = body.lstrip()
    if stripped.startswith("[") or stripped.startswith("{"):
        try:
            data = json.loads(body)
            if isinstance(data, dict):
                data = data.get("domains") or data.get("data") or []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        yield item
                return
        except (ValueError, TypeError):
            pass  # fall through to line parsing
    for line in body.splitlines():
        yield line


def normalize(token):
    """Normalize one token to a canonical ASCII domain, or None to drop it."""
    d = token.strip().strip('",').strip()  # trim whitespace + JSON residue
    if not d or d.startswith("#"):
        return None
    d = d.lower()
    if d.startswith("@"):
        d = d[1:]
    if d.startswith("*."):
        d = d[2:]
    d = d.strip(".")
    if not d or "/" in d or "@" in d or " " in d or "\t" in d:
        return None
    if "." not in d:
        return None
    if not d.isascii():
        try:
            d = d.encode("idna").decode("ascii")
        except (UnicodeError, ValueError):
            return None
    if not _DOMAIN_RE.match(d):
        return None
    return d


def main():
    urls = read_sources(SOURCES_FILE)
    if not urls:
        sys.exit("no sources in %s" % SOURCES_FILE)

    domains = set()
    per_source = []
    failures = 0
    for url in urls:
        try:
            body = fetch(url)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as exc:
            failures += 1
            print("WARN: skipping %s: %s" % (url, exc), file=sys.stderr)
            continue
        found = {n for n in (normalize(t) for t in raw_tokens(body)) if n}
        per_source.append({"url": url, "count": len(found)})
        domains |= found
        print("  %6d domains  <- %s" % (len(found), url), file=sys.stderr)

    if failures > len(urls) // 2:
        sys.exit(
            "ABORT: %d/%d sources failed (>half); refusing to write a truncated list"
            % (failures, len(urls))
        )

    ordered = sorted(domains)
    with open("domains.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(ordered) + "\n")
    with open("domains.json", "w", encoding="utf-8") as fh:
        json.dump(ordered, fh, indent=0)
        fh.write("\n")
    with open("metadata.json", "w", encoding="utf-8") as fh:
        json.dump(
            {"count": len(ordered), "sources": per_source, "generated_by": "github-action"},
            fh,
            indent=2,
        )
        fh.write("\n")

    print("%d unique domains from %d/%d sources" % (len(ordered), len(per_source), len(urls)))


if __name__ == "__main__":
    main()
