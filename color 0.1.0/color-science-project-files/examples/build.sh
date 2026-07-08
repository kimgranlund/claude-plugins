#!/usr/bin/env bash
# Build the examples site: optionally recompile TS → ES modules, then bundle
# everything into a single IIFE classic-script.
#
# Output: lib/dist/refcolor.bundle.js — works directly over file:// because it's
# a classic <script>, not an ES module (file:// has each-file-is-own-origin and
# blocks ESM imports).

set -euo pipefail
cd "$(dirname "$0")"

# Step 1 — TypeScript compile (only if the user has tsc available locally).
# The committed lib/dist/ already contains the latest compile, so this step is
# only required after editing source TS in ../src/.
if [ -x "./node_modules/.bin/tsc" ]; then
  echo "[1/2] Compiling TypeScript (../src/ → lib/dist/) ..."
  ./node_modules/.bin/tsc -p tsconfig.json
elif command -v tsc >/dev/null 2>&1; then
  echo "[1/2] Compiling TypeScript (../src/ → lib/dist/) ..."
  tsc -p tsconfig.json
else
  echo "[1/2] Skipping TS compile (no local 'tsc' found — install with: npm i -D typescript)"
fi

# Step 2 — Bundle everything into one classic IIFE.
echo "[2/2] Bundling to IIFE (bundle-entry.js → lib/dist/refcolor.bundle.js) ..."
npx --yes esbuild bundle-entry.js \
  --bundle \
  --format=iife \
  --target=es2020 \
  --outfile=lib/dist/refcolor.bundle.js

echo "Done. Open index.html directly in a browser."
