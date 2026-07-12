# disposable-email-domain

[![domains](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmehrtat%2Fdisposable-email-domain%2Fmain%2Fmetadata.json&query=%24.count&label=domains&color=blue)](https://raw.githubusercontent.com/mehrtat/disposable-email-domain/main/domains.txt)
[![latest release](https://img.shields.io/github/v/release/mehrtat/disposable-email-domain?label=version)](https://github.com/mehrtat/disposable-email-domain/releases/latest)
[![last updated](https://img.shields.io/github/release-date/mehrtat/disposable-email-domain?label=updated)](https://github.com/mehrtat/disposable-email-domain/releases/latest)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A single, clean list of **disposable / temporary / throwaway email domains**,
aggregated from the best maintained public blocklists, then **deduplicated,
normalized, and sorted**. It **auto-refreshes daily** via GitHub Actions — a new
version is released only on the days the list actually changes.

> **Live count: ~162,000 domains** (the badge above is exact and always current).

## Use it

The canonical artifact is a plain newline-delimited list at a stable raw URL:

```
https://raw.githubusercontent.com/mehrtat/disposable-email-domain/main/domains.txt
```

There is also `domains.json` (a JSON array) and `metadata.json` (`count` +
per-source counts) at the same location.

```bash
# fetch the list
curl -sSL https://raw.githubusercontent.com/mehrtat/disposable-email-domain/main/domains.txt -o domains.txt

# is a domain disposable? (exit 0 = yes)
grep -Fxq "mailinator.com" domains.txt && echo "disposable"
```

### Install as a package

Every release ships the same list embedded in native packages so you don't have
to fetch anything at runtime.

**TypeScript / JavaScript (npm)**

```bash
npm install disposable-email-domain
```

```ts
import { isDisposable, domains } from "disposable-email-domain";

isDisposable("foo@mailinator.com"); // true
isDisposable("foo@gmail.com");      // false
domains.length;                     // ~162000
```

**Go**

```bash
go get github.com/mehrtat/disposable-email-domain@latest
```

```go
import disposable "github.com/mehrtat/disposable-email-domain"

disposable.IsDisposable("foo@mailinator.com") // true
_ = disposable.Domains                        // []string
```

**.NET (NuGet)**

```bash
dotnet add package DisposableEmailDomain
```

```csharp
using DisposableEmail;

DisposableEmailDomains.IsDisposable("foo@mailinator.com"); // true
var all = DisposableEmailDomains.Domains;                  // IReadOnlyList<string>
```

`isDisposable` / `IsDisposable` accept either a full address or a bare domain and
match case-insensitively.

## How it's built

`aggregate.py` (Python standard library only — no dependencies) fetches every
source in [`sources.txt`](sources.txt) and:

- strips whitespace, drops blank and `#` comment lines,
- lowercases, strips a leading `@` or `*.`,
- IDNA/punycode-encodes unicode domains,
- drops anything that isn't a plausible domain,
- unions + dedupes + sorts.

A source that 404s or times out is **skipped with a warning**, never failing the
run — but if **more than half** the sources fail, the run aborts and writes
nothing, so a bad network day can never truncate the published list.

## Sources & credits

All credit to these maintainers. This project only aggregates their work.

| Source | Format |
|---|---|
| [disposable-email-domains/disposable-email-domains](https://github.com/disposable-email-domains/disposable-email-domains) | `.conf` |
| [disposable/disposable-email-domains](https://github.com/disposable/disposable-email-domains) | `.txt` |
| [7c/fakefilter](https://github.com/7c/fakefilter) | `.txt` |
| [FGRibreau/mailchecker](https://github.com/FGRibreau/mailchecker) | `.txt` |
| [wesbos/burner-email-providers](https://github.com/wesbos/burner-email-providers) | `.txt` |
| [ivolo/disposable-email-domains](https://github.com/ivolo/disposable-email-domains) | `.json` |

## Contributing a source

Open a PR that adds one raw URL line to [`sources.txt`](sources.txt) (keep it a
maintained list that returns one domain per line, or a JSON array of domains).
The daily Action picks it up automatically on the next run.

## Versioning

Releases use semver `v1.0.PATCH`, where the patch auto-increments from the
latest tag (starting at `v1.0.0`). Major stays `1` on purpose — Go modules
require a `/vN` path suffix for major ≥ 2, so bumping the major would break
`go get`. A release (tag + GitHub Release + attached `domains.txt` / `domains.json`)
is cut **only when the domain set changed**; unchanged days produce nothing. Each
release note lists the total count and the `+added` / `-removed` delta.

## Publishing (maintainer notes)

`.github/workflows/publish.yml` runs on each published release and publishes the
packages. Each step **skips cleanly if its secret is missing**, so the repo works
before any tokens are configured:

| Package | Needs |
|---|---|
| npm | repo secret `NPM_TOKEN` |
| NuGet | repo secret `NUGET_API_KEY` |
| Go | nothing — the git tag *is* the release |

## License

[MIT](LICENSE) © Mehrdad TAT. The aggregated domain data is drawn from the
public sources listed above, each under its own license.
