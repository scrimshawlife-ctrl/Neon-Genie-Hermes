# Hermes Skills Catalog — Neon Genie submission

## Paths

| Catalog | Status | How users install |
|---------|--------|-------------------|
| **Community Skills Hub / GitHub tap** | **Live** | `hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie` |
| **Official optional** (`optional-skills/`) | **PR to hermes-agent** | `hermes skills install official/productivity/neon-genie` (after merge) |
| **Core bundled** | **Not requested** | Specialized skill — wrong fit |

## Community Hub (done)

```bash
hermes skills tap add scrimshawlife-ctrl/Neon-Genie-Hermes
hermes skills inspect scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```

Package layout:

```text
skills/neon-genie/     # tap install root
skills.sh.json         # Product Intelligence grouping
distribution.yaml      # mirror + support-file contract
```

Verified: security scan SAFE, hub install ~118 files, `do doctor` green (hub layout).

## Official optional catalog (PR)

Per [Hermes optional skills contributing](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog):

1. Add `optional-skills/productivity/neon-genie/` (SKILL.md + support tree)
2. Open PR against `NousResearch/hermes-agent`
3. After merge: appears under `hermes skills browse --source official`

```bash
hermes skills install official/productivity/neon-genie
```

Upstream remains the source of truth for packaging releases; optional catalog tracks major skill versions.

## Maintainer refresh

```bash
python scripts/distribution_spine.py write
python scripts/neon_genie.py do release-check
python scripts/neon_genie.py do doctor
git tag vX.Y.Z && git push origin vX.Y.Z   # Release workflow
```

## Announce (optional)

Share one-liner in [Nous Research Discord](https://discord.gg/NousResearch) skills channel:

```text
Neon Genie — evidence-bound product/opportunity intelligence (advisory only)
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```
