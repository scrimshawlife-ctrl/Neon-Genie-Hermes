# Neon Genie v3.6 Release Checklist

## Required gates

- [ ] `python scripts/neon_genie.py do check`
- [ ] `python scripts/test_wave3_cli.py` (includes eval + recipe)
- [ ] `python scripts/run_fixture_invariants.py`
- [ ] `python scripts/neon_genie.py do eval` — all golden cases PASS
- [ ] `python scripts/neon_genie.py do recipe` — product-audit packaging PASS
- [ ] `python scripts/audit_release_version.py --strict`
- [ ] GitHub Actions `hermes-evals.yml` green
- [ ] `VERSION` / SKILL / manifest == **3.6.0**
- [ ] CHANGELOG has `## [3.6.0]`
- [ ] Authority remains `advisory_only`; recipe handoff stub has `grants_execution: false`

## Release procedure

1. Green CI on PR.
2. Merge to `main`.
3. Tag `v3.6.0` and publish GitHub Release from CHANGELOG.
4. `./install.sh` and re-run `do check` + `do eval`.

## Non-goals

- Full prose product invention is still Hermes skill runtime, not this CLI
- Eval runner is packaging-gate logic only
