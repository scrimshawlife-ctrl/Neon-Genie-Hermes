# Distributing Neon Genie on the Hermes Skills Hub

Neon Genie is a **specialized** skill (product / opportunity intelligence). It is a good fit for the **Skills Hub** and **GitHub taps**, not for the universal bundled catalog that ships with every Hermes install.

Official guidance ([Hermes CONTRIBUTING](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)):

| Path | When |
|------|------|
| **Bundled** `skills/` in hermes-agent | Broadly useful to *most* users (docs, common dev, etc.) |
| **Optional official** `optional-skills/` | Official but not universal |
| **Skills Hub / taps / community** | Specialized or third-party — **this is Neon Genie** |

---

## Recommended: publish as a GitHub skill tap

This repo is already public. Tap layout:

```text
scrimshawlife-ctrl/Neon-Genie-Hermes
├── skills/
│   └── neon-genie/          # install slug
│       ├── SKILL.md
│       ├── profiles/
│       ├── schemas/
│       ├── scripts/
│       ├── …
└── skills.sh.json           # hub category grouping
```

### For operators (install)

```bash
# Subscribe to the tap (once)
hermes skills tap add scrimshawlife-ctrl/Neon-Genie-Hermes

# Install the skill (security scan runs)
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie

# Or install one skill without adding the whole tap
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```

Also works:

```bash
# After clone
./install.sh
# → ~/.hermes/skills/neon-genie
```

### For maintainers (keep package in sync)

Canonical contract: **`distribution.yaml`**. After changing schemas, profiles, scripts, examples, or SKILL packaging:

```bash
python scripts/distribution_spine.py write   # or: ./scripts/sync_skill_package.sh
python scripts/distribution_spine.py verify
git add distribution.yaml SKILL.md references/ examples/evals skills/neon-genie
git commit -m "chore: sync distribution spine + hub package"
```

| Command | Purpose |
|---------|---------|
| `do dist verify` | Fail on mirror drift, bad hub refs, package parity |
| `do dist write` | Refresh mirrors, regenerate SKILL support list, rsync package |
| `do dist report` | JSON report for CI/agents |

Diagnostics use `NG-PKG-*` codes (see spine stderr).
---

## Alternate discovery paths

| Method | Command / action |
|--------|------------------|
| **Direct GitHub path** | `hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie` |
| **Direct SKILL.md URL** | `hermes skills install https://raw.githubusercontent.com/scrimshawlife-ctrl/Neon-Genie-Hermes/main/skills/neon-genie/SKILL.md` (support files follow references) |
| **skills.sh** | Optional: list on [skills.sh](https://skills.sh/) if you want Vercel directory discovery |
| **ClawHub** | `hermes skills publish skills/neon-genie --to clawhub` (when ready for that marketplace) |
| **Discord** | Share in [Nous Research Discord](https://discord.gg/NousResearch) Skills channel for community install |

Inspect before install:

```bash
hermes skills inspect scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```

---

## Official Hermes catalog (optional, higher bar)

To appear under **official optional** skills (`hermes skills browse --source official`):

1. Open a PR against [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) adding a slim package under `optional-skills/` (e.g. `optional-skills/product/neon-genie/`).
2. Follow their skill authoring standards (frontmatter, description, verification).
3. Expect review for security, scope, and maintenance burden.

**Do not** open a PR to put Neon Genie in core **bundled** `skills/` unless Nous asks — it is specialized, not universal.

---

## Pre-submit checklist

- [x] Public GitHub repo with MIT license  
- [x] `SKILL.md` with `name`, `description`, `version`, `author`, `platforms`  
- [x] `metadata.hermes.tags` + `category` for hub indexing  
- [x] `skills/neon-genie/` package for tap discovery  
- [x] `skills.sh.json` grouping  
- [x] Install path documented (`./install.sh` + `hermes skills install …`)  
- [x] `do doctor` / `do check` pass  
- [x] `hermes skills inspect` — listed (skills.sh / community)  
- [x] `hermes skills install …` — security scan SAFE, installs as community  
- [x] Tap registered: `hermes skills tap add scrimshawlife-ctrl/Neon-Genie-Hermes`  
- [ ] Announce on Discord / social with install one-liner  

### Hub install vs full package

Hermes Hub only copies **explicitly path-referenced** files under  
`references/`, `templates/`, `scripts/`, `assets/`, `examples/`  
(security allowlist).

As of **v3.17+**, Neon Genie ships **hub mirrors** of the packaging tree.
As of **v3.18.0**, mirrors + package + SKILL list are driven by **`distribution.yaml`**
(no hand-maintained triple drift).

| Full install | Hub mirror (allowlisted) |
|--------------|--------------------------|
| `schemas/` | `references/schemas/` |
| `profiles/` | `references/profiles/` |
| `evals/` | `examples/evals/` |
| `VERSION`, `manifest.json` | `references/VERSION`, `references/manifest.json` |

`SKILL.md` support-file bullets are **generated** so  
`hermes skills install …` pulls a **working packaging CLI** (`do doctor` green).

Scripts resolve either layout via `scripts/paths.py`.

**Still recommended for maintainers:** clone + `./install.sh` (full tree + docs + CI).

### Runtime verification (v3.19+)

```bash
python scripts/neon_genie.py do behavioral --suite
python scripts/neon_genie.py do runtime              # hub-layout smoke
python scripts/neon_genie.py do runtime --hermes     # isolated HERMES_HOME when CLI present
```

Behavioral cases live under `evals/behavioral/` (mirrored to `examples/evals/behavioral/`).
They assert **semantic invariants** (OPEN→SEAL, claim labels, DataRequest, authority), not exact prose.
---

## One-liner for users

```bash
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```
