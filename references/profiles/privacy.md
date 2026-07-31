# Privacy Profile

Load with `core` for every Neon Genie run.

## Scope

This profile owns only:

- data-sensitivity classification;
- data minimization;
- egress eligibility;
- redaction or blocking decisions;
- external-action provenance;
- retention and deletion disclosure;
- prevention of unsupported privacy claims.

It does not provide legal certification or replace host/provider policies.

## OPEN

Declare:

- run purpose;
- privacy mode: `local_only`, `external_research_allowed`, or `custom`;
- selected artifact path;
- repository telemetry state;
- known host/model/research providers.

Unknown values are `NOT_COMPUTABLE`.

## ALIGN

Classify each source as:

- `operator_input`;
- `workspace_private`;
- `public_web`;
- `provider_model`.

Classify payload sensitivity as:

- `public`;
- `internal`;
- `personal`;
- `sensitive`;
- `secret`.

Request only fields required for the declared purpose.

## ASCEND

Before every network-capable action, execute conceptually:

```text
RUNE.PRIVACY_EGRESS_CHECK(payload, destination, purpose)
```

Never copy private source material wholesale into a search query. Prefer abstracted, minimized queries.

## CLEAR

Block promotion when:

- destination or purpose is unknown;
- secret material may leave the local boundary;
- private material lacks purpose-specific authorization;
- offline mode contains a declared external research action;
- a privacy claim depends on unknown host/provider behavior.

## SEAL

Record:

- privacy mode;
- source classes used;
- known external actions;
- redaction status;
- artifact paths;
- telemetry status;
- retention statement;
- deletion instructions;
- privacy warnings and `NOT_COMPUTABLE` provider fields.

## Prohibited claims

Do not state:

- "your data never leaves your device";
- "zero data collection";
- "fully anonymous";
- "provider does not retain data";
- legal compliance status;

unless directly established for every relevant system.