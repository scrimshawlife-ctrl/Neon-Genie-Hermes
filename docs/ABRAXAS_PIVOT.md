# Abraxas → Neon Genie Hermes pivot

**Status:** ACTIVE (2026-07-31)  
**Authority:** advisory_only · no execution · no Abraxas canon mutation  
**Related PR:** privacy runtime on `main` (#17)

## Decision

**Canonical Hermes packaging skill for Neon Genie lives in this repository:**

| Item | Value |
|------|--------|
| Repo | `scrimshawlife-ctrl/Neon-Genie-Hermes` |
| Hub path | `skills/neon-genie` |
| Install | `hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie` |
| Local clone | `./install.sh` → `~/.hermes/skills/neon-genie` |
| Entry | `run-envelope.json` after packaging; judgment in `SKILL.md` |
| Privacy | `PRIVACY.md` · default `local_only` · purpose-bound consent only |

**Abraxas-v2.0** remains the governed symbolic-intelligence architecture and the **Abraxas-side** invention umbrella (`skills/abx-neon-genie`). It does **not** absorb packaging, Hub distribution, or skill contracts owned here.

## Split of concerns

| Concern | Owner |
|---------|--------|
| OPEN→SEAL packaging, receipts, envelopes, Hub mirrors, privacy runtime | **Neon-Genie-Hermes** (this repo) |
| Invention routing, overlap/ownership matrix vs AAL subsystems, venture shaping umbrella | **Abraxas** `abx-neon-genie` |
| Forecasting, oracle, YGGDRASIL, governance V3 | **Abraxas** core (never Neon Genie) |
| Wayfinder execution planning | Wayfinder (consumes envelopes; does not rewrite product intent) |

## Operator path after pivot

1. **Product / opportunity packaging & Hermes skill work** → this repo (`do doctor`, recipes, privacy, dist).
2. **Abraxas invention umbrella / ownership routing** → Abraxas `skills/abx-neon-genie` (route specialized work; do not re-implement packaging).
3. **Downstream Abraxas docs** that plan Neon Genie ventures stay docs-only; they must link here for executable skill packaging.

## Explicit non-goals

- Not a merge of Abraxas into Neon Genie.
- Not runtime authority for Abraxas or Neon Genie.
- Not promotion of Abraxas canon from this skill.
- Not a global privacy or governance disable.

## Evidence

- Privacy-by-construction runtime merged: `main` #17  
- Abraxas binding note: `docs/ventures/NEON_GENIE_HERMES_PIVOT_017.md` in Abraxas-v2.0  
- Abraxas skill pointer: `skills/abx-neon-genie/SKILL.md` (canonical packaging home)
