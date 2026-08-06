# Schema versioning policy

**OBSERVED:** Skill package version (`VERSION` / frontmatter) and **artifact schema
versions** are separate lifecycles as of v3.20.

## Identifiers

Every sealed envelope carries:

```json
{
  "schema_id": "neon-genie/run-envelope",
  "schema_version": "1.1.0"
}
```

Artifact entries may include `schema_id` + `schema_version` when known.

| Artifact | schema_id | Current |
|----------|-----------|---------|
| Run envelope | `neon-genie/run-envelope` | `1.1.0` (additive `privacy` summary) |
| Run receipt | `neon-genie/run-receipt` | `1.0.0` |
| Opportunity packet | `neon-genie/opportunity-packet` | `1.0.0` |
| Product packet | `neon-genie/product-packet` | `1.0.0` |
| Wayfinder handoff | `neon-genie/wayfinder-execution-packet` | `1.0.0` |

JSON Schema files remain flat under `schemas/*.schema.json` (mirrored to
`references/schemas/`). Directory-per-version trees may be introduced later
without breaking envelope discovery.

## Compatibility rules

| Change | Schema version impact |
|--------|------------------------|
| Add optional field | **minor** (1.0.0 → 1.1.0) |
| Tighten validation of optional data | **minor** if still optional |
| New required field / rename / type change | **major** (1.x → 2.0.0) |
| Remove field | **major** |

### Exception — envelope `1.1.0` privacy (W1 privacy spine)

Envelope schema version **1.1.0** intentionally treats the top-level `privacy`
summary object as **required** for packaging emission and validation, while
shipping as a **minor** bump (not 2.0.0). Rationale:

- Skill package **3.24.0+** always co-loads the privacy profile and emits
  envelope `schema_version: 1.1.0` with a `privacy` object on every packaging run.
- Pre-3.24 consumers and older sample envelopes may lack `privacy`; treat that
  as a transitional gap, not a supported long-term shape.
- Packaging CLI validation (`NG-PRIV-004`) fails when `schema_version >= 1.1.0`
  and `privacy` is missing. Current packaging always writes `1.1.0`.

This is a documented one-time exception for the privacy spine; future *required*
fields still follow the major-bump rule above.

## Support window

- Wayfinder (and other consumers) **must** accept the current major schema_version
  for `run-envelope`.
- Previous major: best-effort for one skill minor series, then drop.
- Packaging CLI validates current major only unless `--schema` points at an older file.

## Migrations

When a major envelope change ships:

1. Document in CHANGELOG under Schema.
2. Add `schemas/migrations/README.md` note (or a script) describing field moves.
3. Keep previous `run-envelope` schema file renamed if dual validation is required.

## Canonical consumer path

1. Open `run-envelope.json` in the run directory.
2. Read `primary_artifact.path` for the main packet.
3. Read `receipt_path` / `receipt` for gates and DataRequests.
4. If `wayfinder.handoff_path` is set, load that packet for execution planning.
5. Refuse execution if `authority != advisory_only` or `grants_execution == true`
   when originating from Neon Genie.
