# Evidence and Stakeholder Intelligence Profile

Proactive research and stakeholder intelligence for grants, boards, philanthropy, competitive landscape, and current external facts.

**Default:** auto-load when external facts would improve the result — not only when the operator names this profile.

## Runes
- `RUNE.NG.RESEARCH.GAP_DETECT`
- `RUNE.NG.RESEARCH.QUERY_PLAN`
- `RUNE.NG.RESEARCH.FETCH`
- `RUNE.NG.RESEARCH.CITE`
- `RUNE.NG.GRANT_DISCOVER`
- `RUNE.NG.GRANT_PROCESS`
- `RUNE.NG.BOARD_RESOLVE`
- `RUNE.NG.PHILANTHROPY_TRACE`
- `RUNE.NG.AFFINITY_MODEL`
- `RUNE.NG.PORTFOLIO_RANK`
- `RUNE.NG.OUTREACH_BUILD`
- `RUNE.NG.COMPETITIVE.SCAN`
- `RUNE.NG.MARKET.FACT_CHECK`

## Source classes (host-dependent)

Use whichever host tools exist; do not hard-require any single provider:

| Class | Examples (illustrative) |
|-------|-------------------------|
| Open web | search, official product/docs pages, news |
| Academic / preprints | arXiv, papers with code, conference sites |
| Standards & regs | RFCs, W3C, gov/regulatory portals |
| Market / company | public sites, filings, pricing pages |
| Grants & funders | foundation sites, grant databases, 990s where public |
| Boards & people | public bios, org pages (no private scraping) |
| Technical | package registries, API docs, GitHub public repos |
| Operator / workspace | files, repos, pasted corpora |

If a class is unavailable on the host, skip it and record `tooling_gap` — never invent results.

## Auto-research protocol

1. List decision-critical questions.
2. Map each to source class + query.
3. Fetch in usefulness order (primary → secondary).
4. Normalize into evidence items with URL/path, title, date, snippet, retrieval time.
5. Label claims; promote only what is supported.
6. Stop when additional fetches would not change the recommendation or scorecard.

## Rules
- Prefer current authoritative primary sources over secondary blogs.
- Preserve role distinctions and attribution boundaries (person / corporate / foundation / model).
- Never fabricate familiarity, referrals, giving motives, private knowledge, or offline-only data.
- Drafting does not authorize sending, applying, or contacting.
- Competitive and market numbers without a cite are `SPECULATIVE` or `NOT_COMPUTABLE`, not `OBSERVED`.
