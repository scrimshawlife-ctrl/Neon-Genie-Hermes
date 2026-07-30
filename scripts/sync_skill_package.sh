#!/usr/bin/env bash
# Sync repo root skill content into skills/neon-genie/ for Hermes tap installs.
# Also refresh hub mirrors under allowlisted dirs (references/, examples/).
# Usage: ./scripts/sync_skill_package.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/skills/neon-genie"

# --- Hub mirrors (Hermes Hub only installs allowlisted + SKILL.md-referenced paths) ---
mkdir -p "${ROOT}/references/schemas" "${ROOT}/references/profiles" "${ROOT}/examples/evals"
rsync -a --delete "${ROOT}/schemas/" "${ROOT}/references/schemas/"
rsync -a --delete "${ROOT}/profiles/" "${ROOT}/references/profiles/"
rsync -a --delete "${ROOT}/evals/" "${ROOT}/examples/evals/"
cp -f "${ROOT}/manifest.json" "${ROOT}/references/manifest.json"
cp -f "${ROOT}/VERSION" "${ROOT}/references/VERSION"

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
for f in PREMIERE.md DEMO.md ROADMAP.md HERMES_DISTRIBUTION.md README.md; do
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
echo "Hub mirrors: references/schemas, references/profiles, examples/evals, references/{VERSION,manifest.json}"
test -f "${DEST}/SKILL.md"
test -d "${DEST}/references/schemas"
test -d "${DEST}/references/profiles"
test -d "${DEST}/examples/evals"
