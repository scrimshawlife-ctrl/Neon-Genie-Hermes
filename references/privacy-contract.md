# Neon Genie Privacy Contract

Contract status: normative

## Invariants

1. **Minimize** — process only data required for the declared run purpose.
2. **Constrain purpose** — do not reuse run data for profiling, advertising, enrichment, or unrelated learning.
3. **No silent telemetry** — repository telemetry defaults to `disabled`.
4. **No Neon Genie training use** — operator content is not used to train a model by this repository.
5. **Local-first persistence** — files are written only to an operator-selected path.
6. **Explicit egress** — network-capable actions must be attributable in receipts when observable.
7. **Private-source containment** — private source content is not transmitted externally without explicit purpose-specific approval.
8. **Redact before egress** — credentials, secrets, government identifiers, financial values, and similarly sensitive fields are blocked or redacted.
9. **Retention transparency** — distinguish repository-owned files from host/provider retention.
10. **Offline semantics** — `research.enabled=false` prohibits Neon-Genie-initiated research and requires zero declared external research actions.
11. **No dark patterns** — privacy language must be plain and no stronger than implemented behavior.
12. **Fail closed** — unknown egress, destination, retention, or provider policy is `NOT_COMPUTABLE` and cannot support a privacy assurance.

## Required run context

```json
{
  "privacy": {
    "contract_version": "1.0.0",
    "mode": "local_only",
    "telemetry": "disabled",
    "training_use": "none_by_neon_genie",
    "retention": {
      "artifact_path": "operator_selected",
      "automatic_expiry": null
    },
    "egress": {
      "allowed": false,
      "approved_domains": [],
      "approved_tool_classes": []
    },
    "redaction": {
      "enabled": true,
      "blocked_categories": [
        "credentials",
        "secrets",
        "government_ids"
      ]
    }
  }
}
```

## RUNE.PRIVACY_EGRESS_CHECK

Input:

```text
(payload, destination, purpose, privacy_context)
```

Output:

```text
ALLOW | REDACT_THEN_ALLOW | REQUEST_CONSENT | BLOCK
```

Decision order:

1. Unknown destination or purpose → `BLOCK`.
2. Credential, secret, or prohibited identifier detected → `BLOCK`.
3. Private-source content required externally without explicit authorization → `REQUEST_CONSENT`.
4. Sensitive fields removable without degrading the task → `REDACT_THEN_ALLOW`.
5. Public, minimized payload allowed by context → `ALLOW`.
6. Any unresolved state → `BLOCK`.

## Receipt requirements

A sealed run should report:

- privacy mode;
- data-source classes used;
- external actions and destinations;
- whether payloads were minimized or redacted;
- artifact paths;
- telemetry status;
- retention statement;
- privacy warnings;
- deletion instructions;
- unknown provider behavior as `NOT_COMPUTABLE`.

## Boundary statement

This contract governs Neon-Genie-owned logic and artifacts. It cannot guarantee the behavior of Hermes, model APIs, search engines, MCP servers, operating systems, backups, or other host facilities. Those boundaries must be named, not silently inherited.