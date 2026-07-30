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
python scripts/validate_hermes_skill.py
# after install:
python ~/.hermes/skills/neon-genie/scripts/validate_hermes_skill.py
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
