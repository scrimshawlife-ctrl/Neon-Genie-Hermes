<div align="center">

# Neon Genie

### Governed opportunity & product intelligence for Hermes

[![Version](https://img.shields.io/badge/version-3.16.0-7c3aed?style=for-the-badge)](./manifest.json)
[![Hermes Skill Evals](https://img.shields.io/github/actions/workflow/status/scrimshawlife-ctrl/Neon-Genie-Hermes/hermes-evals.yml?branch=main&label=hermes-evals&style=for-the-badge)](./.github/workflows/hermes-evals.yml)
[![Authority](https://img.shields.io/badge/authority-advisory%20only-0ea5e9?style=for-the-badge)](#authority--safety)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge)](./LICENSE)

<img src="docs/assets/hero.jpg" alt="Neon Genie — luminous lamp on a dark network grid" width="920" />

**Turn weak signals and blocked transitions into evidence-bound, testable product and opportunity packets — without inventing facts or granting spend/execute rights.**

[How to use](#how-to-use) · [Install](#installation) · [Commands](#command-cheat-sheet) · [Demo](./docs/DEMO.md) · [Premiere](./docs/PREMIERE.md)

</div>

---

## What it is

Neon Genie is a **Hermes skill** (this repo root is the skill). It helps you:

- audit product coherence and draft Wayfinder-ready handoffs  
- mine opportunities and zero-capital first-cash loops  
- map fragmentation, commercial models, agentic graphs, evidence gaps  
- **fail closed** when proof, buyer, or access is missing  

It is **not** Kubrick (cinematic), **not** Wayfinder (engineering execution), and **not** a free-form idea generator.

| Principle | In practice |
|-----------|-------------|
| Evidence-bound | Claims are `OBSERVED` · `INFERRED` · `SPECULATIVE` · `NOT_COMPUTABLE` |
| Find or request | Public facts → research. Private facts → `DataRequest`. Never invent. |
| Advisory only | May draft and recommend. May **not** spend, publish, contact, or mutate repos. |
| Smallest profiles | Loads only the contracts the job needs (`core` always). |

---

## How to use

### Option A — Talk to Hermes (normal use)

1. Install the skill ([below](#installation)).
2. In Hermes, invoke Neon Genie (or say product audit / opportunity / zero option / wayfinder handoff).
3. Describe the job in plain language: who is stuck, what “done” looks like, constraints, what they already know.
4. Hermes follows `SKILL.md`: **OPEN → ALIGN → ASCEND → CLEAR → SEAL**.
5. Treat outputs as **drafts** until you review them. Packets never authorize money or publication.

**Example prompts**

```text
/neon-genie audit this project using product_architecture, commercial,
and wayfinder_handoff. Research decision-critical public facts. Request
private access instead of inventing. Label every material claim.
Do not modify the repository.
```

```text
/neon-genie zero_option: first cash in 7 days from declared skills and
access only. No fictional resources. Mark unknowns NOT_COMPUTABLE.
```

```text
/neon-genie research.enabled=false
# offline: operator + workspace sources only
```

Full prompt patterns and missing-data rules: [QUICKSTART.md](./QUICKSTART.md).  
Worked OPEN→SEAL examples: [evals/transcripts/](./evals/transcripts/).

### Option B — Command line (agents, CI, packaging)

From a clone or install directory, one pattern:

```text
python scripts/neon_genie.py do <job> [options]
```

| Job | Plain English |
|-----|----------------|
| `doctor` | **Start here** — run the full smoke suite |
| `check` | Is the skill install valid? |
| `recipe` | Run a named example end-to-end (product audit, zero-option, …) |
| `route` | Which profiles fit this brief/text? |
| `validate` | Does this packet JSON match its schema? |
| `receipt` | Build an advisory run receipt (hashes, optional DataRequests) |
| `eval` | Run golden fail-closed gate tests |
| `transcripts` | Check golden prose transcript structure |
| `learn` | Append a PROPOSED outcome note to a local ledger (never auto-canon) |

```bash
python scripts/neon_genie.py help          # list jobs
python scripts/neon_genie.py help recipe   # job-specific help
python scripts/neon_genie.py do doctor     # full smoke
```

Packaging CLI does **not** invent opportunities. It validates, routes, recipes, and tests. Creative judgment stays in Hermes + `SKILL.md`.

### A simple path: idea → packet → check

```bash
# 1. Install
./install.sh

# 2. Smoke the install
python scripts/neon_genie.py do doctor

# 3. Run a sample job
python scripts/neon_genie.py do recipe --name product-audit --out out/neon-genie/demo

# 4. Inspect out/neon-genie/demo/
#    profile-route, product stub, DataRequests, receipt — all advisory
```

Ten-minute walkthrough: [docs/DEMO.md](./docs/DEMO.md).

---

## Installation

### Hermes Skills Hub (recommended)

```bash
# One-liner install (GitHub path)
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie

# Or subscribe as a tap, then install
hermes skills tap add scrimshawlife-ctrl/Neon-Genie-Hermes
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```

Inspect first: `hermes skills inspect scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie`

### Clone + local install

```bash
git clone https://github.com/scrimshawlife-ctrl/Neon-Genie-Hermes.git
cd Neon-Genie-Hermes
./install.sh
# → ~/.hermes/skills/neon-genie
```

Or copy the skill package / repo root into your Hermes skills directory.

Then:

```bash
python scripts/neon_genie.py do check
# or: python ~/.hermes/skills/neon-genie/scripts/neon_genie.py do doctor
# reload / restart Hermes
```

**Notes**

- Needs a Hermes runtime that loads custom skills.  
- No external knowledge base required to load.  
- Research uses host tools when available; use offline mode when not.  
- Sibling skill: [Kubrick](https://github.com/scrimshawlife-ctrl/Kubrick) (cinematic) — not a dependency.  
- Distribution & catalog paths: [docs/HERMES_DISTRIBUTION.md](./docs/HERMES_DISTRIBUTION.md)

---

## Command cheat sheet

```bash
# Everyday
python scripts/neon_genie.py do doctor
python scripts/neon_genie.py do recipe --list
python scripts/neon_genie.py do recipe --name product-audit --out out/neon-genie/run1
python scripts/neon_genie.py do recipe --name zero-option --out out/neon-genie/zero

# Briefs & routing
python scripts/neon_genie.py do route --request examples/product-audit.brief.yaml --json
python scripts/neon_genie.py do route --text "first cash zero capital"

# Packets
python scripts/neon_genie.py do validate --packet path/to/packet.json --type opportunity
python scripts/neon_genie.py do validate --packet path/to/receipt.json --type receipt --strict-authority

# Quality / CI
python scripts/neon_genie.py do check
python scripts/neon_genie.py do eval
python scripts/neon_genie.py do transcripts

# After a real outcome (local only)
python scripts/neon_genie.py do learn \
  --class proof_obtained \
  --summary "first paid diagnostic booked" \
  --ledger out/neon-genie/learning-ledger.jsonl
```

### Recipes (`do recipe --name …`)

| Name | Use when |
|------|----------|
| `product-audit` | Product boundary + commercial + Wayfinder handoff stub |
| `opportunity` | Blocked transition → testable opportunity + proof |
| `zero-option` | No skills/access → honest `NOT_COMPUTABLE` |
| `zero-option-executable` | Declared skills → micro-loop stub |
| `fragmentation` | Multi-system friction / defrag scan |
| `commercial` | Pricing scaffold + buyer DataRequest |
| `audit` | Offline diagnostic / cost-of-inaction scaffold |
| `evidence` | Find/request evidence intelligence scaffold |
| `agentic` | Agent action graph; ornamental x402 rejected |
| `memetic` | Names/hooks; cannot raise promotion past evidence fail |

Briefs live in [`examples/`](./examples/). Gallery index: [`examples/gallery/`](./examples/gallery/).

---

## For agents (Hermes / automation)

**Prefer conversation** for product/opportunity work: load the skill, follow `SKILL.md`, use host research tools, emit labeled packets.

**Use the CLI** when you need deterministic packaging:

| Goal | Command |
|------|---------|
| Verify install before a run | `do check` or `do doctor` |
| Scaffold an example packet set | `do recipe --name <name> --out <dir>` |
| Choose profiles from text/brief | `do route --text "…" --json` |
| Schema-check a packet | `do validate --packet … --type …` |
| CI / regression | `do eval` + `do transcripts` |
| Record operator-reported outcome | `do learn …` (PROPOSED only) |

**Rules agents must keep**

1. Never treat model prior as `OBSERVED`.  
2. Public gap → attempt research; private gap → `DataRequest`; then `NOT_COMPUTABLE` if still missing.  
3. No spend, publish, contact, or repo mutation without separate authorization.  
4. Wayfinder handoffs must not rewrite product intent.  
5. `TESTABLE`+ packets need `completion_proof`.

Runtime contract: [`references/hermes-runtime-contract.md`](./references/hermes-runtime-contract.md).

---

## How it works (short)

Always: **OPEN → ALIGN → ASCEND → CLEAR → SEAL**.

Missing data: **find** (public) → **request** (private) → **`NOT_COMPUTABLE`**.

| Mode | Does |
|------|------|
| OPEN | Resolve request, actor, state, constraints, artifact |
| ALIGN | Sources, gaps, research plan / first fetch |
| ASCEND | Topology, thesis, intervention, score, route |
| CLEAR | Fail-closed gates, authority leaks, uncited facts |
| SEAL | Packets + receipt (DataRequests, research log) |

Profiles (loaded as needed): `core`, `product_architecture`, `opportunity_mining`, `fragmentation`, `zero_option`, `agentic_services`, `commercial`, `evidence_intelligence`, `memetic`, `audit_delivery`, `wayfinder_handoff` — see [`profiles/`](./profiles/).

**Promotion:** composite scores never override gate failures. Memetic strength never raises readiness past evidence fail.

**Wayfinder:** Neon Genie owns *what/why/user/boundary/proof*. Wayfinder owns *decomposition/milestones/status*.  
`product_intent_changes_require_neon_genie_review: true`

---

## Authority & safety

**May:** research, infer, generate, compare, score, model, audit, specify, route, draft, recommend.

**May not** (without explicit downstream auth): spend, submit, contact, publish, modify repos, irreversible execute, promote to canon, present forecasts as facts, mutate runtime state.

`manifest.json` → `"authority": "advisory_only"`

---

## Repository layout

```text
Neon-Genie-Hermes/          ← skill root (install this tree)
├── SKILL.md                # Hermes operating contract
├── install.sh
├── scripts/neon_genie.py   # do <job>
├── profiles/  schemas/  references/  templates/
├── examples/               # briefs + gallery
├── evals/                  # gate fixtures + prose transcripts
└── docs/                   # DEMO, PREMIERE, ROADMAP
```

| Doc | Purpose |
|-----|---------|
| [QUICKSTART.md](./QUICKSTART.md) | Short install + prompts |
| [docs/DEMO.md](./docs/DEMO.md) | 10-minute path |
| [docs/PREMIERE.md](./docs/PREMIERE.md) | Why this skill vs idea agents |
| [docs/ROADMAP.md](./docs/ROADMAP.md) | History + maintenance |
| [CHANGELOG.md](./CHANGELOG.md) | Releases |

---

## Versioning

| Field | Value |
|-------|-------|
| Skill | `neon-genie` |
| Version | **3.16.0** |
| Authority | `advisory_only` |
| Research | proactive (opt out: `research.enabled=false`) |

Source of truth: [`VERSION`](./VERSION), [`manifest.json`](./manifest.json), [`SKILL.md`](./SKILL.md) frontmatter.

---

## License

**MIT** — Copyright (c) 2026 Applied Alchemy Labs / Zero State. See [`LICENSE`](./LICENSE).

**Maintainers:** [Applied Alchemy Labs / @scrimshawlife-ctrl](https://github.com/scrimshawlife-ctrl)

---

<div align="center">
<sub>Neon Genie v3.16.0 · OPEN → ALIGN → ASCEND → CLEAR → SEAL · advisory only</sub>
</div>
