#!/usr/bin/env python3
"""Sample packaging pass for the product-audit example brief.

Runs: route → receipt → write bundle under out/neon-genie/product-audit/
Does not invent product architecture (prose runtime owns that).

Usage:
  python scripts/recipe_product_audit.py
  python scripts/recipe_product_audit.py --out out/neon-genie/product-audit
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PY = sys.executable
CLI = SCRIPT_DIR / "neon_genie.py"
BRIEF = SKILL_ROOT / "examples" / "product-audit.brief.yaml"


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(CLI), *args],
        cwd=SKILL_ROOT,
        capture_output=True,
        text=True,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Product-audit packaging recipe")
    parser.add_argument(
        "--out",
        type=Path,
        default=SKILL_ROOT / "out" / "neon-genie" / "product-audit",
        help="Output directory",
    )
    args = parser.parse_args(argv)

    if not BRIEF.is_file():
        print(f"FAIL: missing brief {BRIEF}", file=sys.stderr)
        return 1

    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    r = run_cli(["do", "route", "--request", str(BRIEF), "--json"])
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        return r.returncode
    route = json.loads(r.stdout)
    route_path = out / "profile-route.json"
    route_path.write_text(json.dumps(route, indent=2) + "\n", encoding="utf-8")

    profiles = ",".join(route.get("selected") or ["core"])
    receipt_path = out / "run-receipt.json"
    r = run_cli(
        [
            "do",
            "receipt",
            "--profiles",
            profiles,
            "--status",
            "PROPOSED",
            "--promotion-state",
            "SPEC_COMPLETE",
            "--out",
            str(receipt_path),
        ]
    )
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        return r.returncode

    # Minimal handoff stub — intent fields only; Wayfinder owns decomposition.
    handoff = {
        "packet": "WayfinderExecutionPacket",
        "status": "PROPOSED",
        "product_intent_changes_require_neon_genie_review": True,
        "profiles_loaded": route.get("selected"),
        "objective": "Audit product coherence and produce Wayfinder-ready handoff",
        "non_goals": [
            "Do not rewrite product intent in execution planning",
            "Do not grant execution or spending authority",
        ],
        "authority": "advisory_only",
        "grants_execution": False,
        "brief": str(BRIEF.relative_to(SKILL_ROOT)),
        "note": "Stub handoff from packaging recipe. Full product packet is prose-runtime.",
    }
    handoff_path = out / "wayfinder-handoff.stub.json"
    handoff_path.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")

    # Validate handoff stub does not claim execution
    if handoff.get("grants_execution") is not False:
        print("FAIL: handoff must not grant execution", file=sys.stderr)
        return 1
    if handoff.get("product_intent_changes_require_neon_genie_review") is not True:
        print("FAIL: change control missing", file=sys.stderr)
        return 1

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(SKILL_ROOT))
        except ValueError:
            return str(p)

    summary = {
        "recipe": "product-audit",
        "brief": rel(BRIEF),
        "selected_profiles": route.get("selected"),
        "artifacts": [rel(route_path), rel(receipt_path), rel(handoff_path)],
        "status": "PASS",
    }

    (out / "recipe-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    print("PASS: product-audit packaging recipe")
    print(f"  profiles: {', '.join(route.get('selected') or [])}")
    print(f"  out: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
