# Neon Genie Hermes Wizard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `do wizard` for Neon Genie — resolve-path plan resolver (default print-only) plus quick onboarding path (doctor + sample product-audit) targeting **3.26.0**.

**Architecture:** Stdlib module `scripts/wizard.py` validates answers, merges presets, builds `neon-genie-wizard-plan.v1`, and optionally executes via existing job scripts. Thin registration in `scripts/neon_genie.py`. Product judgment stays in Hermes + `SKILL.md`.

**Tech Stack:** Python ≥ 3.10, stdlib only. Existing `do` jobs (`doctor`, `run`, `route`, `recipe`, `check`, `privacy`). Tests: pytest-style functions under `scripts/test_wizard.py` (match `scripts/test_operator_surface.py`). Spec: `docs/superpowers/specs/2026-08-08-neon-genie-hermes-wizard-design.md`.

## Global Constraints

- Stdlib only — no new third-party dependencies.
- Packaging only — never invent opportunities, buyers, capital, or skills.
- Default is **print-only** on resolve path; `--run` is explicit.
- Quick path: `--auto` defaults to run; non-TTY without `--auto`/`--print-only`/`--run` → exit 2.
- Unknown answer keys rejected (strict).
- Recipe names only from `recipe_run.RECIPES`.
- Never write learning ledger; never mutate skill tree; writes only under `--out` when running.
- Version bump to **3.26.0** in final docs/version task.
- Authority always `advisory_only` on plans.

## File map

| File | Responsibility |
|------|----------------|
| `scripts/wizard.py` | Answers merge/validate, plan resolve, interactive prompts, format, execute, CLI main |
| `scripts/neon_genie.py` | Register `wizard` in INTENTS + EVERYDAY; optional alias |
| `schemas/wizard-answers.v1.schema.json` | JSON Schema for answers contract |
| `scripts/test_wizard.py` | Unit + CLI subprocess tests |
| `references/wizard.md` | Hermes guided interview notes |
| `SKILL.md`, `QUICKSTART.md`, `README.md`, `CHANGELOG.md` | Discoverability |
| `VERSION`, distribution spine, hub mirrors | 3.26.0 parity |

---

### Task 1: Core resolve library + unit tests (TDD)

**Files:**
- Create: `scripts/wizard.py`
- Create: `scripts/test_wizard.py`
- Create: `schemas/wizard-answers.v1.schema.json`

**Interfaces:**
- `ANSWERS_SCHEMA = "neon-genie-wizard-answers.v1"`
- `PLAN_SCHEMA = "neon-genie-wizard-plan.v1"`
- `INTENTS`, `PRESETS`, `PATHS`, `ALLOWED_KEYS`
- `class WizardError(Exception)` with `.message` and optional `.missing`
- `def load_answers(path_or_dash: str) -> dict`
- `def merge_preset(preset: str | None, answers: dict | None) -> dict`
- `def known_recipes() -> frozenset[str]`
- `def validate_answers(answers: dict) -> dict`
- `def resolve_plan(answers: dict, *, run: bool = False) -> dict`
- `def format_plan_human(plan: dict, skill_root_hint: str = "scripts/neon_genie.py") -> str`
- `def format_plan_json(plan: dict) -> str`
- `def execute_plan(plan: dict, *, runner=None) -> int`
- `def main(argv: list[str] | None = None) -> int`

- [ ] **Step 1: Write failing tests** in `scripts/test_wizard.py`
- [ ] **Step 2: Implement `wizard.py` + schema**
- [ ] **Step 3: Tests pass**
- [ ] **Step 4: Commit**

### Task 2: Wire CLI + quick path execution

**Files:**
- Modify: `scripts/neon_genie.py` — INTENTS, EVERYDAY, ALIASES, help text
- Modify: `scripts/wizard.py` — argparse CLI, interactive, quick path defaults

- [ ] **Step 1: Register wizard job**
- [ ] **Step 2: CLI subprocess tests** (`do wizard --preset product-audit --print-only --json`)
- [ ] **Step 3: Quick path tests** (print-only steps; auto with mocked runner optional)
- [ ] **Step 4: Commit**

### Task 3: Docs, version 3.26.0, distribution

**Files:**
- Create: `references/wizard.md`
- Modify: `SKILL.md`, `QUICKSTART.md`, `README.md`, `CHANGELOG.md`, `VERSION`
- Modify: `distribution.yaml` if needed; run `distribution_spine.py write`
- Sync hub package if `sync_skill_package.sh` is the path

- [ ] **Step 1: Docs + VERSION**
- [ ] **Step 2: dist write + check**
- [ ] **Step 3: Commit**

### Task 4: Verification

- [ ] `python -m pytest scripts/test_wizard.py -v` (or `python scripts/test_wizard.py` if plain assert runner)
- [ ] `python scripts/neon_genie.py do check`
- [ ] `python scripts/neon_genie.py do wizard --path quick --auto --out /tmp/ng-wizard-quick` (or print-only if doctor too heavy in CI)
- [ ] Final commit if any fixups
