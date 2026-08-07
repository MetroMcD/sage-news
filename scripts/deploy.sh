#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# build kompiliert das JSX selbst mit (compile_js), sobald sich src/*.jsx
# geaendert hat — inklusive korrekter Reihenfolge nach sync_index_loader.
./scripts/build_posts.py build
./scripts/build_posts.py validate

if command -v npx >/dev/null 2>&1; then
  npx wrangler deploy
else
  echo "wrangler nicht gefunden. Bitte Node/npx installieren oder Deployment manuell starten." >&2
  exit 1
fi
