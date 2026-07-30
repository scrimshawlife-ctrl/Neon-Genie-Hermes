# Neon Genie Roadmap

Sibling skill to Kubrick: **shared architecture patterns**, separate domain (opportunity / product intelligence, not cinematic engineering).

## Wave 1 — Ops shell

Installable skill root, Hermes runtime contract, `install.sh`, VERSION/CHANGELOG/QUICKSTART, smoke validator, examples + evals skeleton, flatten nested package.

**Status:** shipped as **v3.2.0**.

## Wave 2 — Domain depth

- Thicken profile contracts
- Fill missing packet schemas (`EvidenceIntelligencePacket`, `MemeticPressurePacket`, `AuditDeliveryPacket`)
- Richer golden/eval cases and anti-overclaim references

**Status:** shipped as **v3.3.0**.

## Wave 3 — Thin operator surface

Optional packaging CLI only (no product brain in Python):

```text
python scripts/neon_genie.py do check | validate | route | receipt
```

**Status:** shipped as **v3.4.0**.

## Wave 4 — Release maturity

CI evals workflow, release checklist, version audit, fixture invariants.

**Status:** shipped as **v3.5.0**.

## Wave 5 — Executable evals + recipes

- Deterministic golden gate runner (`do eval`) comparing case `expected` to gate logic
- Product-audit packaging recipe (`do recipe`) for first operator path
- CI artifacts from recipe output

**Status:** shipped as **v3.6.0**.

## Wave 6 — Recipe family + deeper validation

- Multi-recipe dispatcher (product-audit, zero-option variants, fragmentation)
- Typed packet validation subset + strict authority checks
- Expanded golden gates (fictional resource, scorecard override ban)
- Sample packets for offline validation demos

**Status:** shipped as **v3.7.0**.

## Premiere program (post packaging waves)

See `docs/superpowers/specs/2026-07-30-neon-genie-premiere-program-design.md`.

| Wave | Status |
|------|--------|
| P0 Evidence spine | shipping 3.8.0 |
| P1 Prose excellence | planned |
| P2 Outcome density | planned |
| P3 Category ownership | planned |

## Non-goals (all waves)

- Merging Neon Genie and Kubrick domains
- Auto-execution, spending, or canon promotion
- Shared monorepo runtime library (revisit only after Wave 2 if a third skill needs a scaffold)
