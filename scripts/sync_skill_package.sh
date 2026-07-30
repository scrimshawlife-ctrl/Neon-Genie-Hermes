#!/usr/bin/env bash
# Sync repo root skill content into skills/neon-genie/ for Hermes tap installs.
# Usage: ./scripts/sync_skill_package.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/skills/neon-genie"

mkdir -p "${DEST}"
rsync -a --delete \
  --exclude '.git' \
  --exclude 'out' \
  --exclude 'skills' \
  --exclude '.superpowers' \
  --exclude '__pycache__' \
  --exclude 'docs/superpowers' \
  --exclude 'docs/assets' \
  --exclude '*.pyc' \
  --exclude '.venv' \
  --exclude 'venv' \
  "${ROOT}/" "${DEST}/"

# Ensure core docs used by operators are present
mkdir -p "${DEST}/docs"
for f in PREMIERE.md DEMO.md ROADMAP.md README.md; do
  if [[ -f "${ROOT}/docs/${f}" ]]; then
    cp -f "${ROOT}/docs/${f}" "${DEST}/docs/${f}"
  fi
done

# Keep skills.sh.json at package root for hub groupings (also at repo root)
if [[ -f "${ROOT}/skills.sh.json" ]]; then
  cp -f "${ROOT}/skills.sh.json" "${DEST}/skills.sh.json"
fi

printf '%s\n' 'out/' '__pycache__/' '*.pyc' '.superpowers/' '.venv/' 'venv/' > "${DEST}/.gitignore"

echo "Synced skill package → ${DEST}"
test -f "${DEST}/SKILL.md"
