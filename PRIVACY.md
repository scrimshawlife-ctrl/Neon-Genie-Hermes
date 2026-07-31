# Privacy and Data Handling

Neon Genie is designed to minimize data use and make external data movement visible. This document describes behavior controlled by this repository. It does not replace the privacy terms of Hermes, model providers, search providers, operating systems, or third-party tools.

## Repository-owned guarantees

Neon Genie:

- does not operate an advertising profile;
- does not silently enable repository-owned telemetry;
- does not train a model on operator content;
- writes generated artifacts only to an operator-selected output path;
- does not intentionally transmit private workspace content to public research tools without purpose-specific authorization;
- treats unknown egress, retention, or provider handling as `NOT_COMPUTABLE` rather than making a reassuring claim;
- records declared external actions in the run receipt when the host exposes enough provenance to do so.

## Data categories

A run may process:

1. operator prompts and declared constraints;
2. files or workspace context explicitly made available by the host;
3. public web or registry evidence retrieved through host tools;
4. generated packets, receipts, envelopes, and optional learning-ledger entries.

Neon Genie should request only fields required for the current task. Credentials, secrets, government identifiers, financial account values, private contact lists, health records, and similarly sensitive material must be processed locally where possible and blocked or redacted before external egress.

## External boundaries

Neon Genie runs inside a host environment. The host may invoke a model API, web search, browser, MCP server, or other provider. Those systems can have separate logging, retention, training, and security policies.

Therefore Neon Genie must not claim that data "never leaves the device" unless every invoked component is demonstrably local. A run receipt should identify known providers and destinations and mark unknown provider behavior as `NOT_COMPUTABLE`.

## Privacy modes

### `local_only`

- `research.enabled=false`
- no Neon-Genie-initiated public research;
- artifacts remain in the selected output path;
- host/model processing may still occur unless the host itself is local.

### `external_research_allowed`

- minimized public queries may be sent through host research tools;
- private source content requires explicit, purpose-specific authorization before transmission;
- external actions must be represented in the run receipt when observable.

### `custom`

The operator supplies an explicit allowlist of tool classes, destinations, and data categories.

## Retention and deletion

Neon-Genie-owned persisted data consists of files written to the selected output path and any explicitly selected learning ledger. Neon Genie performs no automatic cloud backup. Delete those files or directories to remove repository-owned persisted run data.

Host applications, model providers, search providers, version-control systems, backups, and operating systems may retain separate copies. Consult those systems' policies and controls.

## Telemetry

Repository-owned telemetry is disabled by default. Any future telemetry must be opt-in, documented with an event schema, and must not include prompt bodies, private file contents, credentials, or raw personal data.

## Training use

Neon Genie does not itself train models and does not intentionally contribute operator content to a training corpus. Model-provider training or improvement use is outside this repository's control and must be evaluated from the selected provider's terms and settings.

## Privacy failure behavior

Before external transmission, the runtime should evaluate:

```text
RUNE.PRIVACY_EGRESS_CHECK(payload, destination, purpose)
```

Allowed outcomes:

- `ALLOW`
- `REDACT_THEN_ALLOW`
- `REQUEST_CONSENT`
- `BLOCK`

Unknown privacy state fails closed. Unsupported assurances are prohibited.

## Reporting a privacy concern

Open a repository issue without including secrets or personal data. For a sensitive report, use GitHub's private vulnerability-reporting channel when enabled.