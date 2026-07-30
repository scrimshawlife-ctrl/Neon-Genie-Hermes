# Neon Genie v3.9 Release Checklist (Prose transcripts)

## Required gates

- [ ] `python scripts/neon_genie.py do check`
- [ ] `python scripts/neon_genie.py do eval` (14+)
- [ ] `python scripts/neon_genie.py do transcripts` (5 goldens)
- [ ] `python scripts/test_wave3_cli.py`
- [ ] `python scripts/audit_release_version.py --strict`
- [ ] VERSION / SKILL / manifest / README == **3.9.0**
- [ ] CHANGELOG has `## [3.9.0]`
- [ ] `evals/transcripts/` has ≥5 scenario goldens + rubric
- [ ] Authority remains `advisory_only`

## P1 content

| Transcript | Present |
|------------|---------|
| zero-option empty | |
| product audit | |
| fragmentation | |
| commercial missing buyer | |
| offline audit | |
