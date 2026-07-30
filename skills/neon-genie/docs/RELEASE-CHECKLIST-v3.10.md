# Neon Genie v3.10 Release Checklist (Outcome density)

## Required gates

- [ ] `python scripts/neon_genie.py do check`
- [ ] `python scripts/neon_genie.py do eval` (16+)
- [ ] `python scripts/neon_genie.py do transcripts`
- [ ] `python scripts/test_wave3_cli.py`
- [ ] `python scripts/audit_release_version.py --strict`
- [ ] opportunity/product/zero-option schemas require `completion_proof`
- [ ] `do learn` appends PROPOSED ledger entries only
- [ ] `references/post-seal-verification.md` present
- [ ] VERSION == **3.10.0**
- [ ] Authority `advisory_only`; no auto-canon
