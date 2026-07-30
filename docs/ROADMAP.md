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

## Wave 4 — Release maturity (current)

CI evals workflow, release checklist, version audit, fixture invariants.

**Status:** shipping as **v3.5.0**.

## Non-goals (all waves)

- Merging Neon Genie and Kubrick domains
- Auto-execution, spending, or canon promotion
- Shared monorepo runtime library (revisit only after Wave 2 if a third skill needs a scaffold)
