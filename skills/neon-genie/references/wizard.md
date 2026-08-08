# Neon Genie packaging wizard (Hermes)

Load this reference while **guiding** packaging (not during product judgment).

## Prefer the wizard when

- Operator is new or asks “wizard / guide me / walk me through”
- Unsure which packaging job (`doctor`, `route`, `run`, `recipe`) to run
- First install: “is this skill healthy?”

## Do not use the wizard for

- OPEN → ALIGN → ASCEND → CLEAR → SEAL product judgment (that stays in chat + SKILL.md)
- Inventing opportunities, buyers, capital, or skills
- Learning ledger promotion (`do learn` is separate and PROPOSED-only)

## Agent protocol (Desktop-safe)

Interactive stdin is unreliable on Hermes tool paths. Prefer:

1. Ask missing fields in chat (one at a time if multi-turn).
2. Write answers JSON (`schema: neon-genie-wizard-answers.v1`).
3. Plan only:

```bash
python scripts/neon_genie.py do wizard --answers answers.json --print-only --json
```

4. After operator confirms, execute:

```bash
python scripts/neon_genie.py do wizard --answers answers.json --run
```

### New install / smoke

```bash
python scripts/neon_genie.py do wizard --path quick --auto
# alias:
python scripts/neon_genie.py wizard-quick
```

## Paths

| Path | Default | Purpose |
|------|---------|---------|
| `resolve` | print-only | One packaging job plan from intent/preset |
| `quick` | run when `--auto` or TTY | doctor → sample product-audit → handoff coach |

## Resolve intents

`doctor` | `check` | `privacy` | `route` | `run` | `recipe`

### Presets

`doctor`, `check`, `privacy`, `product-audit`, `zero-option`, `opportunity`, `audit`, `route-sample`, `offline-scaffold`, `quick`

## Answers shape (strict)

```json
{
  "schema": "neon-genie-wizard-answers.v1",
  "path": "resolve",
  "intent": "run",
  "recipe": "product-audit",
  "out": "out/neon-genie/wizard-product-audit"
}
```

Unknown keys are rejected. Recipe names must exist in the packaging registry.

## After packaging

1. Open `run-envelope.json` and `HERMES_NEXT.md` under `--out`.
2. Resume **product judgment** in Hermes chat (OPEN→SEAL).
3. Never treat the envelope as execution authority.

## Safety

- Authority: `advisory_only`
- Packaging only — no spend, publish, contact, or repo mutation
- No learning-ledger writes from the wizard
