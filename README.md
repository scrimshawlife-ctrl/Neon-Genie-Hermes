<div align="center">

# Neon Genie

### Governed Hermes skill for invention, product architecture & opportunity intelligence

[![Version](https://img.shields.io/badge/version-3.1.0-7c3aed?style=for-the-badge)](./neon-genie/manifest.json)
[![Authority](https://img.shields.io/badge/authority-advisory%20only-0ea5e9?style=for-the-badge)](#authority--safety)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge)](./LICENSE)
[![Profiles](https://img.shields.io/badge/profiles-11-ec4899?style=for-the-badge)](#profiles)
[![Hermes](https://img.shields.io/badge/Hermes-skill-f59e0b?style=for-the-badge)](#installation)
[![Status](https://img.shields.io/badge/status-stable-22c55e?style=for-the-badge)](https://github.com/scrimshawlife-ctrl/Neon-Genie-Hermes)

<img src="docs/assets/hero.jpg" alt="Neon Genie — luminous lamp on a dark network grid" width="920" />

**Convert weak signals, blocked transitions, and incomplete products into evidence-bound, externally testable opportunity systems.**

[Installation](#installation) · [Quick start](#quick-start) · [How it works](#how-it-works) · [Profiles](#profiles) · [Outputs](#output-packets) · [Docs](#repository-layout)

</div>

---

## Table of contents

- [Why Neon Genie](#why-neon-genie)
- [Features](#features)
- [Installation](#installation)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [Profiles](#profiles)
- [Claim labels](#claim-labels)
- [Authority & safety](#authority--safety)
- [Output packets](#output-packets)
- [Promotion ladder](#promotion-ladder)
- [Repository layout](#repository-layout)
- [Golden tests](#golden-tests)
- [Wayfinder contract](#wayfinder-contract)
- [Versioning](#versioning)
- [License](#license)
- [Maintainers](#maintainers)

---

## Why Neon Genie

Most “idea → product” agents invent freely and overclaim. Neon Genie is the opposite:

| Principle | Behavior |
|-----------|----------|
| **Evidence-bound** | Every material claim is labeled `OBSERVED`, `INFERRED`, `SPECULATIVE`, or `NOT_COMPUTABLE` |
| **Smallest sufficient profile set** | Router loads only the profiles the request actually needs |
| **Fail closed** | Mandatory gates block promotion when buyer/user, proof, or authority is missing |
| **Advisory only** | Research, model, score, route — never spend, publish, or mutate runtime state without explicit downstream auth |
| **Handoff-ready** | Stable product intent packages for Wayfinder execution — without rewriting intent |
| **Proactive research** | Auto-runs host research when facts would improve the answer; never fabricates |

Built for **Hermes** custom skills by [Applied Alchemy Labs](https://github.com/scrimshawlife-ctrl) / Zero State.

---

## Features

- **Governed invention refinery** — weak signal → blocked transition → testable opportunity
- **Product architecture** — boundary, loops, conflict scan, experience & cost surface
- **Fragmentation mining** — find where systems work but don’t work *together*
- **Zero-Option loops** — zero-capital / constrained first-cash micro-execution design
- **Agentic services & x402** — action decomposition, authority gates, capability-market fit
- **Commercial simulation** — buyer map, pricing, scenarios (unsupported numbers stay labeled)
- **Evidence intelligence** — grants, boards, philanthropy, competitive research
- **Memetic pressure tests** — hooks & names without overriding evidence gates
- **Audit-first delivery** — diagnostic packages + cost of inaction (no fabricated costs)
- **Wayfinder handoff** — execution packets with change control back to Neon Genie

---

## Installation

### Hermes custom skill

```bash
# From this repository root
cp -R neon-genie /path/to/hermes/custom-skills/
```

Or clone only what you need:

```bash
git clone https://github.com/scrimshawlife-ctrl/Neon-Genie-Hermes.git
cd Neon-Genie-Hermes
cp -R neon-genie "$HERMES_SKILLS_DIR/"
```

The skill root is `neon-genie/` (contains `SKILL.md` + `manifest.json`).

> **Requirement:** a Hermes runtime that loads custom skills from a skills directory. Neon Genie is the skill package; Hermes is the host.
>
> **Self-contained to load.** No external knowledge base is required.
>
> **Proactive research by default.** Neon Genie uses host tools (web search, page fetch, academic indexes such as arXiv when available, docs, registries, public filings, etc.) to close decision-critical gaps. Operator-supplied files still take priority. Set `research.enabled=false` for offline runs.

---

## Quick start

Invoke with the smallest profile set that matches the job:

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

**Fragmentation scan**

```text
/neon-genie fragmentation: map authority, payment, and workflow friction
across these systems. Propose a defrag layer only if integration burden
is below capturable value.
```

Request template: [`neon-genie/templates/request.yaml`](./neon-genie/templates/request.yaml)

---

## How it works

### Operating sequence (always)

```text
OPEN → ALIGN → ASCEND → CLEAR → SEAL
```

| Mode | Purpose |
|------|---------|
| **OPEN** | Resolve request, actor, state, evidence, constraints, authority, artifact |
| **ALIGN** | Canonical sources, evidence hierarchy, non-goals, novelty & buildability thresholds |
| **ASCEND** | State-transition, topology, intervention, validation, scoring, routing |
| **CLEAR** | Unsupported claims, authority leakage, duplicates, hidden deps, scope creep |
| **SEAL** | Emit packets + run receipt |

### Core pipeline

```text
SIGNAL
  → BLOCKED TRANSITION
  → OUTCOME MODEL
  → SYSTEM TOPOLOGY
  → OPPORTUNITY THESIS
  → INTERVENTION
  → PRODUCT / SERVICE GRAPH
  → VALIDATION LOOP
  → SCORECARD
  → ROUTING
  → VERIFIED OUTCOME
  → LEARNING MEMORY
```

### Score axes

`evidence density` · `outcome clarity` · `affected-user clarity` · `completion-proof quality` · `integration feasibility` · `reversibility` · `auditability` · `scope boundedness`

A composite score **never** overrides a mandatory gate failure.

---

## Profiles

Core is always loaded. Additional profiles activate only on trigger match.

| Profile | When it loads |
|---------|----------------|
| `core` | Always |
| `product_architecture` | Product/app/game/system design, feature coherence |
| `opportunity_mining` | New venture, unmet need, blocked transition |
| `fragmentation` | Many portals, handoffs, incompatible systems |
| `zero_option` | Zero capital, first cash, constrained launch |
| `agentic_services` | Agent workflows, automation, x402 |
| `commercial` | Pricing, buyer, revenue, business model |
| `evidence_intelligence` | Grants, boards, philanthropy, competitive facts |
| `memetic` | Names, hooks, pitch language |
| `audit_delivery` | Client audit, cost of inaction, offer map |
| `wayfinder_handoff` | Build plan, engineering readiness packet |

Profile contracts live in [`neon-genie/profiles/`](./neon-genie/profiles/).

---

## Claim labels

Every material claim must carry one label:

| Label | Meaning |
|-------|---------|
| `OBSERVED` | Directly supported by cited evidence |
| `INFERRED` | Valid inference from evidence (FORECAST-class) |
| `SPECULATIVE` | Plausible but unproven; not to be treated as fact |
| `NOT_COMPUTABLE` | Missing data — **never fabricate** |

SHADOW detects drift/anomalies only; it does not invent upside.

---

## Authority & safety

Neon Genie **may**: research · infer · generate · compare · score · model · audit · specify · route · draft · recommend.

Neon Genie **may not** (without explicit downstream authorization):

- spend or transfer money
- submit applications or contact targets
- publish content
- modify repositories
- execute irreversible workflows
- promote artifacts to canon
- represent forecasts as facts
- mutate runtime state

`manifest.json` → `"authority": "advisory_only"`

### Mandatory gates (fail closed)

Ambiguous desired state · missing affected user · buyer/beneficiary conflation · undefined completion proof · unknown critical integration access · claims without provenance · actions exceeding authority · ornamental x402 · Zero State harming portability · silent subsystem duplicates · handoff that changes product intent · fabricated missing data.

---

## Output packets

A run emits one or more of:

| Packet | Schema |
|--------|--------|
| `NeonGenieOpportunityPacket` | [`schemas/opportunity-packet.schema.json`](./neon-genie/schemas/opportunity-packet.schema.json) |
| `NeonGenieProductPacket` | [`schemas/product-packet.schema.json`](./neon-genie/schemas/product-packet.schema.json) |
| `FragmentationOpportunityPacket` | [`schemas/fragmentation-packet.schema.json`](./neon-genie/schemas/fragmentation-packet.schema.json) |
| `ZeroOptionPacket` | [`schemas/zero-option-packet.schema.json`](./neon-genie/schemas/zero-option-packet.schema.json) |
| `AgenticServiceGraph` | [`schemas/agentic-service-graph.schema.json`](./neon-genie/schemas/agentic-service-graph.schema.json) |
| `CommercialSimulationPacket` | [`schemas/commercial-simulation.schema.json`](./neon-genie/schemas/commercial-simulation.schema.json) |
| `WayfinderExecutionPacket` | [`schemas/wayfinder-execution-packet.schema.json`](./neon-genie/schemas/wayfinder-execution-packet.schema.json) |
| `NeonGenieRunReceipt` | [`schemas/run-receipt.schema.json`](./neon-genie/schemas/run-receipt.schema.json) |
| Run envelope | [`schemas/run-envelope.schema.json`](./neon-genie/schemas/run-envelope.schema.json) |

Also: `EvidenceIntelligencePacket`, `MemeticPressurePacket`, `AuditDeliveryPacket` (profile-defined).

---

## Promotion ladder

```text
RAW_SIGNAL → MAPPED → CONCEPTUAL → TESTABLE → SERVICE_FIRST
  → SERVICE_PROVEN → SPEC_COMPLETE → WAYFINDER_READY
  → BUILD_READY → CANON_CANDIDATE → ARCHIVED | NOT_COMPUTABLE
```

Memetic strength **cannot** increase promotion readiness when evidence or feasibility gates fail.

---

## Repository layout

```text
Neon-Genie-Hermes/
├── README.md                 # You are here
├── LICENSE                   # Proprietary notice
├── docs/assets/hero.jpg      # Banner art
└── neon-genie/               # ← install this directory
    ├── SKILL.md              # Kernel, router, authority, runes
    ├── manifest.json         # Version, profiles, modes
    ├── README.md             # Package-local install note
    ├── profiles/             # 11 profile contracts
    ├── schemas/              # Packet JSON Schemas
    ├── references/           # Capability map + golden tests
    ├── templates/            # request.yaml envelope
    └── tests/golden/         # Fixture expectations
```

| Path | Purpose |
|------|---------|
| [`neon-genie/SKILL.md`](./neon-genie/SKILL.md) | Full skill specification |
| [`neon-genie/manifest.json`](./neon-genie/manifest.json) | Machine-readable skill metadata |
| [`neon-genie/profiles/`](./neon-genie/profiles/) | Specialized contracts |
| [`neon-genie/schemas/`](./neon-genie/schemas/) | Output validation |
| [`neon-genie/references/CAPABILITY_MAP.md`](./neon-genie/references/CAPABILITY_MAP.md) | Capability surface |
| [`neon-genie/references/GOLDEN_TESTS.md`](./neon-genie/references/GOLDEN_TESTS.md) | Invariants |
| [`neon-genie/tests/golden/`](./neon-genie/tests/golden/) | JSON fixtures |

---

## Golden tests

Key invariants (see [`GOLDEN_TESTS.md`](./neon-genie/references/GOLDEN_TESTS.md)):

- Same canonical input + profile set → structurally identical output
- Missing evidence → `NOT_COMPUTABLE`
- High monetization cannot override anti-capture / integration / authority / evidence failure
- x402 rejected when a conventional billing relationship is superior
- Zero Option never invents unavailable resources
- Wayfinder packet cannot modify product intent
- No packet grants execution authority

---

## Wayfinder contract

| Neon Genie owns | Wayfinder owns |
|-----------------|----------------|
| What should be built & why | Work decomposition |
| Target user & blocked transition | Dependency sequence |
| Product boundary & system behavior | Milestones & eng validation |
| Success criteria & proof requirements | Implementation status |

```yaml
product_intent_changes_require_neon_genie_review: true
```

Any proposed change to product intent returns to Neon Genie as a change request.

---

## Versioning

| Field | Value |
|-------|-------|
| Skill | `neon-genie` |
| Version | **3.1.0** |
| Authority | `advisory_only` |
| Default profiles | `core` |
| Research mode | **proactive** (opt out with `research.enabled=false`) |

Version source of truth: [`neon-genie/manifest.json`](./neon-genie/manifest.json) and frontmatter in [`SKILL.md`](./neon-genie/SKILL.md).

---

## License

**MIT** — Copyright (c) 2026 Applied Alchemy Labs / Zero State.

Free to use, copy, modify, merge, publish, distribute, sublicense, and sell, subject to including the copyright and permission notice. See [`LICENSE`](./LICENSE) for the full text.

---

## Maintainers

**Applied Alchemy Labs** · Zero State  
GitHub: [@scrimshawlife-ctrl](https://github.com/scrimshawlife-ctrl)

---

<div align="center">

<sub>Neon Genie v3.1.0 · OPEN → ALIGN → ASCEND → CLEAR → SEAL · advisory only</sub>

</div>
