# Neon Genie skill audit — design (360 + follow-on wave)

**Date:** 2026-08-06  
**Skill version audited:** 3.24.0  
**Status:** design approved for implementation planning  
**Approach:** Hybrid 360 matrix (operator fitness · loadability · enforcement)  
**Deliverable type:** Findings map + scoped design for top fixes (no code in this doc)

---

## 1. Purpose, scope, success

### Purpose

Produce a **360 health map** of Neon Genie across three axes, then a **scoped follow-on design** for the **top 3–5 fixes only**. This is a decision and design artifact, not an implementation change set.

### Audience context (from product intent)

People in transitional states building something of their own with limited resources. They need help developing ideas fully — detailed roadmaps, approaches/resources, or both. Primary install path: Hermes Skills Hub. Tone: utilitarian, helpful.

### In scope

- **Operator fitness** — transitional founders; roadmap / approaches under constraint  
- **Loadability** — what Hermes loads (`SKILL.md`, profiles, hub list, dual-path)  
- **Enforcement integrity** — what dry tooling proves vs what only the LLM can honor  
- Evidence: docs/contracts + dry tooling on this clone

### Out of scope

- Live multi-turn Hermes LLM evals (deferred; already on roadmap)  
- Marketing rewrites unrelated to skill behavior  
- New product domains (e.g. Kubrick merge)  
- Auto-execution / spend authority  
- Full profile-by-profile literary rewrite  
- Privacy authority model changes  

### Success criteria

1. Every finding has: axis · severity · evidence · audience impact  
2. Ranked punch list (risk × audience)  
3. Top fixes each have: goal, non-goals, surfaces, acceptance checks  
4. Spec is reviewable without re-running the audit  
5. Explicit “do nothing / later” bucket so green packaging is not “fixed” for sport  

### Non-goals of the fixes design

- Shipping code in the same step as the audit  
- Expanding gate ontology without a founder-path justification  
- ML or host-level routing outside this skill  

---

## 2. Dry tooling baseline (2026-08-06)

| Check | Result |
|-------|--------|
| `python3 scripts/neon_genie.py do doctor` | **PASS** (all smokes green) |
| `python3 scripts/neon_genie.py do eval` | **19/19 PASS** |
| `python3 scripts/distribution_spine.py verify` | **PASS** (146 hub support files; mirrors OK) |
| `do privacy --json` | `LOCAL_ONLY`, repository telemetry disabled |

**Conclusion:** Packaging and fixture enforcement are healthy. Residual risk is mostly **operator cold-start**, **contract load order**, and **judgment not covered by CI**.

---

## 3. Findings (hybrid 360)

Severity: H / M / L. Audience impact is scored for transitional founders with limited resources.

### Axis A — Operator fitness

| ID | Finding | Sev | Evidence |
|----|---------|-----|----------|
| **O1** | Cold-start router misses founder language | **H** | Natural brief *“I'm between jobs with limited money and need a roadmap for my app idea”* → packaging router selects only `core`, `privacy`. Keyword paths like “zero capital first cash” and “product audit” do fire profiles. |
| **O2** | Public promise vs skill voice gap | **M** | Landing/README sell stuck-idea → testable plan. Skill operating voice is runes, promotion ladders, x402, Zero State — dense for the stated audience. Doctrine is sound; intake framing is operator-ops. |
| **O3** | Zero-option path exists but is opt-in by phrase | **M** | Strong evals/transcripts for zero-capital honesty. Without trigger phrases, founders may never load the profile that blocks fictional resources. |
| **O4** | `capital_sprint` is a partial orphan | **M** | Thickest profile (~106 lines); brief + schema ship; **not** in `profile_router` or `route_profiles.py`; **no** entry in `RECIPES`. Hub list includes the profile file — false completeness. |

### Axis B — Loadability

| ID | Finding | Sev | Evidence |
|----|---------|-----|----------|
| **L1** | `SKILL.md` carries a huge generated hub manifest | **M** | ~573 lines; ~147 lines / ~7KB are auto-generated hub support paths early in the file. |
| **L2** | Always-on + auto-load pressure | **M** | `core` + `privacy` always; `evidence_intelligence` auto when external facts help — correct doctrinally, multiplies held context after OPEN. |
| **L3** | Dual tree is healthy but expensive | **L** | Dist spine PASS; root↔hub parity OK. Maintenance cost only. |
| **L4** | Privacy profile ultra-thin vs long contracts | **L/M** | `profiles/privacy.md` ≈ 5 lines; full contract in long docs. Packaging enforces well; judgment still needs the long path. |

### Axis C — Enforcement integrity

| ID | Finding | Sev | Evidence |
|----|---------|-----|----------|
| **E1** | Green suite proves packaging, not judgment | **H** (context) | Doctor/eval/dist green prove install integrity, schemas, fixture gates, privacy packaging, recipes — **not** free-chat claim labeling or live research quality. |
| **E2** | Router packaging ≠ Hermes chat routing | **M** | `route_profiles.py` is packaging-only. Chat depends on `SKILL.md` router text the model may under-follow. |
| **E3** | Gate registry incomplete vs prose gates | **L** | `gates.yaml` has a partial id set; SKILL prose lists more. Fine if intentional; risky if treated as complete. |

### Ranked punch list (risk × audience)

1. **O1** — Cold-start / natural-language routing  
2. **O2** — Founder-facing intake + default job shape  
3. **O4** — Close or wire `capital_sprint`  
4. **L1** — Slim what Hermes must read first (hub list placement)  
5. **O3** — Discoverable constrained-resource path without jargon  
6. **E1/E2** — Document judgment gap; live evals later  
7. **L2–L4, E3, L3** — later / monitor  

### Explicit do-nothing / later

- Privacy authority model  
- Dual-tree architecture rewrite  
- Full gate YAML auto-generation from prose  
- Live multi-turn Hermes CI (keys / host tools)  
- Marketing-only copy passes  
- “Fixing” green packaging recipes for greenness alone  

---

## 4. Follow-on wave: “Founder cold-start + contract honesty”

Five fixes. No new product domains. No privacy model change. Default for orphan profile: **wire** (`capital_sprint`), not demote.

### F1 — Founder-language routing (O1, O3, E2)

**Goal:** Natural transitional-founder language selects a useful smallest profile set without requiring skill jargon.

**Behavior**

- Extend `PROFILE_TRIGGERS` in `scripts/route_profiles.py` **and** `profile_router` in `SKILL.md` (must stay aligned).  
- Phrase families (case-insensitive substring), illustrative not exhaustive:

  | Intent | Example phrases | Profiles to add (smallest sufficient) |
  |--------|-----------------|----------------------------------------|
  | Develop idea / roadmap | roadmap, business idea, go into business, for myself, solo, side project, launch my, turn my idea, app idea, product idea, what should I build | `opportunity_mining`; + `product_architecture` only if product/app/system language present |
  | Scarcity / first cash | limited money/resources/capital, between jobs, bootstrapped, no budget, first revenue, make money from | `zero_option` |
  | Approach help | how do I approach, where do I start, next steps for my idea | `opportunity_mining` |

- Always keep `core` + `privacy`.  
- Do not dump all profiles.  
- Add packaging tests: table of plain-English strings → expected `selected` sets, including the O1 sample brief.  
- Avoid weak single-token over-triggers (e.g. bare “app”); prefer multi-word phrases or WEAK_TRIGGERS discipline.

**Non-goals:** ML router; Hermes host changes; inventing new profiles.

**Acceptance**

- O1 sample selects at least `core`, `privacy`, `opportunity_mining`.  
- When scarcity language is present, also `zero_option`.  
- Existing keyword paths (product audit, zero capital first cash) still pass.  
- `do doctor` / `do eval` remain green.

### F2 — Default “stuck idea” job shape (O2, O3)

**Goal:** Cold Hermes load knows the default job for a person with an idea under constraint.

**Behavior**

- Add a short section in `SKILL.md` **after Mission and before Research doctrine** titled for transitional builders / default operator job:

  1. Name the stuck point and what “done” looks like  
  2. Capture constraints (time, money, skills) — never invent resources  
  3. Find public → request private → label claims  
  4. Emit roadmap **and/or** approach options with completion proof  
  5. Remain advisory-only  

- Cross-link `opportunity_mining` + `zero_option` as the usual pair for constrained solo builders.  
- Add one plain-English example prompt in `SKILL.md` and/or `QUICKSTART.md` (not only recipe/CLI style).  
- Optional (same wave if cheap): one golden prose transcript for the O1-style brief.

**Non-goals:** Rewriting all profiles to founder voice; redoing the GitHub Pages site.

**Acceptance**

- A reader of `SKILL.md` alone can answer: “What should Neon Genie do for a solo founder with an idea and limited money?”  
- Example prompt is copy-pasteable into Hermes.

### F3 — Wire `capital_sprint` (O4) — option 3a

**Goal:** No half-shipped surface.

**Behavior**

- Add `capital_sprint` to `profile_router` in `SKILL.md` with clear triggers (capital sprint, impact object, time-bounded capital, campaign card, etc.).  
- Mirror triggers in `route_profiles.py`.  
- Prefer **wire** over demote.  
- Optional low-cost: `do recipe --name capital-sprint` stub consistent with other recipes + doctor smoke only if recipe is added.  
- If recipe is deferred, document that packaging recipe is not yet first-class but router path is.

**Demote alternative (not default):** mark experimental and stop implying parity — only if maintainers reject wire.

**Acceptance**

- `route_profiles.py --text "capital sprint impact campaign"` includes `capital_sprint`.  
- Brief `examples/capital-sprint.brief.yaml` preferred_profiles still work.  
- No silent orphan: profile is routable **or** explicitly experimental (not both undefined).

### F4 — Load-path slimming (L1)

**Goal:** Operating doctrine appears before the long hub path dump without breaking Hub install.

**Behavior**

- Keep the generated hub support list **byte-correct** and regenerated via `distribution_spine`.  
- **Relocate** the generated hub support block to the **end** of `SKILL.md` (after Registry and memory), so mission, router, authority, and gates load first for the model.  
- Do **not** delete the list unless Hub path-reference rules are re-verified; Hub requires explicit path references under allowlisted dirs.  
- Re-run `distribution_spine verify` (and write if the spine asserts block position).

**Non-goals:** Deleting dual tree; cutting profiles; moving doctrine into a separate file Hermes won’t load.

**Acceptance**

- Human reading top of `SKILL.md` hits identity → mission → default job (F2) → research → router before the hub path dump.  
- Dist spine + hub package parity PASS.

### F5 — Judgment-gap honesty (E1, E2) — docs only

**Goal:** Green doctor/eval cannot be mistaken for full behavioral coverage.

**Behavior**

- Add a short subsection (README and/or PREMIERE / CONTRIBUTING): **What tooling proves vs what Hermes must still do**  
  - Proves: install integrity, schemas, fixture gates, privacy packaging, recipes, distribution  
  - Does not prove: live research quality, free-chat claim labeling, multi-turn judgment  
- Point to deferred live Hermes evals on the roadmap.

**Acceptance**

- A contributor cannot reasonably claim “19/19 evals = chat-safe judgment complete.”

---

## 5. Architecture, flow, rollout

### Components touched

| Unit | Role | Fixes |
|------|------|-------|
| `scripts/route_profiles.py` | Packaging router | F1, F3 |
| Router unit tests (new/extend) | Founder phrase table | F1 |
| `SKILL.md` | Chat contract: router, default job, hub block position | F1–F4 |
| `scripts/recipe_run.py` | Optional capital-sprint recipe | F3 |
| `QUICKSTART.md` / `README.md` | Plain example + judgment honesty | F2, F5 |
| `docs/PREMIERE.md` or `CONTRIBUTING.md` | Optional judgment honesty home | F5 |
| `distribution_spine` | Verify after SKILL edits | F4 |

### Routing data flow (unchanged spine)

```text
operator text
  → match triggers (packaging CLI and/or SKILL.md router)
  → always: core + privacy
  → + specialized profiles (smallest sufficient)
  → load profile contracts
  → OPEN → ALIGN → ASCEND → CLEAR → SEAL
```

### Implementation order

```text
F4 (move hub list)
F1 (router + tests)  ── parallel with F3 (capital_sprint)
F2 (default job shape; after F1 language is known)
F5 (docs honesty)
```

### Wave acceptance (implementation)

- `do doctor` PASS  
- `do eval` 19/19 (or updated count if cases added)  
- `distribution_spine verify` PASS  
- New router tests green  
- Manual re-run of O1 string shows non-empty specialized profiles  

### Versioning note

Design does not mandate a version number. Implementation plan may ship as **3.25.0** if user-visible routing/contract behavior changes.

### Error / edge cases

- Over-triggering: enforce smallest sufficient set; WEAK_TRIGGERS for dangerous single tokens  
- False zero_option: scarcity must be real resource language, not “venture capital” alone without constraint  
- Hub install: never remove required path references without verifying Hub rules  

---

## 6. Spec self-review

| Check | Result |
|-------|--------|
| Placeholders / TBD | None material; F3 recipe optional is explicit |
| Consistency | F3 default is wire (3a); demote is alternate only |
| Scope | Single wave of five fixes; live LLM evals deferred |
| Ambiguity | O1 acceptance criteria and F4 “move not delete” are explicit |

---

## 7. Next step

After user review of this file: invoke **writing-plans** to produce  
`docs/superpowers/plans/2026-08-06-neon-genie-founder-cold-start.md` (or dated equivalent) with task-level implementation steps.
