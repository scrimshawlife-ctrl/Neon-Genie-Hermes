# Neon Genie v3.5 Release Checklist

## Required gates

- [ ] `python scripts/neon_genie.py do check`
- [ ] `python scripts/test_wave3_cli.py`
- [ ] `python scripts/run_fixture_invariants.py`
- [ ] `python scripts/audit_release_version.py --strict`
- [ ] GitHub Actions workflow `.github/workflows/hermes-evals.yml` green on PR
- [ ] `VERSION` == `SKILL.md` frontmatter == `manifest.json` == **3.5.0**
- [ ] `CHANGELOG.md` has `## [3.5.0]` section
- [ ] README / QUICKSTART document install + CLI
- [ ] Domain isolation: no Kubrick cinematic content in skill corpus
- [ ] Authority remains `advisory_only`
- [ ] Optional: `./install.sh` into clean Hermes path and re-run `do check`

## Release procedure

1. Confirm default branch CI is green.
2. Review `CHANGELOG.md` and version declarations.
3. Confirm no secrets or local absolute paths in skill docs.
4. Merge release PR to `main`.
5. Tag `v3.5.0` from verified `main` commit.
6. Publish GitHub Release from CHANGELOG 3.5.0 notes.
7. Reinstall skill and validate.

## Non-goals

- External model APIs not required for release gates
- Wayfinder / Kubrick remain optional siblings
- CLI does not invent product opportunities or grant execution
