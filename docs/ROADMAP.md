# Neon Genie Roadmap

Sibling skill to Kubrick: **shared architecture patterns**, separate domain (opportunity / product intelligence, not cinematic engineering).

## Wave 1 — Ops shell (current)

Installable skill root, Hermes runtime contract, `install.sh`, VERSION/CHANGELOG/QUICKSTART, smoke validator, examples + evals skeleton, flatten nested package.

**Status:** shipped as **v3.2.0** (branch `feat/ops-shell-wave1`).

## Wave 2 — Domain depth

- Thicken profile contracts
- Fill missing packet schemas (`EvidenceIntelligencePacket`, `MemeticPressurePacket`, `AuditDeliveryPacket`)
- Richer golden/eval cases and anti-overclaim references

## Wave 3 — Thin operator surface

Optional packaging CLI only (no product brain in Python):

```text
neon-genie do check | validate | route | receipt
```

## Wave 4 — Release maturity

CI evals workflow, release checklist, default install as peer of Kubrick in operator environments.

## Non-goals (all waves)

- Merging Neon Genie and Kubrick domains
- Auto-execution, spending, or canon promotion
- Shared monorepo runtime library (revisit only after Wave 2 if a third skill needs a scaffold)
