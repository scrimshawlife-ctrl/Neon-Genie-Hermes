# Neon Genie Quickstart

Governed Hermes skill for invention, product architecture, and opportunity intelligence. **Advisory only.**

## Install

From a clone of this repository:

```bash
./install.sh
# → ~/.hermes/skills/neon-genie
```

Or copy the **repository root** (not a nested package) into your Hermes skills directory.

Validate:

```bash
python scripts/neon_genie.py do check
# after install:
python ~/.hermes/skills/neon-genie/scripts/neon_genie.py do check
```

### Packaging CLI (optional)

```bash
python scripts/neon_genie.py do route --text "product audit wayfinder handoff"
python scripts/neon_genie.py do validate --packet ./packet.json --type product
python scripts/neon_genie.py do receipt --profiles core,product_architecture --out receipt.json
python scripts/neon_genie.py do eval
python scripts/neon_genie.py do transcripts
python scripts/neon_genie.py do recipe
python scripts/neon_genie.py help
```

Packaging only — does not invent opportunities or grant execution authority.

`do eval` runs golden gate fixtures under `evals/cases/`.  
`do transcripts` checks golden prose exemplars under `evals/transcripts/`.  
`do learn` appends outcome observations to a local learning ledger (PROPOSED only).

```bash
python scripts/neon_genie.py do learn \
  --class proof_obtained \
  --summary "first paid diagnostic booked" \
  --ledger out/neon-genie/learning-ledger.jsonl
```

Post-SEAL checklist: `references/post-seal-verification.md`.  

```bash
python scripts/neon_genie.py do recipe --list
python scripts/neon_genie.py do recipe --name product-audit
python scripts/neon_genie.py do recipe --name zero-option
python scripts/neon_genie.py do recipe --name zero-option-executable
python scripts/neon_genie.py do recipe --name fragmentation
python scripts/neon_genie.py do validate --packet examples/packets/sample-receipt.packet.json --type receipt --strict-authority
```

Restart Hermes or reload skills after install.

## First prompts

**Product audit + handoff**

```text
/neon-genie audit this project using product_architecture, commercial,
and wayfinder_handoff. Research anything decision-critical via host tools.
Operator files rank highest; label OBSERVED / INFERRED / SPECULATIVE /
NOT_COMPUTABLE. Do not modify the repository.
```

**Zero-capital loop**

```text
/neon-genie zero_option: first cash within 7 days from existing skills and
access only. No fictional resources. Mark unknowns NOT_COMPUTABLE.
```

**Offline (no live research)**

```text
/neon-genie ... research.enabled=false
```

Example briefs: `examples/`. Request envelope: `templates/request.yaml`.  
Golden prose exemplars: `evals/transcripts/` (how a full OPEN→SEAL run should look).

## Missing data

1. **Find** public / fetchable facts via host research tools.
2. **Request** private or operator-held facts with a `DataRequest` (never invent).
3. Only then **`NOT_COMPUTABLE`** — with attempted query and/or open request id.

Schema: `schemas/data-request.schema.json`. Sample: `examples/packets/sample-data-request.json`.

## How it runs

```text
OPEN → ALIGN → ASCEND → CLEAR → SEAL
```

Core is always loaded. Other profiles load on trigger match. Research is proactive by default when host tools can close gaps.

## Profiles

| Profile | When |
|---------|------|
| `core` | Always |
| `product_architecture` | Product/system design |
| `opportunity_mining` | New venture / blocked transition |
| `fragmentation` | Handoffs / incompatible systems |
| `zero_option` | Zero capital / first cash |
| `agentic_services` | Agents / x402 |
| `commercial` | Pricing / buyer / revenue |
| `evidence_intelligence` | External facts / grants / competitive |
| `memetic` | Names / hooks / pitch |
| `audit_delivery` | Client audit / cost of inaction |
| `wayfinder_handoff` | Engineering handoff packet |

Contracts: `profiles/`. Schemas: `schemas/`. Runtime rules: `references/hermes-runtime-contract.md`.

## Authority

Neon Genie may research, model, score, draft, and recommend. It may **not** spend, publish, modify repos, or grant execution authority without explicit downstream authorization.

## Layout (skill root)

```text
SKILL.md  manifest.json  VERSION  install.sh
profiles/  schemas/  references/  templates/
examples/  evals/  scripts/
```

Full overview: `README.md`. Roadmap: `docs/ROADMAP.md`.
