#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

npm install --no-audit --no-fund

# Reihenfolge ist bindend: build_posts.py normalisiert src/app.jsx
# (sync_index_loader), erst danach darf daraus kompiliert werden.
./scripts/build_posts.py build
npm run build:js
./scripts/build_posts.py validate

if command -v npx >/dev/null 2>&1; then
  npx wrangler deploy
else
  echo "wrangler nicht gefunden. Bitte Node/npx installieren oder Deployment manuell starten." >&2
  exit 1
fi
