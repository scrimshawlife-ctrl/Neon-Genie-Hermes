# Neon Genie examples

Illustrative request briefs and sample packets for Hermes / packaging CLI.  
They are **not** execution authority.

## Install

```bash
./install.sh
```

## Briefs

| File | Use |
|------|-----|
| `product-audit.brief.yaml` | Product architecture + commercial + wayfinder handoff |
| `zero-option.brief.yaml` | Empty skills/access → honest `NOT_COMPUTABLE` |
| `zero-option-with-skills.brief.yaml` | Declared skills → micro-loop stub |
| `fragmentation.brief.yaml` | Multi-portal friction / defrag scan |

## Sample packets

| File | Validate |
|------|----------|
| `packets/sample-opportunity.packet.json` | `do validate --type opportunity` |
| `packets/sample-receipt.packet.json` | `do validate --type receipt --strict-authority` |

## Packaging recipes

```bash
python scripts/neon_genie.py do recipe --list
python scripts/neon_genie.py do recipe --name product-audit
python scripts/neon_genie.py do recipe --name zero-option
python scripts/neon_genie.py do recipe --name zero-option-executable
python scripts/neon_genie.py do recipe --name fragmentation
```

Request envelope: `templates/request.yaml`.
