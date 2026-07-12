#!/usr/bin/env sh
# Usage: scripts/set-version.sh v1.0.3   (run from the repo root)
# Writes the numeric version (leading "v" stripped) into every package manifest.
set -e
v="${1#v}"
python3 - "$v" <<'PY'
import json, re, sys
v = sys.argv[1]

pj = "packages/npm/package.json"
with open(pj) as f:
    p = json.load(f)
p["version"] = v
with open(pj, "w") as f:
    json.dump(p, f, indent=2)
    f.write("\n")

cs = "packages/dotnet/DisposableEmailDomain.csproj"
with open(cs) as f:
    t = f.read()
t = re.sub(r"<Version>[^<]*</Version>", "<Version>%s</Version>" % v, t)
with open(cs, "w") as f:
    f.write(t)

print("set version", v)
PY
