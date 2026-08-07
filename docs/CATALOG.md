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

Verified: security scan SAFE, hub install pulls `PRIVACY.md` / privacy runtime + schemas via hub support list, `do doctor` green (hub layout). Skill **3.25.0** ships privacy-by-construction (`do privacy --json`, always-on `privacy` profile) plus founder cold-start routing and `capital_sprint` packaging.

## Official optional catalog (PR)

**PR:** https://github.com/NousResearch/hermes-agent/pull/75028

Per [Hermes optional skills contributing](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog):

1. `optional-skills/productivity/neon-genie/` — curated leaf (not monorepo dump)
2. Hub-style layout: `references/profiles` + `references/schemas` only
3. Packaging CLI + examples + golden evals; `do doctor` green
4. Upstream monorepo remains source of truth for releases / distribution spine

After merge:

```bash
hermes skills install official/productivity/neon-genie
hermes skills browse --source official
```

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
