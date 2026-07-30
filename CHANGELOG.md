# Changelog

All notable changes to Neon Genie are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses semantic versioning.

## [3.15.0] — 2026-07-30

### Changed

- README: plain-English **How to use** (Hermes chat vs CLI), command cheat sheet, agent rules
- Simplified CLI help: jobs grouped (everyday / verify / outcomes)
- QUICKSTART aligned with the same command shape
- SKILL packaging section shortened to the `do <job>` table

## [3.14.0] — 2026-07-30

### Added

- Recipes: `evidence` (find/request scaffold) and `opportunity` (blocked transition + completion_proof)
- Briefs: `examples/evidence.brief.yaml`, `examples/opportunity.brief.yaml`
- Transcripts 08–09 (9 total goldens)
- Doctor/CI cover evidence + opportunity

### Changed

- Full profile-adjacent recipe surface (10 recipes)

## [3.13.0] — 2026-07-30

### Added

- Recipes: `agentic` (x402 REJECT scaffold) and `memetic` (Gate D promotion cap)
- Briefs: `examples/agentic.brief.yaml`, `examples/memetic.brief.yaml`
- Transcripts: `06-agentic-x402-misfit.md`, `07-memetic-cannot-promote.md` (7 total)
- Doctor suite smokes agentic + memetic recipes

### Changed

- Gallery/examples indexes; ROADMAP maintenance 3.13.0

## [3.12.0] — 2026-07-30

### Added

- Corpus depth: `commercial` and `audit` packaging recipes + briefs
- `do doctor` full-suite operator smoke (`scripts/doctor.py`)
- Gallery/examples index updates for new recipes

### Changed

- CI runs commercial/audit recipes and doctor suite
- ROADMAP maintenance section documents 3.12.0

## [3.11.0] — 2026-07-30

### Added

- Category ownership (Wave P3): `docs/PREMIERE.md` thesis & comparison vs idea agents
- `docs/DEMO.md` — 10-minute install → check → eval → recipe → learn path
- `examples/gallery/README.md` — sanitized briefs, packets, transcripts index
- README short comparison table + premiere/demo nav links
- RELEASE-CHECKLIST-v3.11

### Changed

- Premiere program P0–P3 marked complete on ROADMAP and design spec
- Skill validator requires PREMIERE.md, DEMO.md, gallery README

## [3.10.0] — 2026-07-30

### Added

- Outcome density (Wave P2): `completion_proof` required on opportunity/product/zero-option schemas
- `proof_path` property on those packets; recipes emit proof paths
- Learning ledger: `schemas/learning-ledger-entry.schema.json`, `do learn` / `record_learning.py` (PROPOSED only)
- `references/post-seal-verification.md` checklist
- Golden evals: completion-proof required/present (16 total)

### Changed

- SKILL SEAL/memory doctrine ties packets to proof + ledger
- Docs/ROADMAP premiere P2 marked shipping

## [3.9.0] — 2026-07-30

### Added

- Golden prose transcripts (`evals/transcripts/`) for five premiere scenarios
- Transcript rubric + structural checker: `do transcripts` / `scripts/check_transcripts.py`
- CI step for transcript checks
- Docs: premiere positioning in README, RELEASE-CHECKLIST-v3.8/v3.9, docs index

### Changed

- ROADMAP: P0 shipped, P1 shipped as 3.9.0
- Premiere design spec: P0 success criteria checked off

## [3.8.0] — 2026-07-30

### Added

- Evidence Request Protocol: find public → request private → only then `NOT_COMPUTABLE`
- `schemas/data-request.schema.json` and `examples/packets/sample-data-request.json`
- Anti-overclaim gates **P–R** (skip-find, skip-request, silent private invent)
- Receipt evidence fields: `data_requests`, `open_blocking_requests`, `research_attempts`, `evidence_protocol`
- `build_receipt.py --data-requests`; product-audit recipe surfaces open DataRequests
- Golden evals: public-gap find (P), private-gap request (Q), silent invent (R) — 14 total cases
- Premiere program roadmap section (P0–P3)

### Changed

- Skill doctrine, Hermes runtime contract, and CAPABILITY_MAP gates **A–R**
- Skill validator requires `schemas/data-request.schema.json`

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
