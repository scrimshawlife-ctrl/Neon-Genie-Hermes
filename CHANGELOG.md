# Changelog

All notable changes to Neon Genie are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses semantic versioning.

## [3.7.0] — 2026-07-30

### Added

- Multi-recipe runner: `do recipe --name product-audit|zero-option|zero-option-executable|fragmentation`
- `scripts/recipe_common.py`, `scripts/recipe_run.py`
- Briefs: `fragmentation.brief.yaml`, `zero-option-with-skills.brief.yaml`
- Sample packets under `examples/packets/`
- Deeper packet validator (typed JSON Schema subset + `--strict-authority`)
- Eval cases: `fictional-resource`, `scorecard-cannot-override-gate`

### Changed

- `do recipe` defaults to multi-recipe dispatcher (product-audit still default name)
- CI runs all packaging recipes + sample packet validation

## [3.6.0] — 2026-07-30

### Added

- Golden gate eval runner: `python scripts/neon_genie.py do eval` (`scripts/run_hermes_evals.py`)
- Product-audit packaging recipe: `python scripts/neon_genie.py do recipe`
- CLI intents `eval` and `recipe`; aliases `run-evals`, `product-audit`
- CI runs golden evals + recipe; uploads `out/neon-genie/` artifacts
- `.gitignore` for generated `out/`

### Notes

- Eval runner enforces packaging-level gate logic against `evals/cases/*` expected fields
- Recipe emits route + receipt + Wayfinder handoff stub (no product invention)

## [3.5.0] — 2026-07-30

### Added

- GitHub Actions: `.github/workflows/hermes-evals.yml` (check, CLI tests, fixtures, version audit)
- `scripts/run_fixture_invariants.py`
- `scripts/audit_release_version.py`
- `docs/RELEASE-CHECKLIST-v3.5.md`

### Changed

- Roadmap Wave 4 marked shipped

## [3.4.0] — 2026-07-30

### Added

- Thin packaging CLI: `python scripts/neon_genie.py do <check|validate|route|receipt>`
- `scripts/validate_packet.py`, `route_profiles.py`, `build_receipt.py`
- `scripts/test_wave3_cli.py` regression harness

### Notes

- CLI is packaging-only (no product brain, no research, no execution authority)

## [3.3.0] — 2026-07-30

### Added

- Packet schemas: `evidence-intelligence`, `memetic-pressure`, `audit-delivery`
- `references/anti-overclaim-patterns.md` (gates A–O)
- Eval cases: memetic promote block, offline fabrication, buyer conflation, authority leakage
- Thickened profile contracts (triggers, required fields, CLEAR rules, schema pointers)

### Changed

- Profiles expanded for operational clarity without changing mission or authority
- SKILL output selection links all packet schemas

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
