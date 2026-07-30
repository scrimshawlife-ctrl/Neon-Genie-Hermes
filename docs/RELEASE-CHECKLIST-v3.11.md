# Neon Genie v3.11 Release Checklist (Category ownership)

## Required gates

- [ ] `python scripts/neon_genie.py do check`
- [ ] `python scripts/neon_genie.py do eval` (16+)
- [ ] `python scripts/neon_genie.py do transcripts`
- [ ] `python scripts/test_wave3_cli.py`
- [ ] `python scripts/audit_release_version.py --strict`
- [ ] `docs/PREMIERE.md` present (thesis + comparison)
- [ ] `docs/DEMO.md` present (≤10 minute path)
- [ ] `examples/gallery/README.md` present
- [ ] README links PREMIERE + DEMO
- [ ] VERSION == **3.11.0**
- [ ] Authority remains `advisory_only`
- [ ] Premiere P0–P3 marked shipped on ROADMAP

## Content gates

- [ ] PREMIERE states find → request → NOT_COMPUTABLE
- [ ] Comparison vs idea agents (no overclaim of execution)
- [ ] DEMO ends without granting spend/publish/execute
