# Golden Tests

Fixtures: `evals/cases/`. Rubric skeleton: `evals/rubric.md`.

## Invariants

- Same canonical input and profile set produce structurally identical output.
- Missing evidence yields `NOT_COMPUTABLE`.
- High monetization cannot override anti-capture, integration, authority, or evidence failure.
- x402 is rejected when a conventional billing relationship is superior.
- Zero Option never invents unavailable resources.
- Fragmentation profile rejects integration-negative opportunities.
- Product profile detects conflicting loops and orphan features.
- Evidence profile separates personal, corporate, and foundation attribution.
- Memetic strength cannot promote an unproven concept.
- Wayfinder packet cannot modify product intent.
- No packet grants execution authority.

- Proactive research runs by default when host tools can close material gaps.
- Research failure or missing tooling yields `NOT_COMPUTABLE` with attempted query — never fabricated OBSERVED claims.
- `research.enabled=false` / offline mode skips live fetches and relies on operator + workspace sources only.
- Model prior without fetch is at most `SPECULATIVE`.

## Cases

| File | Focus |
|------|--------|
| `evals/cases/zero-option.json` | Empty skills/access → NOT_COMPUTABLE |
| `evals/cases/x402-misfit.json` | Ornamental x402 rejected |
| `evals/cases/wayfinder-change-control.json` | Product intent change control |
| `evals/cases/memetic-cannot-promote.json` | Gate D — memetic cannot raise promotion |
| `evals/cases/offline-no-fabricated-observed.json` | Gate N — offline model prior ≤ SPECULATIVE |
| `evals/cases/buyer-beneficiary-conflation.json` | Gate C — role conflation fails |
| `evals/cases/authority-leakage.json` | Gate E — packets do not grant execution |

Anti-overclaim catalog: `references/anti-overclaim-patterns.md`.
