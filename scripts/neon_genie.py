#!/usr/bin/env python3
"""Unified packaging CLI for Neon Genie (thin operator surface).

Primary form:
  python scripts/neon_genie.py do <intent> [flags]

Intents (packaging only, no product brain):
  check     Validate skill install integrity
  validate  Validate a packet against a schema
  route     Suggest profile set for a request
  receipt   Build a deterministic run-receipt skeleton
  eval      Run golden gate eval fixtures
  recipe    Run a named packaging recipe (e.g. product-audit)

Also:
  python scripts/neon_genie.py help [intent]
  python scripts/neon_genie.py aliases
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PY = sys.executable

INTENTS: dict[str, dict[str, str]] = {
    "check": {
        "script": "validate_hermes_skill.py",
        "description": "Validate skill layout, version consistency, and profiles",
    },
    "validate": {
        "script": "validate_packet.py",
        "description": "Validate packet JSON required fields against a schema",
    },
    "route": {
        "script": "route_profiles.py",
        "description": "Suggest smallest sufficient profile set from text/request",
    },
    "receipt": {
        "script": "build_receipt.py",
        "description": "Build advisory run-receipt skeleton with content hashes",
    },
    "eval": {
        "script": "run_hermes_evals.py",
        "description": "Run golden gate eval fixtures against deterministic rules",
    },
    "recipe": {
        "script": "recipe_run.py",
        "description": "Run packaging recipe (product-audit, zero-option, fragmentation, …)",
    },
    "transcripts": {
        "script": "check_transcripts.py",
        "description": "Validate golden prose transcript structure and rubric markers",
    },
}

ALIASES = {
    "validate-skill": ("check", []),
    "validate-packet": ("validate", []),
    "route-profiles": ("route", []),
    "build-receipt": ("receipt", []),
    "run-evals": ("eval", []),
    "check-transcripts": ("transcripts", []),
    "product-audit": ("recipe", ["--name", "product-audit"]),
    "zero-option": ("recipe", ["--name", "zero-option"]),
    "fragmentation": ("recipe", ["--name", "fragmentation"]),
}


def top_help() -> str:
    lines = [
        "Neon Genie packaging CLI (advisory only)",
        "",
        "Usage:",
        "  python scripts/neon_genie.py do <intent> [flags]",
        "  python scripts/neon_genie.py help [intent]",
        "  python scripts/neon_genie.py aliases",
        "",
        "Intents:",
    ]
    for name, meta in INTENTS.items():
        lines.append(f"  {name:<10} {meta['description']}")
    lines.extend(
        [
            "",
            "Examples:",
            "  python scripts/neon_genie.py do check",
            "  python scripts/neon_genie.py do validate --packet p.json --type opportunity",
            "  python scripts/neon_genie.py do route --request examples/product-audit.brief.yaml",
            "  python scripts/neon_genie.py do receipt --profiles core,zero_option --out out/receipt.json",
            "  python scripts/neon_genie.py do eval",
            "  python scripts/neon_genie.py do recipe --name product-audit",
            "  python scripts/neon_genie.py do recipe --list",
            "  python scripts/neon_genie.py do recipe --name zero-option",
            "  python scripts/neon_genie.py do recipe --name fragmentation",
            "  python scripts/neon_genie.py do transcripts",
            "",
            "This CLI does not invent opportunities, run research, or grant execution authority.",
            "",
        ]
    )
    return "\n".join(lines)


def intent_help(intent: str) -> str:
    if intent not in INTENTS:
        return f"Unknown intent: {intent}\n"
    meta = INTENTS[intent]
    script = SCRIPT_DIR / meta["script"]
    # Delegate --help to the underlying script
    r = subprocess.run([PY, str(script), "--help"], cwd=SKILL_ROOT, capture_output=True, text=True)
    body = r.stdout or r.stderr or ""
    return f"intent: {intent}\n{meta['description']}\nscript: scripts/{meta['script']}\n\n{body}"


def run_script(script_name: str, argv: list[str]) -> int:
    script = SCRIPT_DIR / script_name
    if not script.is_file():
        print(f"FAIL: missing script {script}", file=sys.stderr)
        return 1
    r = subprocess.run([PY, str(script), *argv], cwd=SKILL_ROOT)
    return int(r.returncode)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in {"-h", "--help", "help"} and len(argv) == 1:
        sys.stdout.write(top_help())
        return 0

    if argv[0] == "help":
        if len(argv) < 2:
            sys.stdout.write(top_help())
            return 0
        sys.stdout.write(intent_help(argv[1]))
        return 0

    if argv[0] == "aliases":
        for alias, (intent, _) in sorted(ALIASES.items()):
            print(f"  {alias} → do {intent}")
        return 0

    # Soft legacy alias at top level
    if argv[0] in ALIASES:
        intent, fixed = ALIASES[argv[0]]
        return run_script(INTENTS[intent]["script"], list(fixed) + argv[1:])

    if argv[0] != "do":
        print(f"Unknown command: {argv[0]}", file=sys.stderr)
        print("Use: python scripts/neon_genie.py do <intent> …", file=sys.stderr)
        return 2

    if len(argv) < 2:
        print("usage: neon_genie.py do <intent> [flags]", file=sys.stderr)
        return 2

    intent = argv[1]
    rest = argv[2:]

    if intent in {"-h", "--help"}:
        sys.stdout.write(top_help())
        return 0

    if any(t in {"-h", "--help"} for t in rest) or intent not in INTENTS:
        if intent not in INTENTS:
            print(f"Unknown intent: {intent}", file=sys.stderr)
            print("Known:", ", ".join(INTENTS), file=sys.stderr)
            return 2
        sys.stdout.write(intent_help(intent))
        return 0

    # Strip help-only path already handled; pass flags through
    return run_script(INTENTS[intent]["script"], rest)


if __name__ == "__main__":
    raise SystemExit(main())
