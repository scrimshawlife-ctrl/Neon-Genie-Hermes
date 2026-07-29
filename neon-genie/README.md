# Neon Genie Hermes Skill v3.1

A modular, governed skill implementing the complete Neon Genie capability surface.
Self-contained to load — **proactive research by default** using host-available tools (web, academic indexes, docs, registries, etc.). No external knowledge base is required.

## Design principle

Load the smallest sufficient profile set. The core kernel is always active; specialized profiles are selected by the router. **Research runs automatically** when external facts would improve the result.

## Installation

Copy the `neon-genie` directory into the Hermes custom-skills directory.

## Example

```text
/neon-genie audit this project using product_architecture, commercial,
and wayfinder_handoff. Research anything decision-critical via host tools.
Treat operator files as highest-priority sources. Separate OBSERVED,
INFERRED, SPECULATIVE, and NOT_COMPUTABLE. Do not modify the repository.
```

Offline / no live research:

```text
/neon-genie ... research.enabled=false
```
