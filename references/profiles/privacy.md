# Privacy Profile

Canonical source: `profiles/privacy.md`.

Load with `core` for every Neon Genie run. Classify source and sensitivity, minimize requested fields, apply `RUNE.PRIVACY_EGRESS_CHECK`, block secrets and unauthorized private-source transmission, and seal privacy provenance into the receipt.

Normative contract: [`../privacy-contract.md`](../privacy-contract.md).

Required outcomes: `ALLOW`, `REDACT_THEN_ALLOW`, `REQUEST_CONSENT`, or `BLOCK`.

Unknown egress, destination, retention, or provider handling is `NOT_COMPUTABLE` and cannot support a privacy assurance.

Do not claim that data never leaves the device, that processing is anonymous, or that a provider does not retain data unless every relevant boundary is directly established.