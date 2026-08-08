# Neon Genie — Hermes Wizard Design

**Status:** Draft (awaiting operator review)  
**Date:** 2026-08-08  
**Version target:** 3.26.0 (minor — new public CLI surface)  
**Hosts:** Hermes (CLI, gateway, Desktop), OpenClaw  
**Repository:** NeonGenie (`neon-genie` skill)

## Intent

Add a guided **wizard** that collapses Neon Genie’s packaging decision tree (`doctor` / `route` / `run` / `recipe` / `check` / `privacy`) into a single, testable path so Hermes agents (and humans) do not freestyle argv, invent recipe names, or skip install smoke.

The wizard is a **hybrid of Orchestra Approach A + Hyperlex quick onboarding**:

1. **Default path (`resolve`)** — thin plan resolver: answers / preset → argv plan for existing packaging jobs. Product judgment stays in Hermes + `SKILL.md`.
2. **Quick path (`quick`)** — fixed onboarding sequence: doctor → sample product-audit package → HERMES next-steps coach. For first-time operators after install.

Interactive TTY when answers are incomplete **and** stdin is a TTY. Fully non-interactive for agents via `--answers` / `--preset` / `--path quick --auto`.

## Non-goals (YAGNI)

- Reimplementing OPEN → ALIGN → ASCEND → CLEAR → SEAL product judgment in Python
- Inventing opportunities, buyers, capital, skills, or market facts
- Native Electron multi-step form inside Hermes Desktop UI
- Writing free-form opportunity packets (only packaging workspace + envelope via existing `do run` / recipes)
- Auto-promoting learning ledger entries
- Network install / remote skill fetch
- Session file step-runner (`--session-new` / `--next`) — deferred; chat + answers JSON is Desktop-safe enough
- Auto-running host research tools (research remains Hermes-side per SKILL.md)

## Context

Neon Genie 3.25.0 already ships:

| Everyday job | Script | Role |
|--------------|--------|------|
| `doctor` | `doctor.py` | Full install smoke |
| `check` | `validate_hermes_skill.py` | Skill integrity |
| `run` | `run_job.py` | Brief/recipe → workspace + envelope |
| `recipe` | `recipe_run.py` | Named example end-to-end |
| `route` | `route_profiles.py` | Profile suggestion from text/brief |
| `privacy` | `privacy_diagnostics.py` | Resolved privacy boundary |
| `validate` / `receipt` / `envelope` / `learn` / … | various | CI / outcomes |

CLI shape today:

```text
python scripts/neon_genie.py do <job> [options]
```

Hermes Desktop uses the **same agent, skills, and tools** as CLI/gateway. Skill work runs via tool/terminal invocation — **not** a dedicated NeonGenie Desktop panel. Interactive stdin wizards are unreliable on the agent tool path; **chat + non-interactive CLI** is the Desktop-safe contract.

## Purpose & CLI surface

```text
python scripts/neon_genie.py do wizard [options]
# aliases (optional, registered like existing product-audit → recipe):
#   wizard → do wizard
```

| Mode | Flags | Behavior |
|------|--------|----------|
| Path select | `--path resolve` (default) \| `--path quick` | Resolve plan vs onboarding sequence |
| Interactive | default when TTY and answers incomplete | Numbered prompts; safe defaults |
| Non-interactive | `--answers PATH\|-` and/or `--preset NAME` | Fully determined; exit non-zero on invalid |
| Quick auto | `--path quick --auto` | No prompts; doctor + sample package with defaults |
| Plan only | `--print-only` (**default** on resolve path) | Print resolved plan + exact argv; no mutation |
| Execute | `--run` | Dispatch resolved job(s) via existing `do` scripts |
| Machine out | `--json` | Emit `neon-genie-wizard-plan.v1` JSON on stdout |
| Presets | `--preset …` | Seed answers; overridable by `--answers` |

**Safety defaults:**

- Prefer `--print-only` on **resolve** path. `--run` is explicit.
- **Quick** path with `--run` (or `--auto`) may create under `--out` only (default `out/neon-genie/wizard-quick/`). Never mutates the skill tree, repos, or learning ledger.
- Never claims product judgment, OBSERVED facts, or execution authority.
- Non-TTY without enough answers to resolve → exit `2` with guidance to use `--answers` / chat (Desktop-safe).
- Unknown answer keys → reject (strict).

## Path A — Resolve (default)

Wizard resolves to **one primary packaging job** per invocation (v1). Multi-step argv lists are reserved for the quick path only.

```text
1. Intent
   doctor | check | privacy | route | run | recipe

2. route
   → text (required unless brief)
   → brief path (optional; exclusive with free-text when both would set)
   → --json always implied in plan for agents when answers.json_out true (default true for route)

3. run
   → recipe OR brief OR text (at least one)
   → out (recommended; default out/neon-genie/wizard-run)
   → optional packet + type + validate

4. recipe
   → name (required; from RECIPES registry)
   → out (optional)

5. doctor | check | privacy
   → no extra fields (privacy plan includes --json)

6. Resolve → plan (argv + rationale + safety notes + hermes_coach)

7. If --run → subprocess existing job script (same as neon_genie.py do)
```

### Presets (resolve path)

| Preset | Intent | Seed defaults |
|--------|--------|----------------|
| `doctor` | doctor | — |
| `check` | check | — |
| `privacy` | privacy | — |
| `product-audit` | run | `recipe=product-audit`, `out=out/neon-genie/wizard-product-audit` |
| `zero-option` | run | `recipe=zero-option`, `out=out/neon-genie/wizard-zero-option` |
| `opportunity` | run | `recipe=opportunity`, `out=out/neon-genie/wizard-opportunity` |
| `audit` | run | `recipe=audit`, `out=out/neon-genie/wizard-audit` |
| `route-sample` | route | `text="zero capital first cash app idea between jobs"` |
| `offline-scaffold` | run | `recipe=product-audit`, `out=out/neon-genie/wizard-offline`, coach notes that Hermes must set `research.enabled=false` in chat/brief (packaging CLI does not invent offline research behavior beyond existing briefs) |

Recipe names must match `recipe_run.RECIPES` keys (today: `agentic`, `audit`, `capital-sprint`, `commercial`, `evidence`, `fragmentation`, `memetic`, `opportunity`, `product-audit`, `zero-option`, `zero-option-executable`).

## Path B — Quick onboarding

Fixed sequence for new installs. Not free-form intent selection.

```text
1. env_intro     — skill root, HERMES_SKILL_DIR coach, authority reminder
2. doctor        — run doctor (or plan doctor argv if --print-only)
3. sample_run    — do run --recipe product-audit --out <out>
4. handoff       — point at run-envelope.json + OPEN→ALIGN→… + advisory only
```

| Flag | Behavior |
|------|----------|
| `--path quick` | Select onboarding sequence |
| `--auto` | Non-interactive defaults (implies enough answers; no TTY needed) |
| `--out DIR` | Sample package root (default `out/neon-genie/wizard-quick`) |
| `--print-only` | Print ordered argv list only; do not execute doctor/run |
| `--run` | Execute steps (doctor then sample run). With `--auto`, default is **run** (onboarding is useless as print-only for first-time humans; agents may still pass `--print-only`) |

**Quick path defaults when both `--print-only` and `--run` omitted:**

- TTY human → treat as `--run` (onboarding expects smoke + sample)
- Non-TTY / agent without `--auto` → exit `2` asking for `--auto` or `--print-only` or `--run`
- `--auto` without `--print-only` → `--run`

Rationale: onboarding that only prints argv fails the “after install, am I healthy?” goal; resolve path keeps print-only as default to match Orchestra safety.

## Answers schema (`neon-genie-wizard-answers.v1`)

```json
{
  "schema": "neon-genie-wizard-answers.v1",
  "path": "resolve",
  "intent": "run",
  "recipe": "product-audit",
  "brief": null,
  "text": null,
  "out": "out/neon-genie/wizard-product-audit",
  "packet": null,
  "packet_type": null,
  "validate_packet": false,
  "json_out": true,
  "recipe_name": null
}
```

| Field | Type | Notes |
|-------|------|--------|
| `schema` | string | Required; exact `neon-genie-wizard-answers.v1` |
| `path` | `resolve` \| `quick` | Default `resolve` |
| `intent` | enum | Required when `path=resolve` |
| `recipe` | string \| null | For `intent=run` |
| `recipe_name` | string \| null | For `intent=recipe` (alias of recipe name for recipe job) |
| `brief` | path string \| null | Existing brief YAML |
| `text` | string \| null | Free text for route or run auto-route |
| `out` | path string \| null | Output directory |
| `packet` | path string \| null | Optional external packet for run |
| `packet_type` | string \| null | Packet type for validate |
| `validate_packet` | bool | Default false |
| `json_out` | bool | Prefer `--json` on route/privacy plans |

### Validation rules

| Rule | Exit |
|------|------|
| Missing `schema` or wrong value | 2 |
| Unknown keys | 2 — **reject** (strict) |
| Unknown `path` / `intent` / recipe name | 2 |
| `path=resolve` missing `intent` | 2 |
| `intent=run` with none of recipe/brief/text | 2 |
| `intent=route` with neither text nor brief | 2 |
| `intent=recipe` without `recipe_name` (or `recipe`) | 2 |
| brief/packet path provided but not a file (on `--run` only) | 1 |
| Interactive on non-TTY without complete answers | 2 |

## Plan schema (`neon-genie-wizard-plan.v1`)

```json
{
  "schema": "neon-genie-wizard-plan.v1",
  "path": "resolve",
  "intent": "run",
  "job": "run",
  "argv": ["run", "--recipe", "product-audit", "--out", "out/neon-genie/wizard-product-audit"],
  "steps": null,
  "rationale": "Preset product-audit → packaging workspace via do run",
  "safety_notes": [
    "advisory_only",
    "packaging only — product judgment remains in Hermes + SKILL.md",
    "no spend / publish / repo mutation"
  ],
  "hermes_coach": [
    "Open Hermes with Neon Genie loaded",
    "OPEN → ALIGN → ASCEND → CLEAR → SEAL",
    "Do not invent buyers, capital, or skills the operator did not declare",
    "After packaging run: open run-envelope.json in the out dir"
  ],
  "authority": "advisory_only"
}
```

For **quick** path:

```json
{
  "schema": "neon-genie-wizard-plan.v1",
  "path": "quick",
  "intent": null,
  "job": "sequence",
  "argv": null,
  "steps": [
    {"id": "env_intro", "job": null, "argv": null, "summary": "..."},
    {"id": "doctor", "job": "doctor", "argv": ["doctor"]},
    {"id": "sample_run", "job": "run", "argv": ["run", "--recipe", "product-audit", "--out", "..."]},
    {"id": "handoff", "job": null, "argv": null, "summary": "..."}
  ],
  "rationale": "Week-one onboarding: smoke + sample package",
  "safety_notes": ["advisory_only", "writes only under --out"],
  "hermes_coach": ["..."],
  "authority": "advisory_only"
}
```

On-disk JSON Schema: `schemas/wizard-answers.v1.schema.json` (and optional `schemas/wizard-plan.v1.schema.json` if we validate plan in tests).

## Hermes agent protocol

When the operator is new, unsure which packaging job to run, or says “wizard” / “guide me” / “walk me through”:

1. Prefer `do wizard` over freestyling `do run` flags.
2. **Chat-driven Q&A** (Desktop-safe): ask only missing fields; merge into answers JSON; call:

   ```bash
   python scripts/neon_genie.py do wizard --answers answers.json --print-only --json
   # when operator confirms:
   python scripts/neon_genie.py do wizard --answers answers.json --run
   ```

3. **New install / “is this working?”** →

   ```bash
   python scripts/neon_genie.py do wizard --path quick --auto
   ```

4. After packaging succeeds, **resume product judgment in chat** (OPEN→SEAL). Do not treat envelope as execution authority.
5. Never invent resources; never auto-`learn` from wizard.

Document in `SKILL.md` (Packaging CLI + Prefer the wizard), `QUICKSTART.md`, and `references/wizard.md` (load on demand while guiding).

## Architecture

```text
neon_genie.py do wizard
        │
        ▼
 scripts/wizard.py          # stdlib: answers, presets, validate, resolve, interactive, format
        │
        ├── print-only → human text or --json plan
        └── --run → neon_genie run_script(INTENTS[job], argv_tail)
                    (reuse existing job scripts; no reimplementation)
```

| Module | Responsibility |
|--------|----------------|
| `scripts/wizard.py` | Core library + CLI entry for argparse when invoked as script |
| `scripts/neon_genie.py` | Register `wizard` in `INTENTS` / EVERYDAY; optional alias |
| `schemas/wizard-answers.v1.schema.json` | Contract for answers |
| `tests/test_wizard.py` | Unit + subprocess CLI tests |
| `references/wizard.md` | Hermes guided interview notes |
| `SKILL.md`, `QUICKSTART.md`, `README.md`, `CHANGELOG.md` | Discoverability |
| `VERSION` → `3.26.0` | Minor bump when feature ships |

**Dependencies:** Python 3.10+ stdlib only (match repo). Recipe registry read from `recipe_run.RECIPES` (import) so wizard cannot invent recipe names.

## Interactive prompts (TTY, resolve path)

Minimal ordered prompts:

1. Intent (doctor / check / privacy / route / run / recipe) — default `run`
2. Branch fields as required
3. `out` with default
4. Confirm print-only vs run (default print-only)

Quick path interactive (only if not `--auto` and TTY):

1. Confirm out dir (default)
2. Confirm run doctor + sample (Y/n)

## Error codes

| Code | Meaning |
|------|---------|
| 0 | Success (plan printed and/or jobs ok) |
| 1 | Packaging / doctor / recipe execution failure |
| 2 | Usage / validation / non-TTY incomplete answers |

## Testing

`tests/test_wizard.py` (unittest or pytest — match repo: existing scripts use pytest-style files under `scripts/test_*.py` **and** may use unittest; prefer **pytest** if already used, else unittest).

Minimum cases:

1. Preset `product-audit` → plan argv contains `run --recipe product-audit`
2. Preset `doctor` → plan job doctor
3. Resolve `route` missing text/brief → exit 2 / WizardError
4. Unknown key → reject
5. Unknown recipe → reject
6. Quick `--print-only` → four steps with doctor + product-audit
7. Quick `--auto --run` (tmpdir out) → doctor ok + envelope exists (or soft-skip if doctor too heavy — prefer subprocess doctor with reasonable timeout; if CI cost high, mock doctor step with injectable runner)
8. Non-TTY incomplete → exit 2
9. `--json` plan has `schema: neon-genie-wizard-plan.v1` and `authority: advisory_only`

**Injectable runner** for unit tests: `resolve_plan` pure; `execute_plan(plan, runner=subprocess)` so doctor/run can be mocked.

## Distribution / hub

After implementation:

- Add `scripts/wizard.py`, `references/wizard.md`, schemas to `distribution.yaml` if hub-shipped
- Run `python scripts/distribution_spine.py write` so `SKILL.md` hub support file block updates
- `do check` / `do doctor` still pass
- Mirror install under `skills/neon-genie/` via existing `sync_skill_package.sh` if that is the release path

## Versioning & changelog

- Bump `VERSION` and frontmatter to **3.26.0**
- CHANGELOG entry under Added: Hermes packaging wizard (`do wizard`) with resolve + quick paths

## Success criteria

- [ ] Hermes agent can package a product-audit workspace with only answers JSON + `do wizard --run`
- [ ] New operator can run `do wizard --path quick --auto` after install and get doctor + sample envelope
- [ ] Default resolve path never mutates disk without `--run`
- [ ] No product judgment, invented resources, or ledger writes from wizard
- [ ] Tests green; `do check` green; docs mention wizard in SKILL + QUICKSTART

## Open questions (resolved in this draft)

| Q | Decision |
|---|----------|
| Primary purpose | Route + package (Approach A) |
| Onboarding | Hybrid: `--path quick` |
| Product brain in wizard | No |
| Session step-runner | Deferred |
| Default print-only | Yes on resolve; quick defaults to run when `--auto` or TTY |

## References

- Sibling patterns: Orchestra wizard design (`2026-08-08-orchestra-hermes-wizard-design.md`), Hyperlex week-one wizard, Sigil-Forge step runner
- Local: `scripts/neon_genie.py`, `scripts/run_job.py`, `scripts/route_profiles.py`, `scripts/recipe_run.py`, `SKILL.md` packaging CLI section
