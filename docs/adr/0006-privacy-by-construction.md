# ADR 0006 — Privacy by construction

## Status

Accepted

## Context

Operators cannot tell from the skill alone what leaves the machine, whether
telemetry exists, or how to delete artifacts. Epistemic gates (P–R) are not
privacy guarantees.

## Decision

1. Privacy is a first-class skill contract (`PRIVACY.md` + `profiles/privacy.md`
   always with core).
2. Packaging CLI emits privacy provenance on receipts/envelopes and validates
   LOCAL_ONLY / telemetry rules.
3. Deterministic preflight blocks high-confidence secrets from egress text.
4. Neon does **not** proxy host research in Python; host/provider retention is
   disclosed, not claimed.
5. Wayfinder remains optional; not part of the privacy boundary.

## Consequences

- Envelope schema 1.1.0 requires a privacy summary.
- Hub installs ship `references/PRIVACY.md`.
- Absolute “never leaves device” claims are forbidden without full local stack proof.
