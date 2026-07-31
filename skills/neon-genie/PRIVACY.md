# Neon Genie Privacy

Neon Genie is private by construction at its repository boundary: repository telemetry is disabled; it does not train models on user content or construct advertising profiles; generated artifacts remain in the output directory chosen by the operator. External research and model calls are host-exposed tools and may have separate data-handling terms. Use `research.enabled=false` / `local_only` for offline-only analysis and inspect the run receipt for declared external actions.

This is a repository guarantee, not a claim about Hermes, model providers, search providers, MCP servers, the operating system, or other host boundaries. Their retention and processing behavior is `NOT_COMPUTABLE` here.

## Defaults

| Control | Value |
|---------|--------|
| Default mode | `local_only` |
| Repository telemetry | `disabled` |
| Training / ads profiles | none by Neon Genie |
| Host/provider retention | `NOT_COMPUTABLE` |
| Egress decisions | `ALLOW` · `REDACT_THEN_ALLOW` · `REQUEST_CONSENT` · `BLOCK` |

## Operator configuration

Briefs and recipes may carry an explicit `privacy:` section (see `templates/request.yaml`). Configuration flows deterministically into:

- `run-receipt.json` (`privacy`, `privacy_mode`, `external_actions`, …)
- `run-envelope.json` (same privacy fields)
- packaging packets generated under the run directory
- local learning-ledger entries (disclosure only; never raw secrets)

There is **no** global “disable privacy” switch. Overrides are **purpose-bound consent records** only (`scope: purpose_bound`).

## External actions

Every recorded external action must include: `provider`, `tool_class`, `destination`, `purpose`, `source_class`, `classification`, `decision` (`ALLOW` or `REDACT_THEN_ALLOW`), `redaction_status`, and `recorded_at` (UTC `YYYY-MM-DDTHH:MM:SSZ`). Private source content is never persisted; `REDACT_THEN_ALLOW` yields a minimized `safe_query`.

## Diagnostics

```bash
python scripts/neon_genie.py do privacy --json
python scripts/test_privacy_runtime.py
```

See also: `references/privacy-contract.md`, `profiles/privacy.md`, `schemas/privacy-context.schema.json`.
