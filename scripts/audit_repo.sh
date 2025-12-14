#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$1"
OUT_DIR="$2"

mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"   # ← 追加：絶対パス化
cd "$REPO_DIR"

corepack enable >/dev/null 2>&1 || true

if [ -f package-lock.json ]; then
  npm ci || npm install             # ← 変更：ci失敗でも進む
  npm audit --audit-level=high --json > "$OUT_DIR/audit.json" || true

elif [ -f pnpm-lock.yaml ]; then
  pnpm install --frozen-lockfile || pnpm install
  pnpm audit --audit-level=high --json > "$OUT_DIR/audit.json" || true

elif [ -f yarn.lock ]; then
  (yarn install --immutable) || (yarn install --frozen-lockfile) || yarn install
  yarn audit --json > "$OUT_DIR/audit.json" || true

else
  echo "No lockfile (package-lock.json / pnpm-lock.yaml / yarn.lock). Skip."
fi
