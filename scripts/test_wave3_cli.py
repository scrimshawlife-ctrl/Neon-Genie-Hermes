#!/usr/bin/env python3
"""Lightweight regression tests for Wave 3 packaging CLI (stdlib only)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
CLI = ROOT / "scripts" / "neon_genie.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(CLI), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def main() -> int:
    errors: list[str] = []

    r = run(["do", "check"])
    if r.returncode != 0:
        errors.append(f"do check failed: {r.stderr or r.stdout}")

    r = run(["do", "route", "--text", "zero capital first cash", "--json"])
    if r.returncode != 0:
        errors.append(f"do route failed: {r.stderr}")
    else:
        data = json.loads(r.stdout)
        if "core" not in data.get("selected", []):
            errors.append("route must include core")
        if "zero_option" not in data.get("selected", []):
            errors.append(f"route expected zero_option, got {data.get('selected')}")

    r = run(["do", "route", "--request", "examples/product-audit.brief.yaml", "--json"])
    if r.returncode != 0:
        errors.append(f"do route --request failed: {r.stderr}")
    else:
        data = json.loads(r.stdout)
        for need in ("product_architecture", "commercial", "wayfinder_handoff"):
            if need not in data.get("selected", []):
                errors.append(f"product-audit route missing {need}: {data.get('selected')}")

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "opp.json"
        # Missing required fields → fail
        packet.write_text("{}", encoding="utf-8")
        r = run(["do", "validate", "--packet", str(packet), "--type", "opportunity"])
        if r.returncode == 0:
            errors.append("validate empty opportunity should FAIL")

        full = {
            "blocked_transition": {},
            "outcome_model": {},
            "system_topology": {},
            "opportunity_thesis": {},
            "validation_path": {},
            "scorecard": {},
            "promotion_state": "TESTABLE",
        }
        packet.write_text(json.dumps(full), encoding="utf-8")
        r = run(["do", "validate", "--packet", str(packet), "--type", "opportunity"])
        if r.returncode != 0:
            errors.append(f"validate full opportunity should PASS: {r.stderr}")

        out = Path(tmp) / "receipt.json"
        r = run(
            [
                "do",
                "receipt",
                "--profiles",
                "core,zero_option",
                "--packet",
                str(packet),
                "--out",
                str(out),
            ]
        )
        if r.returncode != 0:
            errors.append(f"receipt failed: {r.stderr}")
        elif not out.is_file():
            errors.append("receipt did not write file")
        else:
            rec = json.loads(out.read_text(encoding="utf-8"))
            for key in (
                "status",
                "profiles_loaded",
                "claims_by_label",
                "not_computable_fields",
                "promotion_state",
                "human_review_required",
            ):
                if key not in rec:
                    errors.append(f"receipt missing {key}")
            if rec.get("grants_execution") is not False:
                errors.append("receipt must set grants_execution false")
            if rec.get("authority") != "advisory_only":
                errors.append("receipt must be advisory_only")

    if errors:
        print("FAIL: Wave 3 CLI tests", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("PASS: Wave 3 CLI tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
