#!/usr/bin/env bash
# Neon Genie environment bootstrap.
#
# Neon Genie is a pure-standard-library Python 3.11+ project: there are no
# third-party runtime dependencies, so there is nothing to `pip install`.
# The repository's docs and CI invoke the interpreter as `python`, while the
# base image only ships `python3`. This script makes `python` resolve to
# Python 3 so the documented commands work verbatim. It is idempotent.
set -euo pipefail

export PATH="${HOME}/.local/bin:${PATH}"

if ! command -v python >/dev/null 2>&1; then
  if command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq python-is-python3
  else
    mkdir -p "${HOME}/.local/bin"
    ln -sf "$(command -v python3)" "${HOME}/.local/bin/python"
  fi
fi

echo "Using $(python --version 2>&1) at $(command -v python)"

# Lightweight integrity check so a broken checkout fails fast at setup time.
python scripts/neon_genie.py do check
