# Neon Genie Privacy-by-Construction Spine — Design Spec

**Date:** 2026-08-06  
**Status:** Shipped as **3.24.0** (`v3.24.0`); integrated with privacy runtime [#17](https://github.com/scrimshawlife-ctrl/NeonGenie/pull/17)  
**Repo:** [NeonGenie](https://github.com/scrimshawlife-ctrl/NeonGenie)  
**Baseline skill version:** 3.23.0  
**Target skill version:** 3.24.0  
**Implements:** [issue #15](https://github.com/scrimshawlife-ctrl/NeonGenie/issues/15) P0–P2 (+ runtime from #17)  
**Approach:** Doctrine + deterministic packaging spine (not a Python research proxy)

**Ship note:** Packaging uses `scripts/privacy_runtime.py` with receipt/envelope
`privacy-context` and modes such as `local_only` (envelope remains
`schema_version` **1.0.0**). Earlier draft “envelope 1.1.0 privacy summary object”
was superseded by the #17 runtime shape while keeping dual-enforcement NG-PRIV
gates, always-on `privacy` profile, and human contract docs from this design.

---

## 1. Program context

### 1.1 Multi-wave improvement program

| Wave | Theme | Timing |
|------|--------|--------|
| **W1** | Privacy & trust spine (this spec) | First; blocking foundation |
| **W2** | Operator outcomes (proof, post-SEAL, learn loops, handoff payload depth) | Parallel with W3 after W1 |
| **W3** | Judgment quality (capability router, profiles/transcripts, optional live multi-turn evals) | Parallel with W2 after W1 |
| **W4** | Distribution & adoption (catalog polish, announce, install UX) | After W2 ∥ W3 |

```text
W1 Privacy
    ↓
W2 Outcomes  ∥  W3 Judgment
    ↓
W4 Distribution
```

### 1.2 Locked constraints (all waves)

- **Wayfinder** remains an **optional handoff consumer** only. Never a load-time or runtime dependency. Absence never blocks advisory work, doctor, privacy checks, or recipes.
- **Authority** remains `advisory_only` / `grants_execution: false` (ADR 0001).
- **Product brain** stays in `SKILL.md` + profiles (ADR 0002). Packaging CLI does not invent strategy or run host research.
- **No merge** with Kubrick domain; no auto-spend, auto-publish, or auto canon promotion.

### 1.3 W1 depth

Full issue #15: P0 trust docs + receipt/envelope provenance + egress doctrine; P1 privacy profile + secret/PII preflight + UX notices + evals; P2 `do privacy` / doctor extension.

---

## 2. Intent & scope

### 2.1 Goals

| Code | Goal |
|------|------|
| **T1** | Operators can answer *what entered / what left / where artifacts live / what is unknown* without reading source |
| **T2** | Repository-owned telemetry stays **off by default** and is inspectable |
| **T3** | Offline / `research.enabled=false` is test-covered and records **zero** Neon-initiated external research sends |
| **T4** | Likely secrets/credentials cannot silently ride outbound research queries (packaging preflight + doctrine) |
| **T5** | Privacy claims always separate **Neon guarantees** from **host/provider** behavior; unknown → `NOT_COMPUTABLE`, never a warm-blanket claim |

### 2.2 In scope

- Root `PRIVACY.md` + hub-safe mirror under `references/`
- README / QUICKSTART / DEMO trust surfaces + privacy badge
- ADR `docs/adr/0006-privacy-by-construction.md`
- `profiles/privacy.md` always co-loaded with `core`
- Receipt + envelope privacy provenance fields; envelope schema `1.1.0`
- Egress rune + gates S–Y in `gates.yaml` / anti-overclaim patterns
- Deterministic secret/PII preflight (`scripts/privacy_preflight.py`, stdlib)
- Behavioral + unit evals; doctor + `do privacy`
- Distribution spine / hub parity
- Stable field contracts for W2 ∥ W3 consumers

### 2.3 Out of scope

- Legal compliance certification
- Replacing Hermes / model / search / MCP vendor privacy policies
- Python research proxy or automatic network calls from the CLI
- Making Wayfinder required
- W2 outcome density, W3 router/LLM evals, W4 announce/catalog
- Absolute “never leaves your device” claims unless every layer is provably local
- Advertising, profiling, or silent usage collection

---

## 3. Architecture

### 3.1 Boundary rule (hard)

Neon Genie can **guarantee** only repository-owned behavior:

| Guaranteed by Neon | Not guaranteed (disclose only) |
|--------------------|--------------------------------|
| Files it writes under operator-selected output paths | Hermes host retention / logging |
| Its own telemetry flag (default **off**; no collector in-repo) | Model provider training / logs |
| Doctrine + CLEAR gates + packaging validation | Search / web / MCP tool vendor policies |
| What it records on the receipt | OS, browser, cloud IDE, or third-party side channels |
| Deterministic secret preflight on strings/paths it is asked to check | Memory of an already-running remote model session |

Unsupported privacy state → `NOT_COMPUTABLE` and/or `privacy_warnings[]`. Never invent “private.”

### 3.2 Layers

```text
Operator (prompts, files, workspace, flags)
        │
        ▼
Hermes prose runtime (Tier 0)
  SKILL.md + core + privacy
  OPEN → ALIGN → ASCEND → CLEAR → SEAL
  RUNE.PRIVACY_EGRESS_CHECK before host research/tool
        │                              │
        │ local only                   │ ALLOW / REDACT_THEN_ALLOW
        ▼                              ▼
Operator out/ path              Host tools (optional)
packets, receipt,               web / search / fetch / MCP
envelope, ledger*               = external boundary

* learning ledger: explicit operator `do learn` only
```

### 3.3 Privacy modes

| Mode | Meaning |
|------|---------|
| `LOCAL_ONLY` | Research disabled / offline; no Neon-initiated external research **sends**; `external_actions` empty or only `sent: false` deny records |
| `EXTERNAL_RESEARCH_ALLOWED` | Host research may run; every egress attempt passes egress check and is logged |
| `UNKNOWN_HOST_BOUNDARY` | Host cannot confirm offline enforcement or provider policy; do not claim LOCAL_ONLY absolutes; warn |

Packaging recipes that never call host tools still emit privacy provenance (defaults: `LOCAL_ONLY`, telemetry disabled, empty external actions).

### 3.4 Profile loading

```text
core     — always
privacy  — always co-loaded with core (not optional; not a legal mega-profile)
…specialized profiles — smallest sufficient set (unchanged)
wayfinder_handoff — only when handoff requested; Wayfinder runtime still optional
```

`privacy` must not widen authority, invent compliance certifications, replace other profiles’ domain logic, or auto-load Wayfinder.

### 3.5 Dual enforcement (honest)

| Path | What enforces privacy |
|------|------------------------|
| Live Hermes run | Doctrine in SKILL + `profiles/privacy.md` + gates; agent logs `external_actions` / redaction on receipt |
| Packaging CLI | Builds/validates privacy fields; secret preflight; doctor / `do privacy`; golden/behavioral fixtures |
| Neither | May control a frontier model’s own logging — disclosed as host boundary |

### 3.6 Wayfinder

- Neon may emit `WayfinderExecutionPacket` and envelope pointers.
- Wayfinder is not loaded for doctor/privacy and is not an egress destination of the skill itself.
- Pushing packets into a remote Wayfinder service is operator/host action; if recorded at all, it is an explicit external action outside default Neon guarantees.

---

## 4. Artifacts & schema contracts

### 4.1 Documents

| Artifact | Role |
|----------|------|
| `PRIVACY.md` (repo root) | Canonical human contract: data-flow, categories, Neon vs host, retention/deletion, telemetry, training, offline, research disclosure, contact |
| `references/PRIVACY.md` | Hub-safe mirror of the same contract (Hub allowlists `references/`, not arbitrary roots); must stay content-aligned with root `PRIVACY.md` |
| `docs/adr/0006-privacy-by-construction.md` | ADR: doctrine + packaging spine; no Python research proxy |
| README | Badge + short **Privacy & Data Handling** near top; link to contract; restrained copy |
| QUICKSTART / DEMO | Compact privacy notice before first prompt example |
| `references/schema-versioning.md` | Document envelope `1.0.0` → `1.1.0` additive privacy |

### 4.2 Data categories

1. `operator_input` — prompts, pasted text, attached files  
2. `workspace_private` — local repo/files Hermes can read  
3. `public_web` — fetched/search results  
4. `provider_model` — content sent to the model host  
5. Neon artifacts — packets, receipt, envelope, optional learn ledger under operator `out/…` (retention: local paths)

### 4.3 Run receipt privacy provenance

Extend `schemas/run-receipt.schema.json` and hub mirror. Packaging skeletons always populate. SEALED hermes-quality receipts require these fields:

| Field | Rules |
|-------|--------|
| `privacy_mode` | `LOCAL_ONLY` \| `EXTERNAL_RESEARCH_ALLOWED` \| `UNKNOWN_HOST_BOUNDARY` |
| `privacy_contract_version` | Semver of privacy contract text; start `1.0.0` |
| `data_sources_used` | Subset of categories actually used; packaging with brief/recipe defaults include `operator_input` |
| `external_actions` | Array of egress records (see §4.4) |
| `artifact_paths` | Resolved paths Neon wrote this run |
| `telemetry_status` | Const `disabled` in W1; any other value fails validation |
| `retention_statement` | Non-empty; must not claim host retention is zero |
| `privacy_warnings` | Strings/codes (e.g. `UNKNOWN_PROVIDER_RETENTION`, `HOST_OFFLINE_NOT_ENFORCEABLE`) |
| `deletion_instructions` | Path-oriented operator steps |
| `redaction` | `{ enabled, blocked_categories, events }` |
| `research_policy` | `{ enabled, offline }` mirroring operator flags |

**Relationship to evidence spine:** Successful external research appears in both `research_attempts` and `external_actions`. Blocked preflight may appear only in `external_actions` + `redaction.events`.

### 4.4 `external_actions[]` item shape

```json
{
  "action_id": "ea_001",
  "timestamp": "ISO-8601",
  "tool_or_provider": "web_search | page_fetch | mcp:<name> | model:<provider> | other",
  "destination": "domain or provider id or unknown",
  "purpose": "short why",
  "data_categories": ["operator_input"],
  "payload_redacted": true,
  "outcome": "ALLOW | REDACT_THEN_ALLOW | REQUEST_CONSENT | BLOCK",
  "sent": false,
  "consent_ref": null
}
```

Rules:

- `sent: true` only for `ALLOW` / `REDACT_THEN_ALLOW` after check.
- `destination: "unknown"` + `sent: true` → CLEAR fail (Gate S).
- Credentials/secrets category never `sent: true`.
- Remote model sends: log `model:<provider>` with `provider_model` category; if provider unknown, do not claim local-only privacy.

### 4.5 Run envelope `1.1.0`

Bump `schema_version` to `1.1.0`. Add required summary object (full detail on receipt):

```json
"privacy": {
  "privacy_mode": "LOCAL_ONLY",
  "privacy_contract_version": "1.0.0",
  "telemetry_status": "disabled",
  "research_enabled": false,
  "external_action_count": 0,
  "receipt_privacy_complete": true
}
```

- Packaging always emits `1.1.0`.
- Consumers may treat missing `privacy` as pre-3.24.
- Samples and recipes updated so doctor / envelope tests pass.

### 4.6 Version triad

| Version | Tracks |
|---------|--------|
| Skill `3.24.0` | Release shipping this spine |
| `privacy_contract_version` `1.0.0` | Text + field semantics of privacy guarantee |
| Envelope `schema_version` `1.1.0` | Envelope shape including `privacy` summary |

### 4.7 Learning ledger

Still PROPOSED / explicit `do learn` only. Does not set `telemetry_status` to enabled. Ledger path appears in deletion instructions when used.

### 4.8 Optional UX artifact

Optional `privacy-notice.txt` beside envelope; if written, listed in `artifact_paths`.

---

## 5. Gates, profile, egress, preflight

### 5.1 Privacy profile duties

| Duty | Behavior |
|------|----------|
| Sensitivity classify | Tag inputs: public / operator / private / secret-like |
| Field minimization | Smallest queries; DataRequest for private; no wholesale workspace dump to tools |
| Egress eligibility | `RUNE.PRIVACY_EGRESS_CHECK` before host research/tool use |
| Provenance | SEAL receipt privacy fields + `external_actions` |
| Disclosure | OPEN notice; forbid unsupported absolute privacy claims |
| Deletion/retention language | Point at `artifact_paths` + host boundary |

### 5.2 Egress rune

```text
RUNE.PRIVACY_EGRESS_CHECK(payload, destination, purpose, data_categories)
  → ALLOW | REDACT_THEN_ALLOW | REQUEST_CONSENT | BLOCK
```

Research loop:

```text
GAP_DETECT → QUERY_PLAN → PRIVACY_EGRESS_CHECK → FETCH → NORMALIZE → CITE → LABEL
```

`REQUEST_CONSENT` requires operator affirmation for that purpose before send; record `consent_ref` when later allowed.

Additional runes: `RUNE.PRIVACY_CLASSIFY`, `RUNE.PRIVACY_MINIMIZE`, `RUNE.PRIVACY_SEAL_PROVENANCE`.

### 5.3 New gates (S–Y)

| Gate | Name | Blocking when | Remediation |
|------|------|---------------|-------------|
| **S** | `egress_destination_known` | `sent: true` and destination unknown/empty | Block send; log BLOCK |
| **T** | `offline_no_external_send` | LOCAL_ONLY / research disabled but `sent: true` | Fail CLEAR |
| **U** | `secret_no_egress` | Credential/secret-like payload would be or was sent | BLOCK; never OBSERVED from leaked secret |
| **V** | `private_egress_needs_consent` | Private/operator egress without consent_ref | REQUEST_CONSENT or keep local |
| **W** | `privacy_claim_must_be_supported` | Absolute privacy claim without matching mode + evidence | NOT_COMPUTABLE / warning |
| **X** | `telemetry_off_unless_opt_in` | `telemetry_status != disabled` in W1 | Force disabled; fail validate |
| **Y** | `sealed_receipt_privacy_complete` | SEAL without required privacy provenance | Complete receipt before SEAL |

Register in `references/gates.yaml` and `references/anti-overclaim-patterns.md`. CLEAR order: authority → evidence P–R → privacy S–Y → remaining anti-overclaim.

### 5.4 Secret / PII preflight

Module: `scripts/privacy_preflight.py` (stdlib; used by doctor, validate, tests).

Detect with high-precision bias for secrets (fail closed on API keys / PEMs); best-effort for broader PII:

- `credentials`, `secrets`, `passwords_connection`
- `government_ids`, `financial`, `contact_lists`, `precise_geo`, `special_category` (best-effort; documented)

API shape:

```text
preflight(text) -> {
  findings: [{ category, span_hint, severity }],
  blocked_categories: [...],
  safe_for_egress: bool,
  redacted_text: optional
}
```

Default: credentials/secrets **BLOCK** for external queries; private lists need consent for enrichment; local packet drafting still allowed when the operator task requires it. Does not scan whole disk unless paths are explicitly passed.

### 5.5 UX notices

**LOCAL_ONLY:**

```text
Privacy mode: LOCAL_ONLY
External research: disabled
Artifacts: <resolved output path>
Telemetry: disabled
```

**EXTERNAL_RESEARCH_ALLOWED:**

```text
Privacy mode: EXTERNAL_RESEARCH_ALLOWED
Only minimized queries may leave the workspace.
Private source content requires explicit approval before transmission.
Telemetry: disabled
```

**UNKNOWN_HOST_BOUNDARY:** research-allowed notice plus warning that offline/host retention is not enforceable by Neon.

### 5.6 Packaging CLI

| Job | Behavior |
|-----|----------|
| `do privacy` | Report contract version, artifact root if known, telemetry, research flags, redaction availability, offline requested vs host-enforceable, unknown retention |
| `do doctor` | Privacy checks: contract present, schema fields, telemetry const, sample envelope 1.1.0, preflight self-test on canned secret (must BLOCK) |
| receipt / envelope builders | Privacy defaults for non-research packaging |
| `do validate` | Privacy subschema; reject telemetry enabled; reject LOCAL_ONLY + sent actions |
| `do run` recipes | Always write privacy-complete receipt + envelope 1.1.0 |

No new network calls in CLI.

### 5.7 SKILL.md updates

- Profile router: `privacy: always` (with core).
- Research loop includes egress check.
- SEAL requires privacy provenance fields.
- Runes listed in §5.2.

---

## 6. Tests, distribution, parallel interfaces, rollout

### 6.1 Behavioral cases

| # | Case | Asserts |
|---|------|---------|
| 1 | Offline / research disabled | LOCAL_ONLY; no `sent: true` |
| 2 | Public market query | Minimized research allowed; action logged |
| 3 | Pasted API key | BLOCK; Gate U |
| 4 | Private customer list | Consent required; Gate V |
| 5 | Receipt external actions | Every allowed fetch logged |
| 6 | Telemetry | Remains disabled; Gate X |
| 7 | Unknown provider retention | Absolute claim → NOT_COMPUTABLE / warning; Gate W |
| 8 | Deletion | Instructions + artifact_paths cover Neon outputs |
| 9 | Learning ledger | Explicit path only; not telemetry |
| 10 | Hub contract | Contract + schemas present in hub layout doctor |

### 6.2 Unit / packaging tests

- `scripts/test_privacy_preflight.py` — secrets BLOCK; benign product text passes; redaction strips bearer tokens
- Envelope tests — `1.1.0` + `privacy` summary from builders
- Validate fixtures — LOCAL_ONLY + sent fails; missing privacy fields fail SEAL validate
- Doctor / `do privacy` — green on clean tree; fail if contract missing
- Existing suites stay green with updated samples

Optional prose golden transcript is nice-to-have, not blocking.

### 6.3 Distribution

- Update `distribution.yaml`; run `distribution_spine.py write`
- Hub package includes privacy contract mirror, profile, schemas, scripts, evals
- `do doctor` green on hub layout and full tree
- Catalog / distribution docs note privacy contract path

### 6.4 Stable interfaces for W2 ∥ W3

| Contract | W2 Outcomes | W3 Judgment |
|----------|-------------|-------------|
| `privacy_mode` | No outcomes that required silent private egress | Prefer local-safe routing when LOCAL_ONLY |
| `external_actions[]` | Proof paths only from logged fetches | Score research quality on logged attempts |
| `data_sources_used` | completion_proof / learn cite allowed sources | evidence_intelligence only when research policy allows |
| `privacy_warnings[]` | Surface on outcome packets | Live evals mark host-boundary unknowns |
| `telemetry_status` | Learn ledger stays explicit | Eval harnesses add no silent telemetry |
| Gates S–Y | Post-SEAL includes privacy completeness | Multi-turn evals include secret-block + offline |
| `do privacy` | Gate “publish demo” on clean report | CI capability surface |

W4 reuses public copy only; no new guarantees without a privacy_contract bump.

### 6.5 Implementation order (inside W1)

1. PRIVACY.md + references mirror + ADR 0006 + README/QUICKSTART/DEMO  
2. Schema 1.1.0 envelope + receipt privacy fields + samples  
3. privacy profile + SKILL/core/gates/anti-overclaim + runes  
4. `privacy_preflight.py` + validate/receipt/envelope wiring  
5. `do privacy` + doctor hooks  
6. Behavioral evals 1–10 + unit tests  
7. `distribution_spine write` + hub doctor green  
8. VERSION 3.24.0 + CHANGELOG + ROADMAP note  

Single release **3.24.0**. Do not claim “private by construction” publicly until doctor + evals pass.

### 6.6 Acceptance criteria

- [ ] New user understands collection, egress, retention, training, deletion via README → PRIVACY.md  
- [ ] Telemetry verifiably `disabled` in schemas/defaults/tests  
- [ ] Offline mode test-covered; zero `sent: true` under LOCAL_ONLY  
- [ ] Every successful external action visible on receipt  
- [ ] Likely credentials blocked from egress preflight + Gate U case  
- [ ] Private material needs consent before egress (Gate V case)  
- [ ] Claims distinguish Neon vs host; unknown → NOT_COMPUTABLE / warnings  
- [ ] Hub mirror includes contract, profile, schemas, tests  
- [ ] README restrained; no absolute “never leaves device”  
- [ ] Wayfinder still optional; advisory_only unchanged  

### 6.7 Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Operators think LOCAL_ONLY means the model is local | UNKNOWN_HOST_BOUNDARY + Gate W + PRIVACY.md host section |
| Preflight false positives on product specs | High-precision secrets first; PII best-effort; local drafting allowed |
| Agents ignore doctrine | Behavioral evals + Gate Y sealed completeness |
| Schema break for old consumers | Additive 1.1.0; missing `privacy` = pre-3.24 |
| Hub omits root PRIVACY.md | Dual ship under `references/` |

---

## 7. Non-goals (restate)

- Legal compliance certification without scoped assessment  
- Replacing host/provider privacy policies  
- Account analytics, advertising identifiers, behavioral profiling, silent usage collection  
- Unverifiable “zero data” or “never leaves device” promises  
- Merging Neon Genie and Kubrick  
- Auto-execution, spending, or canon promotion  
- Requiring Wayfinder for any W1 path  

---

## 8. Success definition

W1 ships when acceptance criteria (§6.6) are met, `do doctor` and privacy evals are green on full tree and hub layout, and W2/W3 can depend on the frozen privacy field names without redefining them.

**Next step after this spec is approved on disk:** invoke writing-plans to produce an implementation plan for W1 only (W2/W3 plans later, post-W1 or as parallel plans that only consume §6.4 interfaces).
