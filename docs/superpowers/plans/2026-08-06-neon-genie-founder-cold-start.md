# Neon Genie Founder Cold-Start + Contract Honesty Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship Neon Genie **3.25.0** founder cold-start wave: natural-language profile routing for transitional builders, default stuck-idea job shape in `SKILL.md`, wire `capital_sprint` into the router, move the hub support list below operating doctrine, and document packaging-vs-judgment honesty.

**Architecture:** Packaging router (`route_profiles.py`) and chat contract (`SKILL.md` `profile_router`) stay keyword/phrase aligned. Doctrine remains fail-closed and advisory-only. Distribution spine still owns the generated hub file list; only its **position** in `SKILL.md` changes. No privacy model change. No live Hermes LLM CI in this wave.

**Tech Stack:** Markdown skill contracts, Python 3 standard library only, existing JSON Schema / eval harness, `distribution_spine.py` for hub parity.

**Spec:** `docs/superpowers/specs/2026-08-06-neon-genie-skill-audit-design.md`

## Global Constraints

- Version target: **3.25.0** across `VERSION`, `SKILL.md` frontmatter, `manifest.json`, `references/VERSION`, `CHANGELOG.md`, hub package after spine write
- Authority: **`advisory_only`**, no execution / spend / publish
- Always co-load **`core` + `privacy`**
- Smallest sufficient profile set (do not dump all profiles on founder phrases)
- Stdlib only for new/changed Python
- Hub path list: **relocate, do not delete**; markers `<!-- BEGIN HUB_SUPPORT_FILES` / `END` must remain
- `distribution.yaml` `skill_md.section_start` / `section_end` must still bookend the generated block after the move
- Router packaging and `SKILL.md` `profile_router` triggers must stay **semantically aligned**
- Do not claim green `do eval` proves free-chat judgment
- Do not invent resources for zero-option paths

---

## File map

| Path | Action | Responsibility |
|------|--------|----------------|
| `scripts/test_route_profiles.py` | Create | Founder-language + capital_sprint routing table tests |
| `scripts/route_profiles.py` | Modify | New triggers for founder language + capital_sprint |
| `SKILL.md` | Modify | Router YAML, default job section, hub block position, version |
| `scripts/recipe_run.py` | Modify | Optional thin `capital-sprint` recipe + RECIPES entry |
| `scripts/doctor.py` | Modify | Only if capital-sprint recipe smoke is added (mirror other recipes) |
| `QUICKSTART.md` | Modify | Plain-English Hermes example |
| `README.md` | Modify | Judgment-gap honesty + plain example pointer |
| `docs/PREMIERE.md` or `CONTRIBUTING.md` | Modify | Optional one-liner judgment honesty (prefer README) |
| `docs/ROADMAP.md` | Modify | 3.25.0 wave note |
| `VERSION`, `manifest.json`, `CHANGELOG.md` | Modify | 3.25.0 |
| `distribution_spine.py write` | Run | Refresh hub mirrors + package after SKILL edits |
| `skills/neon-genie/*` | Generated | Via spine write — do not hand-edit |

---

### Task 1: Founder-language router tests + implementation (F1)

**Files:**
- Create: `scripts/test_route_profiles.py`
- Modify: `scripts/route_profiles.py` (`PROFILE_TRIGGERS` dict)

**Interfaces:**
- Consumes: `match_profiles(text: str) -> list[str]`, CLI `python3 scripts/route_profiles.py --text "..." --json`
- Produces: Expanded triggers so O1-style text selects `opportunity_mining` (+ `zero_option` when scarcity language present)

- [ ] **Step 1: Write failing tests**

Create `scripts/test_route_profiles.py`:

```python
#!/usr/bin/env python3
"""Unit tests for founder-language and profile routing (stdlib only)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PY = sys.executable
ROUTE = SCRIPT_DIR / "route_profiles.py"


def route(text: str) -> dict:
    r = subprocess.run(
        [PY, str(ROUTE), "--text", text, "--json"],
        cwd=SKILL_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr or r.stdout
    return json.loads(r.stdout)


def test_o1_founder_roadmap_selects_opportunity() -> None:
    out = route(
        "I'm between jobs with limited money and need a roadmap for my app idea"
    )
    selected = set(out["selected"])
    assert "core" in selected and "privacy" in selected
    assert "opportunity_mining" in selected, selected
    assert "zero_option" in selected, selected
    print("PASS: O1 founder roadmap + scarcity")


def test_product_audit_still_works() -> None:
    out = route("product audit for my SaaS")
    assert "product_architecture" in out["selected"]
    print("PASS: product audit")


def test_zero_capital_phrase_still_works() -> None:
    out = route("zero capital first cash")
    assert "zero_option" in out["selected"]
    print("PASS: zero capital phrase")


def test_venture_capital_does_not_force_zero_option() -> None:
    """'venture capital' alone is not scarcity — do not over-trigger zero_option."""
    out = route("research venture capital firm partners for a Series A thesis")
    assert "zero_option" not in out["selected"], out["selected"]
    print("PASS: venture capital not zero_option")


def test_capital_sprint_routes() -> None:
    out = route("design a capital sprint and impact object for our annual fund")
    assert "capital_sprint" in out["selected"], out["selected"]
    print("PASS: capital_sprint routes")


def test_brief_preferred_capital_sprint() -> None:
    brief = SKILL_ROOT / "examples" / "capital-sprint.brief.yaml"
    r = subprocess.run(
        [PY, str(ROUTE), "--request", str(brief), "--json"],
        cwd=SKILL_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr or r.stdout
    out = json.loads(r.stdout)
    assert "capital_sprint" in out["selected"]
    print("PASS: capital-sprint brief preferred_profiles")


if __name__ == "__main__":
    test_o1_founder_roadmap_selects_opportunity()
    test_product_audit_still_works()
    test_zero_capital_phrase_still_works()
    test_venture_capital_does_not_force_zero_option()
    test_capital_sprint_routes()
    test_brief_preferred_capital_sprint()
    print("ALL PASS: test_route_profiles")
```

- [ ] **Step 2: Run tests — expect FAIL on O1 and capital_sprint**

```bash
cd /home/scrimshawlife/Neon-Genie-Hermes
python3 scripts/test_route_profiles.py
```

Expected: assertion failure on `opportunity_mining` / `zero_option` / `capital_sprint` not in selected.

- [ ] **Step 3: Extend `PROFILE_TRIGGERS` in `scripts/route_profiles.py`**

Add triggers (merge into existing tuples; do not remove existing phrases):

```python
# Inside PROFILE_TRIGGERS["opportunity_mining"] add:
"roadmap",
"business idea",
"go into business",
"for myself",
"self-employed",
"side project",
"launch my",
"turn my idea",
"app idea",
"product idea",
"what should i build",
"where do i start",
"next steps for my idea",
"how do i approach",

# Inside PROFILE_TRIGGERS["zero_option"] add:
"limited money",
"limited resources",
"limited capital",
"between jobs",
"bootstrapped",
"no budget",
"can't afford",
"cannot afford",
"first revenue",
"make money from",

# Inside PROFILE_TRIGGERS["product_architecture"] add if missing:
"app idea",  # only if you want product_architecture on app idea; prefer opportunity only
# Prefer NOT adding bare "app idea" here — keep product_architecture on product audit / system design

# New key:
"capital_sprint": (
    "capital sprint",
    "annual fund",
    "donation drive",
    "membership drive",
    "fundraising deadline",
    "501c3 campaign",
    "501(c)(3)",
    "impact object",
    "donor sprint",
    "nonprofit capital",
    "raise money by deadline",
),
```

**Edge rule for "venture capital":** do **not** add the bare trigger `"capital"` or `"venture capital"` to `zero_option`. Scarcity phrases must stay multi-word (`limited capital`, `no capital`, `zero capital`).

- [ ] **Step 4: Re-run tests — expect PASS**

```bash
python3 scripts/test_route_profiles.py
```

Expected: `ALL PASS: test_route_profiles`

- [ ] **Step 5: Commit**

```bash
git add scripts/test_route_profiles.py scripts/route_profiles.py
git commit -m "feat: founder-language and capital_sprint profile routing"
```

---

### Task 2: Align `SKILL.md` profile_router (F1 + F3 chat path)

**Files:**
- Modify: `SKILL.md` — `profile_router` YAML block only in this task

**Interfaces:**
- Chat path must list the same trigger *families* as `route_profiles.py` (exact YAML list items, human-readable)

- [ ] **Step 1: Update `profile_router` in `SKILL.md`**

Locate the `profile_router:` block. Apply these edits:

1. Under `opportunity_mining.triggers`, append:
   - `roadmap`, `business idea`, `go into business`, `side project`, `app idea`, `product idea`, `what should I build`, `where do I start`, `next steps`

2. Under `zero_option.triggers`, append:
   - `limited money`, `limited resources`, `limited capital`, `between jobs`, `bootstrapped`, `no budget`, `first revenue`

3. Add new block (same indentation as siblings):

```yaml
  capital_sprint:
    triggers:
      - capital sprint
      - annual fund
      - donation drive
      - membership drive
      - fundraising deadline
      - impact object
      - donor sprint
      - nonprofit capital raise
```

- [ ] **Step 2: Sanity check packaging still matches chat intent**

```bash
python3 scripts/route_profiles.py --text "I'm between jobs with limited money and need a roadmap for my app idea" --json
python3 scripts/test_route_profiles.py
```

Expected: selected includes `opportunity_mining` and `zero_option`; tests PASS.

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "docs(skill): align profile_router with founder and capital_sprint triggers"
```

---

### Task 3: Thin capital-sprint packaging recipe (F3 complete)

**Files:**
- Modify: `scripts/recipe_run.py` — add `recipe_capital_sprint` + RECIPES entry
- Modify: `scripts/doctor.py` only if doctor enumerates recipes by name list (search for `opportunity` / `recipe smoke`)

**Interfaces:**
- `do recipe --name capital-sprint --out out/neon-genie/capital-sprint`
- Uses `examples/capital-sprint.brief.yaml`
- Emits stub packet + receipt + envelope via `recipe_common` patterns (copy structure from `recipe_opportunity`)

- [ ] **Step 1: Find doctor recipe list**

```bash
rg -n "recipe smoke|opportunity|RECIPES|product-audit" scripts/doctor.py | head -40
```

- [ ] **Step 2: Add `recipe_capital_sprint` to `scripts/recipe_run.py`**

Place before `RECIPES = {`. Pattern (adapt imports/helpers already in file):

```python
def recipe_capital_sprint(out: Path) -> int:
    brief = SKILL_ROOT / "examples" / "capital-sprint.brief.yaml"
    route = rc.route_request(brief)
    rc.write_json(out / "profile-route.json", route)
    profiles = route.get("selected") or ["core", "privacy", "capital_sprint"]

    data_req = {
        "request_id": "dr-org-identity-deadline",
        "field": "org_legal_identity_and_hard_deadline",
        "why_decision_critical": "Capital sprint fails closed without legal org identity and deadline",
        "sensitivity": "operator",
        "suggested_source": "Operator org records (EIN, tax status) and board-approved deadline",
        "blocks_promotion": True,
        "status": "open",
    }
    data_requests = [data_req]
    rc.write_json(out / "data-requests.json", data_requests)

    packet = {
        "sprint_window": {"days": [7, 14, 30], "deadline": "NOT_COMPUTABLE_until_operator"},
        "impact_object": {
            "goal": "NOT_COMPUTABLE_until_operator",
            "unit_cost": "NOT_COMPUTABLE_until_operator",
            "note": "Stub packaging packet; full CapitalSprintPacket is prose-runtime",
        },
        "warm_network_classes": ["member", "alumni", "corporate", "creator", "cold"],
        "completion_proof": "externally checkable gift total vs floor by deadline OR documented shortfall",
        "proof_path": [
            "satisfy DataRequest for org identity and deadline",
            "publish advisory campaign card (operator executes)",
            "record gifts against floor",
            "ledger proof_obtained or proof_failed",
        ],
        "promotion_state": "TESTABLE",
        "authority": "advisory_only",
        "grants_execution": False,
        "constraints": [
            "no private org names in shared corpus",
            "dues are not donations",
        ],
    }
    packet_path = out / "capital-sprint-packet.stub.json"
    rc.write_json(packet_path, packet)
    # If validate_packet supports capital_sprint type, call it; else skip typed validate
    # Prefer: only validate if schema type exists in validate_packet.py

    receipt_path = out / "run-receipt.json"
    rc.build_receipt(
        receipt_path,
        profiles,
        status="PROPOSED",
        promotion_state="TESTABLE",
        not_computable="org_identity,deadline,floor_until_declared",
        packets=[packet_path],
        data_requests=data_requests,
        brief=brief,
    )
    return rc.finish(
        recipe="capital-sprint",
        brief=brief,
        out=out,
        route=route,
        artifacts=[
            out / "profile-route.json",
            packet_path,
            out / "data-requests.json",
            receipt_path,
            out / "recipe-summary.json",
        ],
        extra={"outcome": "CAPITAL_SPRINT_STUB_WITH_REQUEST"},
    )
```

Register:

```python
RECIPES: dict[str, RecipeFn] = {
    # ... existing ...
    "capital-sprint": recipe_capital_sprint,
}
```

- [ ] **Step 3: Wire doctor smoke if doctor has an explicit recipe list**

If `doctor.py` hardcodes recipe names, append `capital-sprint` the same way as `opportunity`. If it iterates `RECIPES` dynamically, no change.

- [ ] **Step 4: Run recipe**

```bash
python3 scripts/neon_genie.py do recipe --name capital-sprint --out out/neon-genie/capital-sprint
python3 scripts/route_profiles.py --request examples/capital-sprint.brief.yaml --json
```

Expected: exit 0; `capital_sprint` in selected; `run-envelope.json` present under out dir.

- [ ] **Step 5: Commit**

```bash
git add scripts/recipe_run.py scripts/doctor.py
git commit -m "feat: capital-sprint packaging recipe"
```

---

### Task 4: Move hub support list to end of `SKILL.md` (F4)

**Files:**
- Modify: `SKILL.md` — relocate hub section
- Possibly modify: `distribution.yaml` only if `section_end` text must change (prefer keep exact string)
- Run: `python3 scripts/distribution_spine.py write` then `verify`

**Interfaces:**
- `distribution.yaml`:
  - `skill_md.section_start: "### Hermes Hub support files"`
  - `skill_md.section_end: "Full tree also keeps root schemas, profiles, evals, VERSION, and manifest"`
- Spine rewrites content **between** heading line and `section_end` substring

- [ ] **Step 1: Manual structure at end of `SKILL.md`**

Cut the entire block starting at `### Hermes Hub support files` through the paragraph that begins with `Full tree also keeps root schemas...` (include that paragraph) from its **current early position**.

Paste it at the **end of the file** (after Registry and memory), preserving:

```markdown
### Hermes Hub support files

... (generated markers + bullets stay as-is until write) ...

Full tree also keeps root schemas, profiles, evals, VERSION, and manifest for clone/`./install.sh` installs (scripts resolve either layout via `scripts/paths.py`).
```

Ensure no duplicate `### Hermes Hub support files` remains near Packaging CLI.

- [ ] **Step 2: Confirm spine can still find markers**

```bash
python3 scripts/distribution_spine.py verify
```

Expected: PASS. If FAIL with NG-PKG-006/007, fix heading/`section_end` exact strings to match `distribution.yaml`.

- [ ] **Step 3: Refresh package**

```bash
python3 scripts/distribution_spine.py write
python3 scripts/distribution_spine.py verify
diff -q SKILL.md skills/neon-genie/SKILL.md
```

Expected: verify PASS; hub package SKILL matches root after write.

- [ ] **Step 4: Commit**

```bash
git add SKILL.md skills/neon-genie/SKILL.md distribution.yaml
# include any mirror churn from write
git status -sb
git add -u skills/neon-genie SKILL.md
git commit -m "refactor(skill): load hub support list after operating doctrine"
```

---

### Task 5: Default operator job shape + plain-English example (F2)

**Files:**
- Modify: `SKILL.md` — insert section **after Mission, before Research doctrine**
- Modify: `QUICKSTART.md` — one plain-English chat example

**Interfaces:**
- Section title: `## Default operator job (transitional builders)`
- Cross-links profiles by name: `opportunity_mining`, `zero_option`

- [ ] **Step 1: Insert into `SKILL.md` after Mission**

```markdown
## Default operator job (transitional builders)

When the operator is developing an idea under constraint (solo, transitional,
limited money/time/skills) and has not named a specialized recipe, default to
this job shape — still **advisory only**:

1. **Name the stuck point** — who is blocked, current state, what “done” looks like.
2. **Capture constraints** — time, money, skills, access. Never invent resources.
3. **Find → request → refuse** — research public facts; emit `DataRequest` for private
   facts; label claims `OBSERVED` / `INFERRED` / `SPECULATIVE` / `NOT_COMPUTABLE`.
4. **Shape the plan** — roadmap and/or approach options with **completion_proof**
   (externally checkable). Prefer profiles `opportunity_mining` and, when resources
   are scarce, `zero_option` (plus `product_architecture` only if a product/system
   boundary is in scope).
5. **Seal as drafts** — packets + receipt; no spend, publish, contact, or repo mutation.

**Example Hermes prompt (plain English):**

```text
Use Neon Genie. I'm between jobs with limited money and an app idea.
I need a realistic roadmap and first approaches I can actually run.
Do not invent buyers, capital, or skills I did not declare.
Research public facts if you can; request private facts with DataRequest.
Label every important claim. Advisory only — do not modify any repo.
```
```

- [ ] **Step 2: Add the same example to `QUICKSTART.md` under Use in Hermes**

Place near existing `/neon-genie` examples as “plain English (transitional builders)”.

- [ ] **Step 3: Commit**

```bash
git add SKILL.md QUICKSTART.md
git commit -m "docs(skill): default transitional-builder job shape and example"
```

---

### Task 6: Judgment-gap honesty (F5)

**Files:**
- Modify: `README.md` — short subsection under How to use or after badges/trust area
- Optionally one sentence in `docs/PREMIERE.md` “Proof of maturity” table

- [ ] **Step 1: Add README subsection**

```markdown
### What packaging checks prove (and what they do not)

| Proved by `do doctor` / `do eval` / dist spine | Still requires Hermes judgment |
|-----------------------------------------------|--------------------------------|
| Install integrity, hub package parity | Live research quality |
| Schema and receipt/envelope shape | Claim labeling in free chat |
| Fixture gates (P–R, privacy packaging, authority stubs) | Multi-turn honesty under pressure |
| Recipe packaging stubs | Outcome usefulness in the real world |

Green CI means the **shell** is sound. It does **not** mean every chat run is fully evaluated.
Live multi-turn Hermes evals remain a later roadmap item.
```

- [ ] **Step 2: Commit**

```bash
git add README.md docs/PREMIERE.md
git commit -m "docs: clarify packaging proof vs Hermes judgment"
```

---

### Task 7: Version 3.25.0 + full smoke

**Files:**
- Modify: `VERSION` → `3.25.0`
- Modify: `SKILL.md` frontmatter `version: 3.25.0`
- Modify: `manifest.json` `"version": "3.25.0"`
- Modify: `CHANGELOG.md` — new top section
- Modify: `docs/ROADMAP.md` — maintenance table row for 3.25.0
- Run: `python3 scripts/distribution_spine.py write` (syncs VERSION mirrors + package)

- [ ] **Step 1: Bump versions and CHANGELOG**

`CHANGELOG.md` entry outline:

```markdown
## 3.25.0 — Founder cold-start

- Founder-language profile routing (roadmap / limited resources → opportunity + zero_option)
- `capital_sprint` router triggers + packaging recipe
- Default transitional-builder job shape in SKILL.md
- Hub support file list moved below operating doctrine
- Docs: packaging checks vs Hermes judgment
```

- [ ] **Step 2: Spine write + verify**

```bash
python3 scripts/distribution_spine.py write
python3 scripts/distribution_spine.py verify
```

- [ ] **Step 3: Full smoke**

```bash
python3 scripts/test_route_profiles.py
python3 scripts/neon_genie.py do eval
python3 scripts/neon_genie.py do doctor
```

Expected: all PASS.

- [ ] **Step 4: Commit release**

```bash
git add VERSION SKILL.md manifest.json CHANGELOG.md docs/ROADMAP.md \
  references/VERSION references/manifest.json skills/neon-genie
git status -sb
git commit -m "release: Neon Genie 3.25.0 founder cold-start"
```

---

## Plan self-review

| Spec item | Task |
|-----------|------|
| F1 founder routing + tests | Task 1–2 |
| F2 default job shape + plain example | Task 5 |
| F3 wire capital_sprint (router + recipe) | Task 1–3 |
| F4 hub list to end of SKILL | Task 4 |
| F5 judgment honesty | Task 6 |
| Version / acceptance doctor+eval+dist | Task 7 |
| Placeholders | None — recipe skip path not used; 3a wire is mandatory |
| Venture capital false positive | Test in Task 1 |

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-06-neon-genie-founder-cold-start.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — execute tasks in this session with checkpoints  

Which approach?
