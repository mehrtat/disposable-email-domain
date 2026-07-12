#!/usr/bin/env sh
# Copy the canonical domain list into each language package so every published
# package ships the SAME data. Run from anywhere; paths resolve to the repo root.
# Go embeds the root domains.txt directly, so it needs no copy.
set -e
root="$(cd "$(dirname "$0")/.." && pwd)"
cp "$root/domains.json" "$root/packages/npm/domains.json"
cp "$root/domains.txt"  "$root/packages/dotnet/domains.txt"
echo "synced domains.json -> packages/npm, domains.txt -> packages/dotnet"
