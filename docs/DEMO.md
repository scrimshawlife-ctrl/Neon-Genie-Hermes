# Neon Genie — 10-minute demo

From zero to a governed packet path. **Advisory only.**

## Prerequisites

- Git, Python 3  
- Hermes (optional for chat; packaging demo is CLI-only)  

## Minute 0–2: Install

```bash
git clone https://github.com/scrimshawlife-ctrl/Neon-Genie-Hermes.git
cd Neon-Genie-Hermes
./install.sh
# → ~/.hermes/skills/neon-genie

python scripts/neon_genie.py do check
```

Expected: `PASS` at current VERSION.

## Minute 2–4: Integrity + gates

```bash
python scripts/neon_genie.py do eval
python scripts/neon_genie.py do transcripts
```

Expected: all golden gates and 5 prose transcripts PASS.

## Minute 4–7: Product-audit recipe

```bash
python scripts/neon_genie.py do recipe --name product-audit --out out/neon-genie/demo-audit
ls out/neon-genie/demo-audit
```

You should see:

- `profile-route.json` — smallest profile set  
- `product-packet.stub.json` — with `completion_proof` + `proof_path`  
- `data-requests.json` — private access request (find/request protocol)  
- `wayfinder-handoff.stub.json` — intent freeze  
- `run-receipt.json` — advisory receipt  

Open the product stub and receipt; note **no execution authority**.

## Minute 7–9: Zero-option honesty

```bash
python scripts/neon_genie.py do recipe --name zero-option --out out/neon-genie/demo-zero
```

Empty skills/access → honest **`NOT_COMPUTABLE`**, not invented capabilities.

## Minute 9–10: Record an outcome (ledger)

```bash
python scripts/neon_genie.py do learn \
  --class proof_failed \
  --summary "demo: no real cash yet; packaging path verified" \
  --source-run out/neon-genie/demo-audit/run-receipt.json \
  --ledger out/neon-genie/learning-ledger.jsonl
```

Ledger entries are **`PROPOSED` only** — never auto-canon.

## Optional: Hermes chat

Reload Hermes, then:

```text
/neon-genie audit this project using product_architecture, commercial,
and wayfinder_handoff. Research decision-critical public facts. Request
private access instead of inventing. Label OBSERVED / INFERRED /
SPECULATIVE / NOT_COMPUTABLE. Do not modify the repository.
```

Compare the run shape to `evals/transcripts/02-product-audit.md`.

## What to say afterward

> Neon Genie is the Hermes skill for governed invention: find or request evidence, seal packets with completion proof, and never grant spend/publish/execute by default.

More: [PREMIERE.md](./PREMIERE.md) · [ROADMAP.md](./ROADMAP.md)
