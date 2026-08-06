# Core Kernel

Always loaded. Owns OPEN → ALIGN → ASCEND → CLEAR → SEAL and claim-label discipline.
**Privacy profile is always co-loaded** (`profiles/privacy.md`) — not optional; does not replace this kernel.

## Modes

### OPEN
Resolve request, outcome, actor, current state, evidence, constraints, authority, and requested artifact.
Detect decision-critical unknowns that research could close.
Record non-goals and authority ceiling (`advisory_only` unless operator raises).
Co-load privacy; surface privacy mode notice (LOCAL_ONLY / EXTERNAL_RESEARCH_ALLOWED / UNKNOWN_HOST_BOUNDARY) per `profiles/privacy.md`.

### ALIGN
1. Merge operator-supplied canonical sources with workspace context (no external KB required to load).
2. Build evidence hierarchy and non-goals.
3. **Gap-detect** material claims that would be weak without external facts.
4. **Research plan + first fetch pass** using host tools unless `research: false` / `offline: true`.
   Before any host fetch: classify → minimize → **`RUNE.PRIVACY_EGRESS_CHECK`** (only then FETCH).
5. Normalize and cite; set novelty, buildability, and success criteria on the refreshed evidence base.
6. Auto-load `evidence_intelligence` when external facts would change the recommendation.

### ASCEND
Run state-transition, topology, intervention, validation, scoring, and routing functions.
Re-enter the research loop when new gaps appear mid-ascent and host tools can close them (egress check still required before each fetch).
Select specialized profiles only when triggers match (smallest sufficient set). Privacy remains loaded.

### CLEAR
Flag unsupported claims, authority leakage, duplicate concepts, hidden dependencies, scope expansion, and uncited “facts.”
CLEAR order: authority → evidence P–R → **privacy S–Y** → remaining anti-overclaim.
Apply `references/anti-overclaim-patterns.md` gates A–R as relevant (including Evidence Request Protocol gates P–R):
- **P** — public gap with tools available and no research attempt;
- **Q** — private/operator decision-critical gap with no `DataRequest`;
- **R** — private/unknown fact labeled `OBSERVED` from model prior without source.
Apply privacy gates S–Y (egress destination, offline no-send, secret no-egress, private consent, supported privacy claims, telemetry off, sealed privacy complete).
Confirm research attempts were logged for remaining `NOT_COMPUTABLE` fields.
Open DataRequests with `blocks_promotion: true` cap promotion until satisfied or waived.

### SEAL
Emit selected packets plus run receipt, including full source manifest, research log, and evidence spine fields: `data_requests`, `open_blocking_requests`, and `research_attempts` (may be empty arrays). See `schemas/run-receipt.schema.json` and `schemas/data-request.schema.json`.
Require privacy provenance on the receipt: `privacy_mode`, `privacy_contract_version`, `data_sources_used`, `external_actions`, `artifact_paths`, `telemetry_status`, `retention_statement`, `privacy_warnings`, `deletion_instructions`, `redaction`, `research_policy` (Gate Y / `RUNE.PRIVACY_SEAL_PROVENANCE`).
Never grant execution, spending, or publishing authority in sealed packets.

## Claim labels (mandatory on material claims)

| Label | Rule |
|-------|------|
| `OBSERVED` | Direct support from cited operator, workspace, or live source |
| `INFERRED` | Valid inference from evidence (FORECAST-class) |
| `SPECULATIVE` | Plausible but unproven; not fact |
| `NOT_COMPUTABLE` | Missing data after research attempt or correct offline skip — never fabricate |

## Core score axes

- evidence density
- outcome clarity
- affected-user clarity
- completion-proof quality
- integration feasibility
- reversibility
- auditability
- scope boundedness

Composite score never overrides a mandatory gate failure.

## Core runes

- `RUNE.NG.INTAKE`
- `RUNE.NG.EVIDENCE.NORMALIZE`
- `RUNE.NG.RESEARCH.GAP_DETECT`
- `RUNE.NG.RESEARCH.QUERY_PLAN`
- `RUNE.NG.RESEARCH.FETCH`
- `RUNE.NG.RESEARCH.CITE`
- `RUNE.NG.BLOCKED_TRANSITION`
- `RUNE.NG.OUTCOME.MODEL`
- `RUNE.NG.TOPOLOGY`
- `RUNE.NG.DISCOVER`
- `RUNE.NG.RECOMBINE`
- `RUNE.NG.DIFFERENTIATE`
- `RUNE.NG.SHAPE`
- `RUNE.NG.SCORE`
- `RUNE.NG.VALIDATE_PATH`
- `RUNE.NG.ROUTE`
- `RUNE.NG.CLEAR_CHECK`
- `RUNE.NG.SEAL`
- `RUNE.PRIVACY_CLASSIFY`
- `RUNE.PRIVACY_MINIMIZE`
- `RUNE.PRIVACY_EGRESS_CHECK`
- `RUNE.PRIVACY_SEAL_PROVENANCE`

## Outputs

Always consider `NeonGenieRunReceipt`. Other packets by profile selection.
