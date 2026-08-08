# Neon Genie Ops Shell (Wave 1) — Design Spec

**Date:** 2026-07-30  
**Status:** Approved for implementation planning  
**Repo:** [NeonGenie](https://github.com/scrimshawlife-ctrl/NeonGenie)  
**Reference architecture (patterns only):** [Kubrick](https://github.com/scrimshawlife-ctrl/Kubrick)  
**Skill version target:** 3.2.0  

---

## 1. Intent

Make **Neon Genie** a Hermes skill that shares **Kubrick’s skill operating system** (layout, install, runtime contract, smoke validation, docs ops, examples/evals skeleton) while remaining a **separate skill with a separate mission**.

| Skill | Mission |
|-------|---------|
| **Neon Genie** | Governed invention, product architecture, opportunity intelligence, commercial simulation, Wayfinder handoff |
| **Kubrick** | Symbolic cinematic narrative engineering, motif/storyboard, visual QA |

They are **sibling skills**. No shared runtime library, no monorepo merge, no domain content cross-import.

---

## 2. Constraints (non-negotiable)

1. **Domain isolation** — No cinematic runes, motif graphs, or Forge-first concepts in Neon Genie. No opportunity packets or Zero-Option doctrine in Kubrick.
2. **Pattern twin, not code twin** — Mirror *kinds* of files and contracts, not Kubrick’s scripts or corpus.
3. **Prose-first** — Full OPEN → ALIGN → ASCEND → CLEAR → SEAL advisory work must work without Python.
4. **Authority** — Remain `advisory_only`. No spend, publish, repo mutation, canon promotion, or runtime state mutation without explicit downstream auth.
5. **No premature abstraction** — Do not extract a shared `hermes-skill-scaffold` in Wave 1 (optional later after Wave 2).

---

## 3. Multi-wave roadmap (full arc; implement Wave 1 only next)

| Wave | Name | Outcome |
|------|------|---------|
| **1** | Ops shell | Installable skill root, runtime contract, VERSION/CHANGELOG/QUICKSTART, install.sh, smoke validator, examples + evals skeleton, path flatten |
| **2** | Domain depth | Thicken profiles; fill missing packet schemas; richer golden/eval cases; anti-overclaim references |
| **3** | Thin operator surface | Optional `neon-genie do check\|validate\|route\|receipt` — packaging only, no product brain in Python |
| **4** | Release maturity | CI evals, release checklist, default install as peer of Kubrick in operator environments |

This document specifies **Wave 1 only**. Waves 2–4 are documented for continuity, not as Wave 1 scope.

---

## 4. Goals and non-goals (Wave 1)

### Goals

- Neon Genie installs as a **self-contained Hermes skill root** (peer of Kubrick).
- Operators who know Kubrick’s layout can navigate Neon without a second packaging model.
- Deterministic surface is **skill integrity smoke only**.
- Existing domain doctrine (profiles, gates, claim labels, research mode, packet schemas) is preserved; only packaging and paths change.
- Multi-wave roadmap is written so later work does not collapse into Wave 1.

### Non-goals

- Opportunity/product reasoning engines in Python.
- Full Kubrick-style intent router (`do compile|retrieve|…`).
- Thickening profile contracts beyond path fixes.
- Shared packages with Kubrick.
- OpenClaw dual packaging (out of scope unless later explicitly requested).

---

## 5. Target repository / skill layout

After Wave 1, **git repo root = Hermes skill root**:

```text
Neon-Genie-Hermes/
├── SKILL.md
├── manifest.json
├── VERSION
├── CHANGELOG.md
├── QUICKSTART.md
├── README.md
├── LICENSE
├── install.sh
├── profiles/                 # 11 profile contracts
├── schemas/                  # packet JSON schemas
├── references/
│   ├── hermes-runtime-contract.md
│   ├── CAPABILITY_MAP.md
│   └── GOLDEN_TESTS.md
├── templates/
│   └── request.yaml
├── examples/
│   ├── README.md
│   ├── product-audit.brief.yaml
│   └── zero-option.brief.yaml
├── evals/
│   ├── rubric.md
│   └── cases/                # migrated golden fixtures
├── scripts/
│   └── validate_hermes_skill.py
├── docs/
│   ├── README.md
│   ├── ROADMAP.md
│   ├── assets/               # hero + social preview
│   └── superpowers/
│       └── specs/
│           └── 2026-07-30-neon-genie-ops-shell-design.md
└── (no nested neon-genie/ package)
```

### Migration from current layout

| Before | After |
|--------|--------|
| `neon-genie/SKILL.md` | `SKILL.md` |
| `neon-genie/manifest.json` | `manifest.json` |
| `neon-genie/profiles/*` | `profiles/*` |
| `neon-genie/schemas/*` | `schemas/*` |
| `neon-genie/references/*` | `references/*` |
| `neon-genie/templates/*` | `templates/*` |
| `neon-genie/tests/golden/*` | `evals/cases/*` |
| `neon-genie/README.md` | Fold into root README + QUICKSTART; remove nested package README or replace with pointer if briefly needed during transition |
| Nested `neon-genie/` directory | **Removed** after move |

**Compat note (docs only):** Old instructions `cp -R neon-genie …` are obsolete. New: `./install.sh` or copy **repository root** into Hermes skills.

---

## 6. Install

### `install.sh`

Behavior (aligned with Kubrick’s installer pattern, Neon-specific paths):

1. Default destination: `$HOME/.hermes/skills/neon-genie`
2. If destination exists: back up to `neon-genie.bak`, then replace
3. Copy the skill tree (repo root contents appropriate for install; exclude `.git` if copying from a live checkout)
4. `chmod +x scripts/*.py` when present
5. Print location + “restart/reload Hermes” next steps

Optional category subdirectory (e.g. `research/`) is **not required** in Wave 1. Default install is **flat skill root**, matching Kubrick’s primary path.

### Hermes discoverability

`SKILL.md` frontmatter must support Hermes loading:

- Required: `name`, `description`, `version`, `author` (and existing `license` if present)
- Recommended packaging fields: `platforms`, `tags`, domain-specific `triggers`
- `name` must be `neon-genie`
- `version` must match `VERSION` and `manifest.json`

Triggers are **Neon-domain only** (examples): product audit, opportunity mining, zero option, fragmentation, wayfinder handoff, commercial simulation, agentic services, evidence intelligence — not cinematic/motif triggers.

---

## 7. Hermes runtime contract

New file: `references/hermes-runtime-contract.md`.

### Runtime assumptions

Neon Genie **may** assume:

- Hermes loads `SKILL.md` and relative references from the installed skill root
- Host tools for research may be available (web, fetch, indexes) but are **optional**
- Python 3 may be available for smoke validation helpers

Neon Genie **must not** assume:

- Git repository checkout is present
- Editable Python package install
- Kubrick, Continuity Forge, or Wayfinder runtime is installed
- Network access (offline / `research.enabled=false` must still function)
- Write access inside the installed skill directory
- A particular current working directory

### Path resolution

Scripts resolve from script directory → skill root → `references` / `schemas` / `evals`.  
User outputs default to operator project dir or `./out/neon-genie/` — never mutate skill corpus or references during ordinary runs.

### Dependency tiers

| Tier | Contents | Wave 1 |
|------|----------|--------|
| **0** | Prose skill: SKILL + profiles + schemas + references | Full advisory work |
| **1** | Stdlib Python smoke validation | `validate_hermes_skill.py` |
| **2** | Optional deps (e.g. jsonschema) | Not required; degrade cleanly if added later |
| **3** | Host research tools, Wayfinder, external systems | Optional; absence never blocks local advisory work |

### Authority (unchanged doctrine)

May: research (when tools allow), infer, generate, compare, score, model, audit, specify, route, draft, recommend.  
May not without downstream auth: spend, submit, contact, publish, modify repos, irreversible execution, canon promotion, represent forecasts as facts, mutate runtime state.

### Companion systems

| System | Role | Required? |
|--------|------|-----------|
| Host research tools | Close decision-critical evidence gaps | No |
| Wayfinder | Execution handoff consumer | No |
| Kubrick | Sibling creative skill | No — never a dependency |

---

## 8. Validation surface (Wave 1)

**File:** `scripts/validate_hermes_skill.py`  
**Dependencies:** Python 3 standard library only.  
**Invocation:**

```bash
python scripts/validate_hermes_skill.py
```

### Checks

1. `SKILL.md` exists and has closed YAML frontmatter
2. Required frontmatter fields present; `name == neon-genie`
3. `VERSION` file exists and matches frontmatter `version` and `manifest.json` `version`
4. Required paths exist:
   - `SKILL.md`, `QUICKSTART.md`, `manifest.json`, `VERSION`
   - `references/hermes-runtime-contract.md`
   - `references/CAPABILITY_MAP.md`, `references/GOLDEN_TESTS.md`
   - `profiles/`, `schemas/`, `templates/request.yaml`
   - `evals/`, `evals/rubric.md`, `examples/README.md`
   - `scripts/validate_hermes_skill.py`
5. Every profile listed in `manifest.json` `profiles` exists as `profiles/<name>.md`
6. Relative paths cited in backticks under `profiles|schemas|references|scripts|evals|templates` in `SKILL.md` (and key docs as practical) resolve on disk
7. No hard-coded machine-absolute home paths or `pip install -e` skill requirements in core skill docs
8. All `scripts/*.py` compile via `ast.parse`

Exit code `0` on pass; non-zero with enumerated failures on fail.

**Out of scope for Wave 1:** scoring opportunities, compiling packets, research fetch automation, intent routing.

---

## 9. Docs ops

| Artifact | Purpose |
|----------|---------|
| `VERSION` | Single-line `3.2.0` |
| `CHANGELOG.md` | Keep a Changelog; 3.2.0 documents packaging/layout/install |
| `QUICKSTART.md` | Install, first prompts, offline research flag, validate command, map of profiles/schemas |
| `docs/ROADMAP.md` | Waves 1–4 as in this spec |
| `docs/README.md` | Documentation index |
| Root `README.md` | Public overview; update repository layout and installation; preserve marketing quality and doctrine tables |

Bump skill version to **3.2.0** for Wave 1 (layout + installability as a minor feature release from 3.1.0).

---

## 10. Examples and evals skeleton

### Examples

- `examples/README.md` — how to use briefs with Hermes; examples are illustrative, not execution authority
- `examples/product-audit.brief.yaml` — sample request aligned with `templates/request.yaml`
- `examples/zero-option.brief.yaml` — constrained zero-capital style request

No requirement that examples produce golden outputs in Wave 1.

### Evals

- Migrate `neon-genie/tests/golden/*.json` → `evals/cases/`
- `evals/rubric.md` — encode invariants already described in `GOLDEN_TESTS.md` (NOT_COMPUTABLE on missing evidence, authority bounds, Wayfinder intent freeze, x402 rejection when ornamental, Zero Option resource honesty, etc.)
- Wave 1 does **not** require a full eval runner or CI workflow (Wave 4 / late Wave 2)

Update `references/GOLDEN_TESTS.md` paths to point at `evals/cases/`.

---

## 11. Domain preservation rules

When moving files, preserve **verbatim** unless a path rewrite is required:

- Operating sequence OPEN → ALIGN → ASCEND → CLEAR → SEAL
- Claim labels: OBSERVED, INFERRED, SPECULATIVE, NOT_COMPUTABLE
- Core pipeline, runes, mandatory gates, promotion ladder
- Research doctrine (proactive by default; offline opt-out)
- Profile contracts’ domain content
- Wayfinder ownership split (Neon owns product intent; Wayfinder owns decomposition)
- JSON schemas’ validation semantics

Allowed edits: relative path strings, version numbers, frontmatter packaging fields, links in README, removal of nested-package install wording.

---

## 12. Implementation order

1. Create working branch (e.g. `feat/ops-shell-wave1`).
2. Move nested `neon-genie/` contents to repository root; remove empty nest.
3. Add Wave 1 artifacts: `install.sh`, `VERSION`, `CHANGELOG.md`, `QUICKSTART.md`, runtime contract, validator, examples, evals migration, `docs/ROADMAP.md`, `docs/README.md`.
4. Update `SKILL.md` frontmatter and path references; update root `README.md` and `manifest.json` version.
5. Run `python scripts/validate_hermes_skill.py` until green.
6. Optionally install locally via `./install.sh` only with operator confirmation if overwriting an existing skill path.
7. Commit with clear CHANGELOG entry for 3.2.0.

---

## 13. Success criteria (Wave 1 done)

- [ ] Repository root is a valid Hermes skill (`SKILL.md` at root)
- [ ] `./install.sh` installs to `~/.hermes/skills/neon-genie`
- [ ] `python scripts/validate_hermes_skill.py` exits 0
- [ ] Runtime contract documents authority, research opt-out, Wayfinder optional, no Kubrick dependency
- [ ] `VERSION`, `CHANGELOG.md`, `QUICKSTART.md`, `docs/ROADMAP.md` present and version-consistent at 3.2.0
- [ ] Golden fixtures preserved under `evals/cases/`
- [ ] Domain doctrine preserved; only packaging/paths changed
- [ ] No cinematic/Kubrick domain content introduced

---

## 14. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Breaks users of `cp -R neon-genie` | CHANGELOG + README migration note; install.sh is new primary path |
| Accidental domain merge with Kubrick | Explicit non-goals; review checklist bans cinematic imports |
| Scope creep into Wave 2–3 | Success criteria limited to ops shell; roadmap documents deferrals |
| Version skew across files | Validator enforces VERSION ↔ frontmatter ↔ manifest |

---

## 15. Deferred detail (not Wave 1)

- Missing schemas named in prose but absent on disk (`EvidenceIntelligencePacket`, `MemeticPressurePacket`, `AuditDeliveryPacket`) — Wave 2
- Profile depth expansion — Wave 2
- Intent CLI and receipt hashing tooling — Wave 3
- GitHub Actions hermes-evals workflow — Wave 4
- Shared skill scaffold extraction — after Wave 2, only if a third skill needs it

---

## 16. Spec self-review record

| Check | Result |
|-------|--------|
| Placeholders / TBD | None material; optional install category explicitly deferred |
| Internal consistency | Wave 1 goals, layout, validator paths, and success criteria align |
| Scope | Single implementation plan; Waves 2–4 deferred explicitly |
| Ambiguity | Version fixed at 3.2.0; install path fixed; no category subdir in Wave 1 |

---

## Approval

- **Approach:** Pattern twin (shared architecture, separate domains)  
- **Wave 1 depth:** Skill ops shell first (no thin intent CLI yet)  
- **Design:** Approved in session 2026-07-30  

Next step after user review of this file: invoke **writing-plans** to produce `docs/superpowers/plans/2026-07-30-neon-genie-ops-shell.md` and implement Wave 1.
