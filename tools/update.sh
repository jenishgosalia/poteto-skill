#!/usr/bin/env bash
# Pull the latest upstream pstack, re-port it, validate, and report the version/SHA.
# Usage: tools/update.sh [upstream-ref]   (default: main)
set -euo pipefail
cd "$(dirname "$0")/.."
REF="${1:-main}"
TMP="$(mktemp -d)"
git clone -q --depth 1 --filter=blob:none --sparse --branch "$REF" https://github.com/cursor/plugins.git "$TMP/up"
git -C "$TMP/up" sparse-checkout set pstack -q
SHA="$(git -C "$TMP/up" rev-parse HEAD)"
python3 -I tools/port.py "$TMP/up/pstack" pstack
claude plugin validate . --strict
echo "$SHA" > UPSTREAM_SHA
VER="$(python3 -c "import json;print(json.load(open('pstack/.claude-plugin/plugin.json'))['version'])")"
echo "upstream $SHA  plugin version $VER"
rm -rf "$TMP"
