# Neon Genie Wave P0 — Evidence Spine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Codify find → request private → NOT_COMPUTABLE as Neon Genie’s evidence spine (DataRequest schema, doctrine, anti-overclaim gates, golden evals, receipt fields) at v3.8.0.

**Architecture:** Prose + packaging only. Extend SKILL/runtime contract/anti-overclaim for the Evidence Request Protocol; add `schemas/data-request.schema.json` and document receipt fields; add deterministic gate evaluators in `run_hermes_evals.py` that simulate find/request decisions from fixture inputs. No Python product brain.

**Tech Stack:** Markdown skill contracts, JSON Schema, Python 3 stdlib evals/CLI (existing).

**Spec:** `docs/superpowers/specs/2026-07-30-neon-genie-premiere-program-design.md` §7–8 (Wave P0)

## Global Constraints

- Priority stack: Evidence-seeking honesty → Outcomes → Category
- Conflict rule: find public → request private → only then NOT_COMPUTABLE; never invent OBSERVED
- Authority remains `advisory_only`
- No Kubrick domain content
- Version target: **3.8.0**
- Skill name: `neon-genie`
- Stdlib-only scripts; CI must stay green via `do check` + `do eval` + packaging tests
- P1–P3 (transcripts, learning ledger, manifesto) are **out of scope**

---

## File map

| Path | Action | Responsibility |
|------|--------|----------------|
| `schemas/data-request.schema.json` | Create | DataRequest artifact contract |
| `schemas/run-receipt.schema.json` | Modify | Document `data_requests`, `open_blocking_requests`, `research_attempts` |
| `SKILL.md` | Modify | Evidence Request Protocol + research rules + SEAL |
| `references/hermes-runtime-contract.md` | Modify | Find/request/offline policy |
| `references/anti-overclaim-patterns.md` | Modify | Gates P–R (skip-find, silent-private, request-less NC) |
| `evals/cases/public-gap-must-attempt-research.json` | Create | Find obligation |
| `evals/cases/private-gap-must-request.json` | Create | DataRequest obligation |
| `evals/cases/private-gap-silent-invent.json` | Create | Silent invent fails |
| `scripts/run_hermes_evals.py` | Modify | Evaluators for new cases |
| `scripts/run_fixture_invariants.py` | Modify | Required case list |
| `scripts/build_receipt.py` | Modify | Optional `--data-request` / list open requests |
| `scripts/recipe_run.py` or recipe example | Modify | Surface open DataRequest in one recipe path |
| `examples/packets/sample-data-request.json` | Create | Sample valid DataRequest |
| `VERSION`, `manifest.json`, `CHANGELOG.md`, `README.md`, `docs/ROADMAP.md`, `evals/rubric.md`, `references/GOLDEN_TESTS.md` | Modify | v3.8.0 + docs |
| `scripts/validate_hermes_skill.py` | Modify | Require data-request schema path |

---

### Task 1: DataRequest schema + sample packet

**Files:**
- Create: `schemas/data-request.schema.json`
- Create: `examples/packets/sample-data-request.json`
- Modify: `schemas/run-receipt.schema.json`

**Interfaces:**
- Produces: schema with required fields matching premiere design

- [ ] **Step 1: Write `schemas/data-request.schema.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Data Request",
  "type": "object",
  "required": [
    "field",
    "why_decision_critical",
    "sensitivity",
    "suggested_source",
    "blocks_promotion",
    "status"
  ],
  "properties": {
    "field": { "type": "string", "minLength": 1 },
    "why_decision_critical": { "type": "string", "minLength": 1 },
    "sensitivity": {
      "type": "string",
      "enum": ["public", "operator", "private"]
    },
    "suggested_source": { "type": "string" },
    "blocks_promotion": { "type": "boolean" },
    "status": {
      "type": "string",
      "enum": ["open", "satisfied", "waived"]
    },
    "request_id": { "type": "string" },
    "attempted_queries": { "type": "array" },
    "satisfied_by": { "type": "string" }
  },
  "additionalProperties": true
}
```

- [ ] **Step 2: Write `examples/packets/sample-data-request.json`**

```json
{
  "request_id": "dr-001",
  "field": "buyer_budget_authority",
  "why_decision_critical": "Commercial packet cannot separate buyer vs beneficiary without budget authority",
  "sensitivity": "private",
  "suggested_source": "Operator CRM or declared stakeholder interview notes",
  "blocks_promotion": true,
  "status": "open",
  "attempted_queries": []
}
```

- [ ] **Step 3: Extend `schemas/run-receipt.schema.json` properties** (keep existing required; add documented properties):

```json
"data_requests": { "type": "array" },
"open_blocking_requests": { "type": "array" },
"research_attempts": { "type": "array" },
"evidence_protocol": {
  "type": "string",
  "enum": ["find_request_not_computable"]
}
```

- [ ] **Step 4: Validate sample**

```bash
python scripts/neon_genie.py do validate --packet examples/packets/sample-data-request.json --schema schemas/data-request.schema.json
```

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add schemas/data-request.schema.json schemas/run-receipt.schema.json examples/packets/sample-data-request.json
git commit -m "feat(schema): add DataRequest and receipt evidence fields"
```

---

### Task 2: Golden eval fixtures + evaluators (TDD)

**Files:**
- Create: `evals/cases/public-gap-must-attempt-research.json`
- Create: `evals/cases/private-gap-must-request.json`
- Create: `evals/cases/private-gap-silent-invent.json`
- Modify: `scripts/run_hermes_evals.py`
- Modify: `scripts/run_fixture_invariants.py`
- Modify: `evals/rubric.md`, `references/GOLDEN_TESTS.md`

**Interfaces:**
- Produces: evaluators returning dicts that subset-match `expected`

- [ ] **Step 1: Write fixtures**

`evals/cases/public-gap-must-attempt-research.json`:

```json
{
  "input": {
    "gap": "competitor_public_pricing",
    "sensitivity": "public",
    "host_tools_available": true,
    "research_attempted": false,
    "claim_label_emitted": "OBSERVED"
  },
  "expected": {
    "status": "GATE_FAIL",
    "gate": "P",
    "reason": "Public gap requires research attempt before OBSERVED or NOT_COMPUTABLE"
  }
}
```

`evals/cases/private-gap-must-request.json`:

```json
{
  "input": {
    "gap": "internal_unit_economics",
    "sensitivity": "private",
    "host_tools_available": true,
    "data_request_emitted": false,
    "blocks_decision": true
  },
  "expected": {
    "status": "GATE_FAIL",
    "gate": "Q",
    "reason": "Private decision-critical gap requires DataRequest"
  }
}
```

`evals/cases/private-gap-silent-invent.json`:

```json
{
  "input": {
    "gap": "closed_crm_pipeline",
    "sensitivity": "private",
    "data_request_emitted": false,
    "claim_label_emitted": "OBSERVED",
    "claim_source": "model_prior_only"
  },
  "expected": {
    "status": "GATE_FAIL",
    "gate": "R",
    "reason": "Silent invent of private facts as OBSERVED is forbidden"
  }
}
```

Also add **positive** cases for pass paths:

`evals/cases/public-gap-research-attempted.json`:

```json
{
  "input": {
    "gap": "competitor_public_pricing",
    "sensitivity": "public",
    "host_tools_available": true,
    "research_attempted": true,
    "research_outcome": "fetched",
    "claim_label_emitted": "OBSERVED"
  },
  "expected": {
    "status": "PASS",
    "gate": "P"
  }
}
```

`evals/cases/private-gap-request-open.json`:

```json
{
  "input": {
    "gap": "internal_unit_economics",
    "sensitivity": "private",
    "data_request_emitted": true,
    "blocks_promotion": true,
    "data_request_status": "open",
    "claim_label_emitted": "NOT_COMPUTABLE"
  },
  "expected": {
    "status": "PASS",
    "gate": "Q",
    "promotion_capped": true
  }
}
```

- [ ] **Step 2: Run evals — expect FAIL (missing evaluators)**

```bash
python scripts/neon_genie.py do eval
```

Expected: FAIL on new cases with `no evaluator registered`

- [ ] **Step 3: Add evaluators to `scripts/run_hermes_evals.py`**

```python
def eval_public_gap_must_attempt_research(inp: dict[str, Any]) -> dict[str, Any]:
    sens = str(inp.get("sensitivity") or "")
    tools = bool(inp.get("host_tools_available"))
    attempted = bool(inp.get("research_attempted"))
    label = str(inp.get("claim_label_emitted") or "")
    if sens == "public" and tools and not attempted and label in {"OBSERVED", "NOT_COMPUTABLE", "INFERRED"}:
        # NOT_COMPUTABLE without attempt also fails when tools available
        return {
            "status": "GATE_FAIL",
            "gate": "P",
            "reason": "Public gap requires research attempt before OBSERVED or NOT_COMPUTABLE",
        }
    if sens == "public" and tools and not attempted:
        return {
            "status": "GATE_FAIL",
            "gate": "P",
            "reason": "Public gap requires research attempt before OBSERVED or NOT_COMPUTABLE",
        }
    return {"status": "PASS", "gate": "P"}


def eval_private_gap_must_request(inp: dict[str, Any]) -> dict[str, Any]:
    sens = str(inp.get("sensitivity") or "")
    emitted = bool(inp.get("data_request_emitted"))
    blocks = bool(inp.get("blocks_decision") or inp.get("blocks_promotion"))
    if sens == "private" and blocks and not emitted:
        return {
            "status": "GATE_FAIL",
            "gate": "Q",
            "reason": "Private decision-critical gap requires DataRequest",
        }
    promotion_capped = bool(inp.get("blocks_promotion")) and str(inp.get("data_request_status") or "") == "open"
    return {
        "status": "PASS",
        "gate": "Q",
        "promotion_capped": promotion_capped,
    }


def eval_private_gap_silent_invent(inp: dict[str, Any]) -> dict[str, Any]:
    sens = str(inp.get("sensitivity") or "")
    emitted = bool(inp.get("data_request_emitted"))
    label = str(inp.get("claim_label_emitted") or "")
    source = str(inp.get("claim_source") or "")
    if sens == "private" and not emitted and label == "OBSERVED":
        return {
            "status": "GATE_FAIL",
            "gate": "R",
            "reason": "Silent invent of private facts as OBSERVED is forbidden",
        }
    if sens == "private" and not emitted and source == "model_prior_only" and label == "OBSERVED":
        return {
            "status": "GATE_FAIL",
            "gate": "R",
            "reason": "Silent invent of private facts as OBSERVED is forbidden",
        }
    return {"status": "PASS", "gate": "R"}
```

Register in `EVALUATORS`:

```python
"public-gap-must-attempt-research.json": eval_public_gap_must_attempt_research,
"public-gap-research-attempted.json": eval_public_gap_must_attempt_research,
"private-gap-must-request.json": eval_private_gap_must_request,
"private-gap-request-open.json": eval_private_gap_must_request,
"private-gap-silent-invent.json": eval_private_gap_silent_invent,
```

**Note on public-gap-research-attempted:** When `research_attempted` is true, first function returns PASS. When false + label OBSERVED, FAIL. Ensure positive fixture has `research_attempted: true` so PASS.

**Note on private-gap-must-request positive:** Use `eval_private_gap_must_request` — with `data_request_emitted: true` returns PASS and `promotion_capped: true` when status open + blocks_promotion.

- [ ] **Step 4: Update `REQUIRED_CASES` in `run_fixture_invariants.py`** to include the five new filenames.

- [ ] **Step 5: Update `evals/rubric.md` and `references/GOLDEN_TESTS.md`** with new case rows and gates P–R.

- [ ] **Step 6: Run**

```bash
python scripts/run_fixture_invariants.py
python scripts/neon_genie.py do eval
```

Expected: all PASS (existing 9 + new 5 = 14)

- [ ] **Step 7: Commit**

```bash
git add evals scripts/run_hermes_evals.py scripts/run_fixture_invariants.py references/GOLDEN_TESTS.md
git commit -m "test: evidence spine golden gates P–R (find/request/invent)"
```

---

### Task 3: Doctrine — SKILL, runtime contract, anti-overclaim

**Files:**
- Modify: `SKILL.md`
- Modify: `references/hermes-runtime-contract.md`
- Modify: `references/anti-overclaim-patterns.md`
- Modify: `profiles/core.md` (CLEAR/SEAL bullets for DataRequest)
- Modify: `profiles/evidence_intelligence.md` (request when private)

**Interfaces:**
- Produces: prose operators must follow; references `schemas/data-request.schema.json`

- [ ] **Step 1: Insert into `SKILL.md` after Research rules section** a new section:

```markdown
## Evidence Request Protocol

Priority when a material fact is missing:

1. **Find** — if sensitivity is public (or unknown-but-likely-public) and host tools can run, attempt research; cite or drop.
2. **Request** — if sensitivity is operator/private or access is undeclared, emit a `DataRequest` (`schemas/data-request.schema.json`) instead of inventing.
3. **NOT_COMPUTABLE** — only after find was attempted (or correctly skipped offline) and/or a DataRequest is open or unanswered.
4. **Never** mark model prior as `OBSERVED`.

### DataRequest (required fields)

- `field`, `why_decision_critical`, `sensitivity` (`public`|`operator`|`private`),
  `suggested_source`, `blocks_promotion` (bool), `status` (`open`|`satisfied`|`waived`)

### CLEAR rules

- Public gap + tools available + no research attempt → fail (Gate P)
- Private decision-critical gap + no DataRequest → fail (Gate Q)
- Private/unknown fact labeled OBSERVED from model prior without source → fail (Gate R)
- Open DataRequests with `blocks_promotion: true` cap promotion until satisfied or waived

### SEAL

Run receipt must list `data_requests`, `open_blocking_requests`, and `research_attempts` (may be empty arrays). See `schemas/run-receipt.schema.json`.
```

- [ ] **Step 2: Update Research rules bullet list** to mention request private before NOT_COMPUTABLE.

- [ ] **Step 3: Update mandatory gates** with:
  - public fetchable facts skipped without attempt;
  - private decision-critical facts without DataRequest;
  - silent invent of private facts as OBSERVED.

- [ ] **Step 4: Anti-overclaim** — append gates:

| Gate | Pattern | Repair |
|------|---------|--------|
| **P — Skip find** | Public gap, tools available, no research attempt, claim still asserted or NC without attempt | Run research loop or record attempt failure |
| **Q — Skip request** | Private/operator gap is decision-critical and no DataRequest | Emit DataRequest; block promotion if needed |
| **R — Silent private invent** | Private fact as OBSERVED without source/request | Downgrade; emit request or NOT_COMPUTABLE |

Update header: gates A–O become **A–R**.

- [ ] **Step 5: Runtime contract** — under Research policy add Evidence Request Protocol summary and pointer to schema.

- [ ] **Step 6: profiles/core.md** — in CLEAR, apply gates P–R; in SEAL, emit data_requests on receipt.

- [ ] **Step 7: Commit**

```bash
git add SKILL.md references/hermes-runtime-contract.md references/anti-overclaim-patterns.md profiles/core.md profiles/evidence_intelligence.md
git commit -m "docs(skill): Evidence Request Protocol find/request/NOT_COMPUTABLE"
```

---

### Task 4: Receipt builder + recipe surface

**Files:**
- Modify: `scripts/build_receipt.py`
- Modify: `scripts/recipe_run.py` (e.g. product-audit or commercial-adjacent path)
- Create or update: example receipt with open request under `examples/packets/sample-receipt-with-requests.json`

**Interfaces:**
- `build_receipt.py` accepts `--data-requests path.json` (JSON array or single object)

- [ ] **Step 1: Extend `build_receipt.py`**

Add argparse:

```python
parser.add_argument(
    "--data-requests",
    type=Path,
    help="JSON file: one DataRequest object or array of DataRequests",
)
```

Load requests; validate each has required keys (or call validate_packet logic inline for required fields). Set:

```python
receipt["data_requests"] = requests_list
receipt["open_blocking_requests"] = [
    r for r in requests_list
    if r.get("status") == "open" and r.get("blocks_promotion") is True
]
receipt["research_attempts"] = receipt.get("research_attempts") or []
receipt["evidence_protocol"] = "find_request_not_computable"
```

If open blocking requests exist and status was PROPOSED, keep human_review_required True; optionally note promotion caution in `note` field.

- [ ] **Step 2: Sample receipt**

`examples/packets/sample-receipt-with-requests.json` — full receipt required fields + one open blocking DataRequest.

Validate with:

```bash
python scripts/neon_genie.py do validate --packet examples/packets/sample-receipt-with-requests.json --type receipt --strict-authority
```

- [ ] **Step 3: Recipe** — in `recipe_product_audit` or `recipe_run.recipe_product_audit`, when emitting receipt, include a sample open DataRequest if brief implies missing private access (e.g. product audit without canonical_sources):

```python
data_req = {
    "request_id": "dr-product-access",
    "field": "critical_integration_access",
    "why_decision_critical": "Integration feasibility cannot be OBSERVED without declared access",
    "sensitivity": "private",
    "suggested_source": "Operator environment credentials or access inventory",
    "blocks_promotion": True,
    "status": "open",
}
```

Write `out/data-requests.json` and pass to `build_receipt` via new helper in `recipe_common.build_receipt` (add optional `data_requests` list written to temp file or extend `build_receipt` to accept list by writing temp JSON).

Minimal change to `recipe_common.build_receipt`:

```python
def build_receipt(..., data_requests: list | None = None):
    ...
    if data_requests:
        dr_path = out_path.parent / "_data_requests.json"
        write_json(dr_path, data_requests)
        args.extend(["--data-requests", str(dr_path)])
```

- [ ] **Step 4: Test**

```bash
python scripts/neon_genie.py do recipe --name product-audit --out out/neon-genie/p0-product-audit
# receipt should contain data_requests
python scripts/test_wave3_cli.py
```

- [ ] **Step 5: Commit**

```bash
git add scripts/build_receipt.py scripts/recipe_common.py scripts/recipe_run.py examples/packets/
git commit -m "feat: surface DataRequests on receipts and product-audit recipe"
```

---

### Task 5: Version 3.8.0, docs, skill validator, CI sanity

**Files:**
- `VERSION` → `3.8.0`
- `manifest.json`, `SKILL.md` frontmatter version
- `CHANGELOG.md`, `README.md` badges/version, `QUICKSTART.md` (evidence protocol one-liner)
- `docs/ROADMAP.md` — premiere waves + P0 shipping
- `scripts/validate_hermes_skill.py` — require `schemas/data-request.schema.json`
- `docs/README.md` — link premiere spec + this plan

- [ ] **Step 1: Bump versions to 3.8.0** consistently.

- [ ] **Step 2: CHANGELOG entry** for 3.8.0 (DataRequest, gates P–R, evals, receipt fields).

- [ ] **Step 3: ROADMAP** — add Premiere Program section:

```markdown
## Premiere program (post packaging waves)

See `docs/superpowers/specs/2026-07-30-neon-genie-premiere-program-design.md`.

| Wave | Status |
|------|--------|
| P0 Evidence spine | shipping 3.8.0 |
| P1 Prose excellence | planned |
| P2 Outcome density | planned |
| P3 Category ownership | planned |
```

- [ ] **Step 4: QUICKSTART** — short “Missing data” box:

```markdown
## Missing data

1. Neon tries to **find** public facts (research).
2. If private, it **requests** via DataRequest (does not invent).
3. Only then `NOT_COMPUTABLE`.
```

- [ ] **Step 5: Full verify**

```bash
python scripts/neon_genie.py do check
python scripts/run_fixture_invariants.py
python scripts/neon_genie.py do eval
python scripts/test_wave3_cli.py
python scripts/audit_release_version.py --strict
```

Expected: all PASS; eval count ≥ 14.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "release: Evidence Request Protocol Wave P0 (v3.8.0)"
```

- [ ] **Step 7: Optional operator steps (after approval)**

```bash
./install.sh
git push && gh pr create ...
```

---

## Spec coverage self-review

| P0 requirement | Task |
|----------------|------|
| Doctrine find/request/NC | Task 3 |
| Runtime contract + anti-overclaim P–R | Task 3 |
| data-request.schema.json | Task 1 |
| Receipt fields | Task 1 + 4 |
| Golden evals public/private/offline | Task 2 (+ existing offline case) |
| run_hermes_evals evaluators | Task 2 |
| VERSION 3.8.0 + ROADMAP | Task 5 |
| Recipe/receipt surface DataRequest | Task 4 |
| No Python invention engine | Global constraints |
| advisory_only / no Kubrick merge | Global constraints |

## Placeholder scan

None intentional. Evaluator code and schemas are complete in-plan.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-30-neon-genie-evidence-spine-p0.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — execute tasks in this session with checkpoints  

Which approach?
