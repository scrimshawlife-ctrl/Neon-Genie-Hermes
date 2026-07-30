# Neon Genie Ops Shell (Wave 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Flatten Neon Genie into a Kubrick-style installable Hermes skill root (ops shell only) at version 3.2.0, without changing domain doctrine.

**Architecture:** Pattern twin of Kubrick’s skill packaging — repo root becomes the skill root; `install.sh` deploys to `~/.hermes/skills/neon-genie`; stdlib smoke validator enforces layout/version consistency; docs ops (VERSION, CHANGELOG, QUICKSTART, ROADMAP) and examples/evals skeletons complete the shell. Domain profiles, gates, research doctrine, and packet schemas move path-only.

**Tech Stack:** Markdown skill contracts, JSON schemas/manifest, bash installer, Python 3 standard library validator. No new third-party dependencies.

**Spec:** `docs/superpowers/specs/2026-07-30-neon-genie-ops-shell-design.md`

## Global Constraints

- Domain isolation: no Kubrick/cinematic content; Neon mission unchanged
- Version target: **3.2.0** across `VERSION`, `SKILL.md` frontmatter, `manifest.json`, CHANGELOG
- Skill name: **neon-genie**
- Install path: **`$HOME/.hermes/skills/neon-genie`**
- Validator: stdlib only
- Authority remains **advisory_only**
- Nested `neon-genie/` package must not exist when Wave 1 is complete
- Prose-first: full advisory work without Python

---

## File map

| Path | Action | Responsibility |
|------|--------|----------------|
| `neon-genie/*` → root | Move | Flatten skill package |
| `SKILL.md` | Move + modify | Kernel + packaging frontmatter + path refs |
| `manifest.json` | Move + version bump | Machine metadata |
| `profiles/`, `schemas/`, `templates/` | Move | Domain contracts (path-only) |
| `references/*` | Move + add runtime contract | Ops + domain refs |
| `evals/cases/*` | Create from golden | Fixture home |
| `evals/rubric.md` | Create | Eval invariants skeleton |
| `examples/*` | Create | Operator briefs |
| `scripts/validate_hermes_skill.py` | Create | Smoke validation |
| `install.sh` | Create | Hermes install |
| `VERSION`, `CHANGELOG.md`, `QUICKSTART.md` | Create | Docs ops |
| `docs/ROADMAP.md`, `docs/README.md` | Create | Roadmap + docs index |
| `README.md` | Modify | Layout + install |
| `neon-genie/` | Delete when empty | Remove nest |

---

### Task 1: Flatten skill package to repository root

**Files:**
- Move: all of `neon-genie/` to repo root (except discard nested `README.md` content after folding install notes into root docs — keep file temporarily then delete)
- Delete: empty `neon-genie/` directory and `neon-genie/tests/` after evals migration in Task 3

**Interfaces:**
- Produces: root-level `SKILL.md`, `manifest.json`, `profiles/`, `schemas/`, `references/`, `templates/`, and temporary `tests/golden/` until Task 3

- [ ] **Step 1: Create branch**

```bash
cd /home/scrimshawlife/Neon-Genie-Hermes
git checkout -b feat/ops-shell-wave1
```

- [ ] **Step 2: Move package contents with git**

```bash
git mv neon-genie/SKILL.md .
git mv neon-genie/manifest.json .
git mv neon-genie/profiles .
git mv neon-genie/schemas .
git mv neon-genie/references .
git mv neon-genie/templates .
# Keep tests in place until Task 3 relocates them
git mv neon-genie/tests .
# Nested package README is obsolete after root QUICKSTART/README update
git rm neon-genie/README.md
rmdir neon-genie 2>/dev/null || rm -rf neon-genie
```

- [ ] **Step 3: Verify tree**

```bash
test -f SKILL.md && test -f manifest.json && test -d profiles && test -d schemas
test ! -d neon-genie
ls profiles | wc -l   # expect 11
```

Expected: 11 profile files; no `neon-genie/` directory.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "refactor: flatten neon-genie package to skill root"
```

---

### Task 2: Version bump and SKILL packaging frontmatter

**Files:**
- Create: `VERSION` (content: `3.2.0\n`)
- Modify: `manifest.json` — `"version": "3.2.0"`
- Modify: `SKILL.md` — version, triggers, platforms, tags, runtime contract pointer, path references

**Interfaces:**
- Produces: consistent version string `3.2.0` for validator in Task 5

- [ ] **Step 1: Write VERSION**

```text
3.2.0
```

- [ ] **Step 2: Update manifest.json version field only** to `3.2.0` (keep all other keys).

- [ ] **Step 3: Update SKILL.md frontmatter** to:

```yaml
---
name: neon-genie
version: 3.2.0
description: Governed invention, product architecture, opportunity intelligence, fragmentation mining, Zero-State execution design, agentic service decomposition, commercial simulation, and Wayfinder handoff. Proactive research by default.
author: Applied Alchemy Labs / Zero State
license: MIT
platforms: [linux, macos, windows]
tags: [NeonGenie, HermesSkill, OpportunityIntelligence, ProductArchitecture, ZeroOption, WayfinderHandoff, AdvisoryOnly, EvidenceBound]
triggers:
  - neon genie
  - product audit
  - opportunity mining
  - blocked transition
  - fragmentation scan
  - zero option
  - first cash
  - agentic services
  - x402
  - commercial simulation
  - evidence intelligence
  - wayfinder handoff
  - wayfinder execution packet
  - cost of inaction
  - audit delivery
---
```

- [ ] **Step 4: After frontmatter title, insert Hermes packaging section** (before Mission or after title):

```markdown
## Hermes skill identity

Neon Genie is a **standalone Hermes skill**. Hermes loads this directory directly and uses `SKILL.md` as the operating contract. No Python package install, Kubrick skill, Wayfinder runtime, or external knowledge base is required to load.

See `references/hermes-runtime-contract.md` for path, artifact, authority, and dependency policy.

**Optional companions:** host research tools, Wayfinder (handoff consumer). Their absence never blocks local advisory work.
```

- [ ] **Step 5: Fix any path strings** that still say `neon-genie/profiles` etc. to root-relative `profiles/`, `schemas/`, `references/`.

- [ ] **Step 6: Commit**

```bash
git add VERSION manifest.json SKILL.md
git commit -m "feat(skill): package as root Hermes skill v3.2.0"
```

---

### Task 3: Migrate golden tests to evals; add rubric and examples

**Files:**
- Create: `evals/cases/` (move from `tests/golden/`)
- Create: `evals/rubric.md`
- Create: `examples/README.md`, `examples/product-audit.brief.yaml`, `examples/zero-option.brief.yaml`
- Modify: `references/GOLDEN_TESTS.md` path pointers
- Delete: empty `tests/` after move

**Interfaces:**
- Produces: paths required by validator (`evals/`, `evals/rubric.md`, `examples/README.md`)

- [ ] **Step 1: Relocate fixtures**

```bash
mkdir -p evals/cases
git mv tests/golden/zero-option.json evals/cases/
git mv tests/golden/x402-misfit.json evals/cases/
git mv tests/golden/wayfinder-change-control.json evals/cases/
rm -rf tests
```

- [ ] **Step 2: Write `evals/rubric.md`**

```markdown
# Neon Genie Eval Rubric (skeleton)

Wave 1 captures invariants for later automated runners. Fixtures live in `evals/cases/`.

## Global invariants

1. Missing executable evidence → `NOT_COMPUTABLE` (never fabricate).
2. High monetization or memetic strength cannot override authority, evidence, integration, or anti-capture gate failures.
3. x402 rejected when ornamental or when conventional billing is superior.
4. Zero Option never invents unavailable skills, capital, or access.
5. Wayfinder execution packet cannot modify product intent; intent changes require Neon Genie review.
6. No packet grants execution, spending, or publishing authority.
7. Same canonical input + profile set → structurally stable labeled outputs (Wave 2+ determinism checks).

## Fixture index

| Case | Expectation |
|------|-------------|
| `zero-option.json` | No skills/access → NOT_COMPUTABLE |
| `x402-misfit.json` | Ornamental x402 rejected |
| `wayfinder-change-control.json` | Intent change blocked without Neon review |
```

- [ ] **Step 3: Write `examples/README.md`**

```markdown
# Neon Genie examples

Illustrative request briefs for Hermes. They are **not** execution authority.

1. Install the skill (`./install.sh` from repo root).
2. Paste or attach a brief and invoke Neon Genie (e.g. `/neon-genie` or natural language matching triggers).
3. Prefer smallest sufficient profile set; research is proactive unless `research.enabled=false`.

| File | Use |
|------|-----|
| `product-audit.brief.yaml` | Product architecture + commercial + wayfinder handoff |
| `zero-option.brief.yaml` | Constrained first-cash / zero-capital loop |
```

- [ ] **Step 4: Write example briefs** aligned with `templates/request.yaml`:

`examples/product-audit.brief.yaml`:

```yaml
request_id: "example-product-audit-001"
requested_outcome: "Audit product coherence and produce a Wayfinder-ready handoff packet"
target_user: "operator building a governed multi-skill product"
current_state: "partial product intent; unclear boundaries"
desired_state: "evidence-bound product packet + execution handoff without intent rewrite"
constraints:
  - "advisory_only"
  - "do not modify repositories"
canonical_sources: []
preferred_profiles:
  - product_architecture
  - commercial
  - wayfinder_handoff
requested_outputs:
  - NeonGenieProductPacket
  - WayfinderExecutionPacket
  - NeonGenieRunReceipt
research:
  enabled: true
  offline: false
  max_fetches: null
  focus:
    - "comparable product boundaries"
authority:
  research: true
  drafting: true
  execution: false
  spending: false
  publishing: false
human_review_required: true
```

`examples/zero-option.brief.yaml`:

```yaml
request_id: "example-zero-option-001"
requested_outcome: "First cash within 7 days from existing skills and access only"
target_user: "solo operator with no new capital"
current_state: "skills and access undeclared in this example"
desired_state: "executable zero-option loop or honest NOT_COMPUTABLE"
constraints:
  - "no capital"
  - "no fictional resources"
canonical_sources: []
preferred_profiles:
  - zero_option
requested_outputs:
  - ZeroOptionPacket
  - NeonGenieRunReceipt
research:
  enabled: false
  offline: true
  max_fetches: 0
  focus: []
authority:
  research: false
  drafting: true
  execution: false
  spending: false
  publishing: false
human_review_required: true
```

- [ ] **Step 5: Update `references/GOLDEN_TESTS.md`** to reference `evals/cases/` instead of `tests/golden/`.

- [ ] **Step 6: Commit**

```bash
git add evals examples references/GOLDEN_TESTS.md
git add -u tests 2>/dev/null || true
git commit -m "test: migrate golden fixtures to evals; add examples skeleton"
```

---

### Task 4: Runtime contract, install.sh, docs ops

**Files:**
- Create: `references/hermes-runtime-contract.md`
- Create: `install.sh` (executable)
- Create: `CHANGELOG.md`, `QUICKSTART.md`, `docs/ROADMAP.md`, `docs/README.md`
- Modify: root `README.md` layout + installation sections

**Interfaces:**
- Produces: paths required by validator; operator install entrypoint

- [ ] **Step 1: Write `references/hermes-runtime-contract.md`** per design §7 (Neon-specific: research optional, Wayfinder optional, Kubrick not a dependency, advisory_only, artifact dir `./out/neon-genie/`, tiers 0–3).

Full content must include sections:

1. Purpose  
2. Runtime assumptions (may / must not)  
3. Path resolution  
4. Dependency tiers (0 prose, 1 stdlib helpers, 2 optional packages, 3 host tools / Wayfinder)  
5. Authority boundaries  
6. Research policy (proactive when tools exist; offline opt-out)  
7. Artifact policy (PROPOSED / labeled claims; no corpus mutation)  
8. Companion systems table  
9. Validation entrypoint: `python scripts/validate_hermes_skill.py`

- [ ] **Step 2: Write `install.sh`**

```bash
#!/usr/bin/env bash
# Neon Genie — Hermes Skill Installer
# Usage:
#   ./install.sh                 # installs to ~/.hermes/skills/neon-genie

set -euo pipefail

TARGET_BASE="${HOME}/.hermes/skills"
DEST="${TARGET_BASE}/neon-genie"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Neon Genie to: ${DEST}"
mkdir -p "${TARGET_BASE}"

if [ -d "${DEST}" ]; then
  echo "Existing installation found. Backing up to ${DEST}.bak"
  rm -rf "${DEST}.bak"
  mv "${DEST}" "${DEST}.bak"
fi

mkdir -p "${DEST}"
# Copy skill tree; exclude VCS metadata
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude '.git' --exclude '.gitignore' "${ROOT}/" "${DEST}/"
else
  tar -C "${ROOT}" --exclude '.git' -cf - . | tar -C "${DEST}" -xf -
fi

chmod +x "${DEST}/scripts/"*.py 2>/dev/null || true
chmod +x "${DEST}/install.sh" 2>/dev/null || true

echo ""
echo "Neon Genie installed successfully."
echo "Location: ${DEST}"
echo ""
echo "Next steps:"
echo "  1. Restart Hermes or reload skills."
echo "  2. Validate: python ${DEST}/scripts/validate_hermes_skill.py"
echo "  3. Try triggers like: 'product audit', 'zero option', 'wayfinder handoff'"
echo ""
echo "The skill works standalone inside Hermes (advisory only)."
```

```bash
chmod +x install.sh
```

- [ ] **Step 3: Write `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to Neon Genie are documented in this file.

## [3.2.0] — 2026-07-30

### Added
- Root-level Hermes skill packaging (installable skill root)
- `install.sh` → `~/.hermes/skills/neon-genie`
- `references/hermes-runtime-contract.md`
- `scripts/validate_hermes_skill.py` smoke validator
- `VERSION`, `QUICKSTART.md`, `docs/ROADMAP.md`, `docs/README.md`
- `examples/` operator briefs
- `evals/` fixture home + rubric skeleton

### Changed
- Flattened nested `neon-genie/` package to repository root
- Version alignment across VERSION, SKILL.md, manifest.json

### Migration
- Replace `cp -R neon-genie …` with `./install.sh` or copy repository root into Hermes skills

## [3.1.0] — prior

- Proactive research by default; MIT license; packaging README polish
```

- [ ] **Step 4: Write `QUICKSTART.md`** covering: install, first prompts (from existing README), offline research, validate command, profile list pointer, authority one-liner.

- [ ] **Step 5: Write `docs/ROADMAP.md`** with Waves 1–4 from the design spec; mark Wave 1 as current.

- [ ] **Step 6: Write `docs/README.md`** index linking README, QUICKSTART, ROADMAP, SKILL, runtime contract, specs/plans.

- [ ] **Step 7: Update root `README.md`**

- Version badge → 3.2.0  
- Installation → `./install.sh`  
- Repository layout → new tree (no nested `neon-genie/`)  
- Golden tests path → `evals/cases/`  
- Versioning table → 3.2.0  

- [ ] **Step 8: Commit**

```bash
git add references/hermes-runtime-contract.md install.sh CHANGELOG.md QUICKSTART.md docs/ROADMAP.md docs/README.md README.md
git commit -m "docs: add runtime contract, install, and ops docs for v3.2.0"
```

---

### Task 5: Smoke validator (TDD)

**Files:**
- Create: `scripts/validate_hermes_skill.py`
- Test: run validator as the test (no pytest required; exit code is the suite)

**Interfaces:**
- Produces: CLI exit 0/1; prints FAIL reasons to stderr

- [ ] **Step 1: Implement `scripts/validate_hermes_skill.py`** (stdlib only). Required behavior:

```python
#!/usr/bin/env python3
"""Validate Neon Genie as a portable, self-contained Hermes skill.

Uses only the Python standard library. Run from any working directory:
    python scripts/validate_hermes_skill.py
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILL_FILE = SKILL_ROOT / "SKILL.md"
VERSION_FILE = SKILL_ROOT / "VERSION"
MANIFEST_FILE = SKILL_ROOT / "manifest.json"

REQUIRED_FRONTMATTER = {"name", "description", "version", "author"}
REQUIRED_PATHS = [
    "SKILL.md",
    "QUICKSTART.md",
    "manifest.json",
    "VERSION",
    "references/hermes-runtime-contract.md",
    "references/CAPABILITY_MAP.md",
    "references/GOLDEN_TESTS.md",
    "profiles",
    "schemas",
    "templates/request.yaml",
    "evals",
    "evals/rubric.md",
    "examples/README.md",
    "scripts/validate_hermes_skill.py",
    "install.sh",
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        # Skip nested YAML list/map lines without simple scalars
        val = value.strip().strip('"').strip("'")
        if val.startswith("[") or val == "|" or val == ">" or val == "":
            # keep first-line scalar only; empty means complex value
            if key.strip() not in fields:
                fields[key.strip()] = val
            continue
        fields[key.strip()] = val
    return fields


def referenced_relative_paths(text: str) -> set[str]:
    candidates: set[str] = set()
    for match in re.finditer(
        r"`((?:profiles|schemas|references|scripts|evals|templates|examples)/[^`\n]+)`",
        text,
    ):
        value = match.group(1)
        if " " not in value and not value.startswith("/"):
            candidates.add(value.rstrip(".,;:"))
    return candidates


def validate_python(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeError) as exc:
        errors.append(f"Python compile failure: {path.relative_to(SKILL_ROOT)}: {exc}")
    return errors


def main() -> int:
    errors: list[str] = []

    if not SKILL_FILE.is_file():
        print("FAIL: SKILL.md missing", file=sys.stderr)
        return 1

    skill_text = SKILL_FILE.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(skill_text)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    missing_fields = sorted(REQUIRED_FRONTMATTER - set(frontmatter))
    if missing_fields:
        errors.append(f"Missing frontmatter fields: {', '.join(missing_fields)}")
    if frontmatter.get("name") != "neon-genie":
        errors.append("Frontmatter name must be 'neon-genie'")

    version_fm = frontmatter.get("version", "")
    if not VERSION_FILE.is_file():
        errors.append("VERSION file missing")
        version_file = ""
    else:
        version_file = VERSION_FILE.read_text(encoding="utf-8").strip()

    manifest: dict = {}
    if not MANIFEST_FILE.is_file():
        errors.append("manifest.json missing")
    else:
        try:
            manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"manifest.json invalid JSON: {exc}")

    version_manifest = str(manifest.get("version", ""))
    if version_file and version_fm and version_file != version_fm:
        errors.append(f"VERSION ({version_file}) != SKILL frontmatter version ({version_fm})")
    if version_file and version_manifest and version_file != version_manifest:
        errors.append(f"VERSION ({version_file}) != manifest.json version ({version_manifest})")
    if version_fm and version_manifest and version_fm != version_manifest:
        errors.append(
            f"SKILL frontmatter version ({version_fm}) != manifest.json version ({version_manifest})"
        )

    for relative in REQUIRED_PATHS:
        path = SKILL_ROOT / relative
        if not path.exists():
            errors.append(f"Missing required path: {relative}")

    profiles = manifest.get("profiles") or []
    if not isinstance(profiles, list) or not profiles:
        errors.append("manifest.json profiles must be a non-empty list")
    else:
        for name in profiles:
            p = SKILL_ROOT / "profiles" / f"{name}.md"
            if not p.is_file():
                errors.append(f"Profile listed in manifest but missing: profiles/{name}.md")

    for rel in sorted(referenced_relative_paths(skill_text)):
        # Allow directory references and files
        target = SKILL_ROOT / rel
        if not target.exists():
            # also try without trailing fragments
            errors.append(f"SKILL.md references missing path: {rel}")

    for py in sorted((SKILL_ROOT / "scripts").glob("*.py")) if (SKILL_ROOT / "scripts").is_dir() else []:
        errors.extend(validate_python(py))

    # Forbid obvious machine-local assumptions in core docs
    forbid_patterns = [
        re.compile(r"pip install -e"),
        re.compile(r"/Users/[A-Za-z]"),
        re.compile(r"/home/(?!scrimshawlife)"),  # allow nothing specific; skip or use generic only
    ]
    # Simpler: only check pip install -e and Windows/Users absolute paths
    forbid_patterns = [
        re.compile(r"pip install -e"),
        re.compile(r"/Users/"),
        re.compile(r"[A-Za-z]:\\\\Users\\\\"),
    ]
    for rel in ("SKILL.md", "QUICKSTART.md", "references/hermes-runtime-contract.md", "README.md"):
        path = SKILL_ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pat in forbid_patterns:
            if pat.search(text):
                errors.append(f"Forbidden pattern {pat.pattern!r} in {rel}")

    if errors:
        print("FAIL: Neon Genie skill validation", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("PASS: Neon Genie skill validation")
    print(f"  root: {SKILL_ROOT}")
    print(f"  version: {version_file or version_fm or version_manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Note for implementer: drop the broken intermediate `forbid_patterns` block — keep only the final three patterns. Do not hard-code operator usernames.

- [ ] **Step 2: Run validator**

```bash
python scripts/validate_hermes_skill.py
```

Expected: `PASS: Neon Genie skill validation` and exit 0. Fix any reported missing paths before proceeding.

- [ ] **Step 3: Negative sanity (optional)**

```bash
# Temporarily break VERSION and confirm FAIL, then restore
```

- [ ] **Step 4: Commit**

```bash
git add scripts/validate_hermes_skill.py
git commit -m "feat(scripts): add stdlib Hermes skill smoke validator"
```

---

### Task 6: Final integration check and success criteria

**Files:**
- Touch only if validator or docs still fail

- [ ] **Step 1: Run full checklist**

```bash
python scripts/validate_hermes_skill.py
test ! -d neon-genie
test -f VERSION && grep -q 3.2.0 VERSION
test -x install.sh || chmod +x install.sh
wc -l profiles/*.md | tail -1
ls evals/cases | wc -l   # expect 3
```

- [ ] **Step 2: Confirm success criteria from design §13**

- [ ] Root is valid Hermes skill  
- [ ] install.sh present and points to `~/.hermes/skills/neon-genie`  
- [ ] Validator exits 0  
- [ ] Runtime contract present with authority + no Kubrick dependency  
- [ ] VERSION/CHANGELOG/QUICKSTART/ROADMAP present at 3.2.0  
- [ ] Golden fixtures under `evals/cases/`  
- [ ] Domain doctrine preserved  
- [ ] No cinematic content  

- [ ] **Step 3: Final commit if any fixups**

```bash
git add -A
git status
git commit -m "chore: Wave 1 ops-shell integration fixups" || true
```

- [ ] **Step 4: Do not run `./install.sh` into the live Hermes tree without explicit operator confirmation** (may overwrite). Document command for the operator:

```bash
./install.sh
python ~/.hermes/skills/neon-genie/scripts/validate_hermes_skill.py
```

---

## Spec coverage self-review

| Spec section | Task |
|--------------|------|
| Flatten layout | Task 1 |
| Version 3.2.0 + frontmatter | Task 2 |
| Evals + examples | Task 3 |
| Runtime contract, install, docs ops | Task 4 |
| Validator | Task 5 |
| Success criteria | Task 6 |
| Waves 2–4 deferred | `docs/ROADMAP.md` in Task 4 |
| No domain merge | Global constraints + no Kubrick files in any task |

## Placeholder scan

None intentional. Validator code is complete; install script complete; example YAML complete.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-30-neon-genie-ops-shell.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — execute tasks in this session with checkpoints  

After plan commit, implementers should follow tasks in order with frequent commits.
