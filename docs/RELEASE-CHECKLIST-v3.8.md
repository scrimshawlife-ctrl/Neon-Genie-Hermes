# Neon Genie v3.8 Release Checklist (Evidence spine)

## Status

| Item | Status |
|------|--------|
| Wave P0 Evidence Request Protocol | Shipped **v3.8.0** |
| GitHub Release | https://github.com/scrimshawlife-ctrl/NeonGenie/releases/tag/v3.8.0 |

## Required gates

- [x] `python scripts/neon_genie.py do check`
- [x] `python scripts/neon_genie.py do eval` — **14/14**
- [x] `python scripts/test_wave3_cli.py`
- [x] `python scripts/run_fixture_invariants.py`
- [x] `python scripts/audit_release_version.py --strict`
- [x] `schemas/data-request.schema.json` present
- [x] Doctrine: find → request → NOT_COMPUTABLE
- [x] Anti-overclaim gates **A–R**
- [x] Receipt fields: `data_requests`, `open_blocking_requests`, `research_attempts`
- [x] Authority remains `advisory_only`
- [x] No Kubrick domain merge

## Spec / plan

- `docs/superpowers/specs/2026-07-30-neon-genie-premiere-program-design.md`
- `docs/superpowers/plans/2026-07-30-neon-genie-evidence-spine-p0.md`
