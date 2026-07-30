# Changelog

All notable changes to Neon Genie are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses semantic versioning.

## [3.2.0] — 2026-07-30

### Added

- Root-level Hermes skill packaging (installable skill root)
- `install.sh` → `~/.hermes/skills/neon-genie`
- `references/hermes-runtime-contract.md`
- `scripts/validate_hermes_skill.py` smoke validator
- `VERSION`, `QUICKSTART.md`, `docs/ROADMAP.md`, `docs/README.md`
- `examples/` operator briefs
- `evals/` fixture home + rubric skeleton

### Changed

- Flattened nested `neon-genie/` package to repository root
- Version alignment across `VERSION`, `SKILL.md`, and `manifest.json`

### Migration

- Replace `cp -R neon-genie …` with `./install.sh` or copy the **repository root** into Hermes skills

## [3.1.0] — prior

- Proactive research by default
- MIT license
- Packaging README polish and social assets
