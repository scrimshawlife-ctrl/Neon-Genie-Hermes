# Neon Genie Quickstart

Governed Hermes skill for opportunity and product intelligence. **Advisory only.**

**Paths:** [How to use (README)](./README.md#how-to-use) · [10-minute demo](./docs/DEMO.md) · [Premiere thesis](./docs/PREMIERE.md)

---

## Install

```bash
git clone https://github.com/scrimshawlife-ctrl/Neon-Genie-Hermes.git
cd Neon-Genie-Hermes
./install.sh
# → ~/.hermes/skills/neon-genie

python scripts/neon_genie.py do check
# or full smoke:
python scripts/neon_genie.py do doctor
```

Reload Hermes after install.

---

## Use in Hermes (humans & chat agents)

1. Load / trigger **neon-genie**.
2. State the job, constraints, and what “done” looks like.
3. Prefer smallest profile set; research is proactive unless you turn it off.
4. Expect labeled claims and fail-closed gaps.

```text
/neon-genie audit this project using product_architecture, commercial,
and wayfinder_handoff. Research public decision-critical facts. Request
private access instead of inventing. Label OBSERVED / INFERRED /
SPECULATIVE / NOT_COMPUTABLE. Do not modify the repository.
```

```text
/neon-genie zero_option: first cash in 7 days from declared skills only.
No fictional resources.
```

```text
/neon-genie research.enabled=false
```

Request shape: [`templates/request.yaml`](./templates/request.yaml).  
Prose goldens: [`evals/transcripts/`](./evals/transcripts/).

---

## Commands (one pattern)

```text
python scripts/neon_genie.py do <job> [options]
```

| Job | When to use |
|-----|-------------|
| `doctor` | Full smoke (install / CI / agents) |
| `check` | Skill integrity only |
| `recipe` | Named example end-to-end (`--list` / `--name`) |
| `route` | Profile suggestion from text or brief |
| `validate` | Packet vs schema |
| `receipt` | Advisory run receipt |
| `eval` | Golden gate tests |
| `transcripts` | Golden prose structure checks |
| `learn` | Append PROPOSED outcome to a local ledger |

```bash
python scripts/neon_genie.py help
python scripts/neon_genie.py do recipe --list
python scripts/neon_genie.py do recipe --name product-audit --out out/neon-genie/run1
python scripts/neon_genie.py do route --text "first cash zero capital" --json
```

---

## Missing data

1. **Find** public facts (host research).  
2. **Request** private facts (`DataRequest`) — do not invent.  
3. Only then **`NOT_COMPUTABLE`**.

---

## Authority

May draft and recommend. May **not** spend, publish, contact, or change repos without separate authorization.

`authority: advisory_only`
