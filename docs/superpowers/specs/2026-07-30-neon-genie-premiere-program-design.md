# Neon Genie Premiere Program — Design Spec

**Date:** 2026-07-30  
**Status:** Approved for implementation planning (Wave P0 first)  
**Repo:** [NeonGenie](https://github.com/scrimshawlife-ctrl/NeonGenie)  
**Baseline skill version:** 3.7.0  
**Approach:** Evidence spine + quality corpus  

---

## 1. Intent

Define a multi-wave program to make **Neon Genie** the premiere Hermes skill of its type: **governed opportunity and product intelligence** (not cinematic engineering, not generic ideation chat, not execution runtime).

This document is a **program design**. Waves **P0–P3** are shipped (v3.8–3.11). The premiere program is complete; further work is maintenance and corpus depth.

---

## 2. Category definition

| Neon Genie is | Neon Genie is not |
|---------------|-------------------|
| Evidence-bound invention and product/opportunity intelligence | Kubrick (cinematic / symbolic dramaturgy) |
| Advisory, fail-closed, claim-labeled | Wayfinder (work decomposition / eng execution) |
| Hermes-native standalone skill | A Python product-reasoning engine |
| Find public facts; request private facts; never invent | A fantasy idea generator optimized for volume |

**Sibling rule:** Share *architecture patterns* with Kubrick (install, contracts, evals, CLI packaging). Never merge domains.

---

## 3. Goals (locked)

| Code | Goal | Meaning |
|------|------|---------|
| **A** | Trust density | Operators trust Neon under uncertainty more than peer idea/product agents |
| **B** | Outcome density | Packets that survive contact with reality (tests, cash, eng-usable handoffs) |
| **D** | Category ownership | *The* open Hermes skill named for governed invention / opportunity intelligence |

**Not primary:** ecosystem centrality as the top win (Wayfinder/Applied Alchemy integration remains valuable but secondary).

### Priority stack (conflict resolution)

```text
Evidence-seeking honesty  →  Outcome density  →  Category ownership
```

### Conflict rule (operator-stated)

When data is missing:

1. **Find** it if public/fetchable via host tools (proactive research).
2. **Request** it if private / operator-held / behind undeclared access (`DataRequest`).
3. Only then **`NOT_COMPUTABLE`** — with attempted query and/or open request id.
4. **Never invent** missing facts as `OBSERVED`. Model prior is at most `SPECULATIVE` scaffolding.

Silent guessing and sexy demos that skip find/request are both failures.

### Release gate rule

No release may improve Category (docs/demo flash) by weakening Trust (overclaim) or Evidence-seeking (skip find/request).

---

## 4. Premiere thesis

**Neon Genie is the premiere Hermes skill for governed opportunity and product intelligence** when it is the agent operators trust under uncertainty: it closes evidence gaps when it can, asks for what it cannot see, refuses fantasy, and still produces the most useful sealed packets that survive contact with reality.

It does **not** win by inventing more ideas than generic product chat. It wins by being **harder to impress** and **more decision-useful** than any peer in its class.

---

## 5. Success metrics

| Goal | Leading metrics | Lagging metrics |
|------|-----------------|-----------------|
| **Trust** | % material claims labeled; research log completeness; `DataRequest` rate vs silent guess; golden gate correctness | Operator trust (“I would ship this packet”); fewer false `OBSERVED` |
| **Outcomes** | Packets with completion proof; intent-frozen handoffs; recipes with proof paths | Operator-reported tests, cash, eng acceptance of handoffs |
| **Category** | One-liner clarity; install path; demos; comparison vs ideation agents | Installs, stars/forks, “use neon-genie for X” as default phrase |

Packaging maturity (v3.2–3.7 CLI/CI/recipes) is **table stakes**, not the premiere differentiator.

---

## 6. Program architecture (waves)

```text
Wave P0  Evidence doctrine codification (find / request / NOT_COMPUTABLE)
    ↓
Wave P1  Prose excellence — golden transcripts + profile depth for runtime quality
    ↓
Wave P2  Outcome machinery — proof paths, learning memory hooks, post-seal loops
    ↓
Wave P3  Category ownership — manifesto, demos, positioning, install story
```

**Primary work surfaces:** `SKILL.md`, profiles, references, schemas, evals (gates + later transcripts), receipt fields, docs.  
**Not primary:** heavy Python invention/scoring engines.

Existing packaging CLI (`do check|validate|route|receipt|eval|recipe`) supports the program; P0 extends schemas/evals/doctrine, not a new product brain.

---

## 7. Core mechanism — Evidence Request Protocol

### Behaviors

| Situation | Behavior |
|-----------|----------|
| Fact is public + host tools available | **Find** (proactive research); cite or drop |
| Fact is private / behind auth / undeclared access | **Request** via `DataRequest` |
| Offline / tools missing / request unanswered | **`NOT_COMPUTABLE`** with attempted query or pending request id |
| Model fills the hole as fact | **Forbidden** as `OBSERVED`; at most `SPECULATIVE` scaffolding |

### `DataRequest` artifact (design-level fields)

| Field | Purpose |
|-------|---------|
| `field` | What is needed |
| `why_decision_critical` | Why the decision depends on it |
| `sensitivity` | `public` \| `operator` \| `private` |
| `suggested_source` | Where the operator/holder might provide it |
| `blocks_promotion` | If true, promotion cannot rise until satisfied or waived |
| `status` | `open` \| `satisfied` \| `waived` |

### CLEAR / promotion rules

- Open `blocks_promotion: true` requests cap promotion below levels that require that fact.
- Research log must show find attempts for public gaps before `NOT_COMPUTABLE`.
- Private gaps without `DataRequest` are a CLEAR failure (anti-overclaim extension).

### Schema / receipt integration (P0)

- New: `schemas/data-request.schema.json`
- Extend run receipt (and optionally run envelope) to list `data_requests` / `open_blocking_requests`
- Recipes that produce receipts should surface open requests when applicable

---

## 8. Wave definitions

### Wave P0 — Evidence spine (first implementable unit)

**Goal:** Codify and test find / request / NOT_COMPUTABLE so Trust + evidence-seeking are machine-checkable where possible and prose-mandated everywhere.

**In scope:**

1. Doctrine updates in `SKILL.md` (research rules + Evidence Request Protocol).
2. `references/hermes-runtime-contract.md` and `references/anti-overclaim-patterns.md` updates (new gates for silent private invent / skipped find).
3. `schemas/data-request.schema.json`.
4. Run receipt schema fields for data requests (backward-compatible `additionalProperties` already true; document required usage in SEAL).
5. Golden eval cases:
   - public gap + tools assumed → must attempt research (packaging-level simulation of “attempt recorded”);
   - private gap → must emit `DataRequest` with `blocks_promotion` when decision-critical;
   - offline + model prior → no `OBSERVED` from prior only;
   - existing offline / NOT_COMPUTABLE cases remain green.
6. `run_hermes_evals.py` evaluators for new cases.
7. CHANGELOG / VERSION minor bump (e.g. 3.8.0); ROADMAP premiere waves listed.
8. Optional: recipe or receipt example listing open `DataRequest`s.

**Out of scope for P0:** full golden transcripts (P1), learning memory ledger (P2), public manifesto/demo gallery (P3), Python invention engine.

**Success criteria (P0):**

- [x] Doctrine states find → request → NOT_COMPUTABLE explicitly
- [x] `DataRequest` schema exists and is referenced from SKILL/CLEAR
- [x] Receipt guidance includes open data requests
- [x] New golden evals pass in CI via `do eval` (14/14 at v3.8.0)
- [x] No domain merge with Kubrick; authority remains `advisory_only`

**P0 status:** shipped as **v3.8.0**.

### Wave P1 — Prose excellence

- 3–5 golden transcripts (markdown) covering: zero-option empty, product audit, fragmentation, commercial missing buyer, offline audit
- Transcript rubric: labels, research log, DataRequests, SEAL shape, no authority leakage
- Profile depth only where transcripts reveal holes
- Structural transcript checker (`do transcripts` / `scripts/check_transcripts.py`)

**P1 status:** shipped as **v3.9.0** (`evals/transcripts/`, `do transcripts`).

### Wave P2 — Outcome density

- Completion-proof required discipline on opportunity/product/zero-option packets
- Append-only local learning ledger format (PROPOSED observations only; never auto-canon)
- Post-seal verification checklist
- Recipes emit proof paths, not only structural stubs

**P2 status:** shipped as **3.10.0** (`completion_proof`, `do learn`, `references/post-seal-verification.md`).

### Wave P3 — Category ownership

- `docs/PREMIERE.md` (or manifesto): why Neon vs idea-bots
- 10-minute demo path: install → recipe → transcript
- Comparison table; README positioning
- Optional sanitized public example gallery

**P3 status:** shipped as **3.11.0** (`docs/PREMIERE.md`, `docs/DEMO.md`, `examples/gallery/`).

---

## 9. Non-goals (entire program)

- Python opportunity invention / commercial sim engine as the core product
- Auto-spend, auto-outreach, auto-publish, canon promotion
- Merging Neon Genie and Kubrick domains
- Winning by idea volume
- Category marketing that overclaims capability
- Shared monorepo runtime with Kubrick (unless a third skill later forces a scaffold)

---

## 10. Relationship to shipped work (v3.2–3.7)

| Already shipped | Premiere program adds |
|-----------------|------------------------|
| Install, CLI, CI, recipes | Evidence Request Protocol |
| Gate evals (9 fixtures) | Find/request-specific evals + later transcripts |
| Profiles + packet schemas | Receipt/DataRequest coupling; proof-path outcomes |
| Anti-overclaim A–O | Explicit private-invent and skip-find gates |
| Advisory authority | Unchanged — still advisory_only |

---

## 11. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| `NOT_COMPUTABLE` wall feels useless | Find/request first; only fail after attempt; teach requests in QUICKSTART |
| Category demos tempt overclaim | Release gate rule; Trust metrics block ship |
| Scope creep into Python brain | Non-goals; P0–P3 stay doctrine/corpus/outcome fields |
| Private data over-collection | Request only decision-critical fields; public/operator/private sensitivity |

---

## 12. Implementation handoff

1. User reviews this committed spec.
2. On approval → **writing-plans** for **Wave P0 only**.
3. Implement P0 → ship minor version → then plan P1.

---

## 13. Spec self-review record

| Check | Result |
|-------|--------|
| Placeholders / TBD | None material; version example 3.8.0 is explicit target suggestion for P0 |
| Internal consistency | Stack Trust/evidence → Outcomes → Category matches wave order P0→P3 |
| Scope | Program doc + single first unit (P0); P1–P3 deferred |
| Ambiguity | Conflict rule and priority stack made explicit; “Other” operator note encoded as find/request |

---

## Approval

- Goals: A + B + D with evidence-seeking conflict rule  
- Approach: Evidence spine + quality corpus  
- Deliverable: Multi-wave premiere program  
- Design sections 1–7: approved in session 2026-07-30  

**Next:** user review of this file → writing-plans for Wave P0.
