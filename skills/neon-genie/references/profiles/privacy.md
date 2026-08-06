# Privacy Profile

Always co-loaded with `core`. Owns sensitivity classify → minimize → egress check → seal provenance. Does not widen authority, invent compliance certifications, or replace domain profiles.

Human contract: root `PRIVACY.md` and hub mirror `references/PRIVACY.md`. Packaging preflight: `scripts/privacy_preflight.py`.

## Modes (with core)

### OPEN
Emit a privacy notice for the run mode:

| Mode | Notice gist |
|------|-------------|
| `LOCAL_ONLY` | External research disabled; artifacts under operator `out/`; telemetry disabled |
| `EXTERNAL_RESEARCH_ALLOWED` | Only minimized queries may leave; private content needs approval; telemetry disabled |
| `UNKNOWN_HOST_BOUNDARY` | Research-allowed notice **plus** offline/host retention not enforceable by Neon |

Never claim absolute “never leaves your device” without a fully local stack proof.

### ALIGN / research
1. **`RUNE.PRIVACY_CLASSIFY`** — tag payload sensitivity: `public` | `operator` | `private` | secret-like.
2. **`RUNE.PRIVACY_MINIMIZE`** — smallest sufficient query; no wholesale workspace dump to tools; private facts → `DataRequest`, not silent fetch.
3. **`RUNE.PRIVACY_EGRESS_CHECK`** — before every host research/tool send.
4. Proceed to FETCH only on `ALLOW` / `REDACT_THEN_ALLOW` (after consent when required).

### CLEAR
Apply privacy gates **S–Y** after authority and evidence P–R (see `references/anti-overclaim-patterns.md`, `references/gates.yaml`):

- **S** — `sent: true` requires known destination  
- **T** — `LOCAL_ONLY` / research disabled ⇒ no `sent: true`  
- **U** — credentials/secret-like never egress  
- **V** — private/operator egress needs `consent_ref`  
- **W** — absolute privacy claims need matching mode + evidence  
- **X** — `telemetry_status` must be `disabled` (W1)  
- **Y** — sealed receipt must carry complete privacy provenance  

### SEAL
`RUNE.PRIVACY_SEAL_PROVENANCE` — run receipt must include (non-empty semantics; arrays may be empty where allowed):

- `privacy_mode`
- `privacy_contract_version`
- `data_sources_used`
- `external_actions`
- `artifact_paths`
- `telemetry_status` (`disabled`)
- `retention_statement`
- `privacy_warnings`
- `deletion_instructions`
- `redaction`
- `research_policy`

Envelope privacy summary (when present) must agree with receipt. Successful external research appears in both `research_attempts` and `external_actions`.

## Egress rune

```text
RUNE.PRIVACY_EGRESS_CHECK(payload, destination, purpose, data_categories)
  → ALLOW | REDACT_THEN_ALLOW | REQUEST_CONSENT | BLOCK
```

| Outcome | Meaning |
|---------|---------|
| `ALLOW` | Minimized, non-secret payload; destination known; log and may send |
| `REDACT_THEN_ALLOW` | Strip blocked spans; log redaction events; may send only redacted form |
| `REQUEST_CONSENT` | Private/operator material; need operator affirmation + `consent_ref` before send |
| `BLOCK` | Secret-like, unknown destination with intent to send, offline violation, or unsafe preflight — log `sent: false` |

`sent: true` only for `ALLOW` / `REDACT_THEN_ALLOW` after check. Destination `"unknown"` + `sent: true` → fail Gate S.

Research loop (with core):

```text
GAP_DETECT → QUERY_PLAN → PRIVACY_EGRESS_CHECK → FETCH → NORMALIZE → CITE → LABEL
```

## Runes

- `RUNE.PRIVACY_CLASSIFY`
- `RUNE.PRIVACY_MINIMIZE`
- `RUNE.PRIVACY_EGRESS_CHECK`
- `RUNE.PRIVACY_SEAL_PROVENANCE`

## Forbidden absolute claims

Do **not** assert without matching `privacy_mode` + evidence:

- “Never leaves your device” / “fully private” / “zero host retention”
- “Never used for training” (host/provider may train — disclose only)
- Telemetry “on” or silent usage collection (repo telemetry stays off)

Unsupported state → `NOT_COMPUTABLE` and/or `privacy_warnings[]` — never invent “private.”

## Non-goals

- Not legal counsel or compliance certification (GDPR/CCPA/etc. as product claims)
- Does not replace Hermes / model / search / MCP vendor policies
- Does not proxy host research in Python; does not scan whole disk unless paths are passed
- Does not auto-load Wayfinder; Wayfinder is outside Neon’s privacy boundary
- Does not widen `advisory_only` authority

## Outputs

Privacy fields ride on `NeonGenieRunReceipt` and envelope `privacy` summary. No separate privacy packet.
