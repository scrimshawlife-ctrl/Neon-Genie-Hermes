<div align="center">

# Neon Genie

### Governed opportunity & product intelligence for Hermes

[![Version](https://img.shields.io/badge/version-3.23.0-7c3aed?style=for-the-badge)](./manifest.json)
[![Hermes Skill Evals](https://img.shields.io/github/actions/workflow/status/scrimshawlife-ctrl/Neon-Genie-Hermes/hermes-evals.yml?branch=main&label=hermes-evals&style=for-the-badge)](./.github/workflows/hermes-evals.yml)
[![Authority](https://img.shields.io/badge/authority-advisory%20only-0ea5e9?style=for-the-badge)](#authority--safety)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge)](./LICENSE)

<img src="docs/assets/hero.jpg" alt="Neon Genie — luminous lamp on a dark network grid" width="920" />

**Turn weak signals and blocked transitions into evidence-bound, testable product and opportunity packets — without inventing facts or granting spend/execute rights.**

[How to use](#how-to-use) · [Install](#installation) · [Commands](#command-cheat-sheet) · [Demo](./docs/DEMO.md) · [Premiere](./docs/PREMIERE.md) · [Contributing](./CONTRIBUTING.md)

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

There are two ways to use Neon Genie. **Most people should use Hermes chat.**  
The command line is for install checks, sample runs, and automation.

### 1. Install (once)

**Option A — Hermes Skills Hub (recommended)**

```bash
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```

Then reload or restart Hermes so it picks up the skill.

**Option B — Clone this repo**

```bash
git clone https://github.com/scrimshawlife-ctrl/Neon-Genie-Hermes.git
cd Neon-Genie-Hermes
./install.sh
# installs into ~/.hermes/skills/neon-genie
```

Check that the install works:

```bash
python ~/.hermes/skills/neon-genie/scripts/neon_genie.py do doctor
# or, from a clone:
python scripts/neon_genie.py do doctor
```

You want a final line that says the doctor passed. If it fails, the skill files are incomplete or the path is wrong.

More install detail: [Installation](#installation) · [docs/HERMES_DISTRIBUTION.md](./docs/HERMES_DISTRIBUTION.md)

---

### 2. Everyday use in Hermes (plain English)

This is the normal path.

1. **Start Hermes** (desktop or CLI) with Neon Genie installed.
2. **Ask for Neon Genie** by name, or describe a product/opportunity problem so the skill loads  
   (triggers include: product audit, opportunity mining, zero option, wayfinder handoff).
3. **Say what you need in ordinary language.** Include:
   - Who is stuck (person, team, customer)
   - What “done” looks like
   - What you already know (links, notes, constraints)
   - What you do **not** want (e.g. do not invent a buyer; do not change the repo)
4. **Let Hermes work through the steps.** Neon Genie always runs in order:  
   understand request → gather evidence → build the answer → check gates → seal outputs.
5. **Treat everything as a draft.** Neon Genie can recommend. It cannot spend money, publish, email people, or change git history.

**Example things to say**

```text
Use Neon Genie. We have an audio continuity tool but no defined buyer.
What should we charge? Research public competitors if you can. If you need
private facts (who pays, who authorizes budget), ask me with a DataRequest
instead of inventing. Label every important claim. Do not modify the repo.
```

```text
Use Neon Genie zero-option: I need first cash in 7 days with no capital.
Only use skills and access I explicitly declare. Do not invent customers,
credentials, or money. If you cannot compute an answer, say NOT_COMPUTABLE.
```

```text
Use Neon Genie offline: research.enabled=false
Only use what I paste and what is already in this workspace.
```

**What good output looks like**

- Claims labeled **OBSERVED** (with a source), **INFERRED**, **SPECULATIVE**, or **NOT_COMPUTABLE**
- Missing private facts asked for as a **DataRequest**, not filled in with guesses
- Clear product or opportunity packet(s) and a short run summary
- Still **advisory only** — no “I will merge the PR” / “I will charge the card”

**What to do with the files**

If a packaging run wrote a folder (see below), open **`run-envelope.json` first**.  
That file points at the main packet, the receipt, and any open data requests.

More prompt patterns: [QUICKSTART.md](./QUICKSTART.md) · Worked chat examples: [evals/transcripts/](./evals/transcripts/)

---

### 3. Command-line helpers (optional)

Use these when you want a **sample run on disk**, CI checks, or automation.  
This CLI does **not** invent product strategy by itself — it packages, validates, and runs examples.

**One pattern**

```text
python scripts/neon_genie.py do <job> [options]
```

From a clone, `cd` into the repo first. From a Hub install, use the full path under `~/.hermes/skills/neon-genie/`.

| In plain English | Command |
|------------------|---------|
| Check the install | `do doctor` |
| Run a named sample end-to-end | `do run --recipe product-audit --out out/neon-genie/demo` |
| Run from a short YAML brief | `do run --brief examples/product-audit.brief.yaml --out out/neon-genie/demo` |
| See what the skill can do (JSON) | `do capabilities --json` |
| List sample recipes | `do recipe --list` |
| Suggest profiles from text | `do route --text "first cash zero capital" --json` |
| Check a packet or envelope file | `do validate --packet path/to/file.json --type envelope` |
| Record a real outcome later | `do learn --class proof_obtained --summary "…" --envelope out/…/run-envelope.json` |

```bash
# Typical first CLI session (from a clone)
python scripts/neon_genie.py help
python scripts/neon_genie.py do doctor
python scripts/neon_genie.py do run --recipe product-audit --out out/neon-genie/demo
# then open: out/neon-genie/demo/run-envelope.json
```

**After a packaging run, look for**

| File | Meaning |
|------|---------|
| `run-envelope.json` | **Start here** — index of the whole run |
| `run-receipt.json` | Status, profiles, open data requests |
| `*-packet*.json` / handoff stubs | Draft product/opportunity content |
| `HERMES_NEXT.md` | Reminder that real judgment is in Hermes + `SKILL.md` |

Full command list: [Command cheat sheet](#command-cheat-sheet) · 10-minute walkthrough: [docs/DEMO.md](./docs/DEMO.md)

---

### 4. Rules of the road (so you are not surprised)

| Rule | Meaning |
|------|---------|
| Evidence-bound | Important claims must be labeled; no silent guessing |
| Find or request | Public facts → research if tools allow; private facts → ask you; else **NOT_COMPUTABLE** |
| Advisory only | Neon Genie will not spend, publish, contact targets, or change your repo |
| Smallest profiles | Only loads the skill “modes” the job needs (`core` is always on) |
| Wayfinder handoff | Neon Genie decides *what* and *why*; engineering tools decide *how to build* — product intent stays frozen unless Neon Genie reviews a change |

---

## Worked example (before → after)

**Input**

> “We have an audio continuity tool but no defined buyer.”

**What Neon Genie does**

| Step | Result |
|------|--------|
| OPEN | Product category known; buyer missing |
| ALIGN | Public research allowed; **DataRequest** for private buyer/budget authority |
| ASCEND | Claims labeled; firm price is `NOT_COMPUTABLE` without buyer |
| CLEAR | Gate Q (private gap) blocks promotion past CONCEPTUAL |
| SEAL | Packets + receipt + **`run-envelope.json`** — still `advisory_only` |

**You should see**

- Product boundary clarified (draft)  
- Buyer marked **NOT_COMPUTABLE** until evidence  
- Open `DataRequest` (blocks promotion)  
- Testable diagnostic offer only after roles exist  
- Wayfinder handoff **blocked** until buyer evidence (or explicit waive)  
- **No** repo mutation, spend, or publish  

Reproduce packaging scaffold:

```bash
python scripts/neon_genie.py do run --recipe commercial --out out/neon-genie/audio-buyer
# or full Hermes session using the prompt above
```

---

## Installation (detail)

### Hermes Skills Hub (recommended)

```bash
hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
```

Optional: inspect first, or add the whole tap:

```bash
hermes skills inspect scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie
hermes skills tap add scrimshawlife-ctrl/Neon-Genie-Hermes
```

Reload or restart Hermes after install.

### Clone + local install

```bash
git clone https://github.com/scrimshawlife-ctrl/Neon-Genie-Hermes.git
cd Neon-Genie-Hermes
./install.sh
# → ~/.hermes/skills/neon-genie

python scripts/neon_genie.py do doctor
```

### Notes

- You need Hermes (or another agent that loads this skill folder).  
- No external knowledge base is required just to load the skill.  
- Research uses tools Hermes already has (search, fetch, etc.) when available.  
- For offline-only work, say `research.enabled=false`.  
- Sibling skill: [Kubrick](https://github.com/scrimshawlife-ctrl/Kubrick) for cinematic work — not required here.  
- Catalog / tap docs: [docs/HERMES_DISTRIBUTION.md](./docs/HERMES_DISTRIBUTION.md) · [docs/CATALOG.md](./docs/CATALOG.md)

---

## Command cheat sheet

Run from a **clone** of this repo (or prefix with `~/.hermes/skills/neon-genie/` after Hub install).

```bash
# Check install
python scripts/neon_genie.py do doctor

# Sample end-to-end runs (write files under out/)
python scripts/neon_genie.py do run --recipe product-audit --out out/neon-genie/run1
python scripts/neon_genie.py do run --brief examples/zero-option.brief.yaml --out out/neon-genie/zero
# Open run-envelope.json in that folder first

# What can this skill do? (for agents / orchestrators)
python scripts/neon_genie.py do capabilities --json

# Suggest profiles from free text
python scripts/neon_genie.py do route --text "first cash zero capital" --json

# Check a finished envelope
python scripts/neon_genie.py do validate --packet out/neon-genie/run1/run-envelope.json --type envelope

# Quality gates (CI-style)
python scripts/neon_genie.py do check
python scripts/neon_genie.py do eval
python scripts/neon_genie.py do behavioral --suite

# After a real-world outcome (local note only — never auto-updates the skill)
python scripts/neon_genie.py do learn --class proof_obtained \
  --summary "first paid diagnostic booked" \
  --envelope out/neon-genie/run1/run-envelope.json \
  --ledger out/neon-genie/learning-ledger.jsonl

# Maintainers: before tagging a release
python scripts/neon_genie.py do dist verify
python scripts/neon_genie.py do release-check
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

## For agents

| Goal | Command |
|------|---------|
| Discover surface | `do capabilities --json` |
| Verify install | `do doctor` |
| Packaging workspace | `do run --brief …` or `--recipe …` |
| Resume a run | open `run-envelope.json` first |
| CI | `do eval` · `do behavioral` · `do dist verify` |
| Ship a version | `do release-check` → tag `vX.Y.Z` → Release workflow |

**Rules:** no model-prior as `OBSERVED`; public→research / private→`DataRequest`; no spend/publish/mutate; Wayfinder must not rewrite product intent; `TESTABLE`+ needs `completion_proof`.

Contract: [`references/hermes-runtime-contract.md`](./references/hermes-runtime-contract.md) · Schemas: [`references/schema-versioning.md`](./references/schema-versioning.md)

### How it works (short)

**OPEN → ALIGN → ASCEND → CLEAR → SEAL.** Missing data: **find → request → NOT_COMPUTABLE**.

Neon Genie owns *what/why/user/boundary/proof*. Wayfinder owns *decomposition/milestones/status*  
(`product_intent_changes_require_neon_genie_review: true`).

**Authority:** `advisory_only` — may research/draft/recommend; may not spend, publish, contact, or mutate repos.

---

## Repository layout

```text
Neon-Genie-Hermes/          ← skill root (also full install tree)
├── SKILL.md                # operating contract
├── distribution.yaml       # Hub mirror single source
├── scripts/neon_genie.py   # do <job>
├── skills/neon-genie/      # tap / Hub package (generated)
├── profiles/ schemas/ references/ examples/ evals/
├── docs/ adr/ GOVERNANCE   # design + process
└── .github/                # CI, release, issue templates
```

| Doc | Purpose |
|-----|---------|
| [QUICKSTART.md](./QUICKSTART.md) | Short install + prompts |
| [docs/DEMO.md](./docs/DEMO.md) | 10-minute path |
| [docs/PREMIERE.md](./docs/PREMIERE.md) | Why this skill vs idea agents |
| [docs/ROADMAP.md](./docs/ROADMAP.md) | History + maintenance |
| [docs/adr/](./docs/adr/) | Architecture decisions |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Dev + release process |
| [docs/GOVERNANCE.md](./docs/GOVERNANCE.md) | Branch protection + releases |
| [CHANGELOG.md](./CHANGELOG.md) | Releases |

---

## Versioning

| Field | Value |
|-------|-------|
| Skill | `neon-genie` |
| Version | **3.23.0** |
| Authority | `advisory_only` |
| Research | proactive (opt out: `research.enabled=false`) |

Source of truth: [`VERSION`](./VERSION), [`manifest.json`](./manifest.json), [`SKILL.md`](./SKILL.md) frontmatter.

---

## License

**MIT** — Copyright (c) 2026 Applied Alchemy Labs / Zero State. See [`LICENSE`](./LICENSE).

**Maintainers:** [Applied Alchemy Labs / @scrimshawlife-ctrl](https://github.com/scrimshawlife-ctrl)

---

<div align="center">
<sub>Neon Genie v3.23.0 · OPEN → ALIGN → ASCEND → CLEAR → SEAL · advisory only</sub>
</div>
