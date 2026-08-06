#!/usr/bin/env python3
"""Integration tests for privacy packaging surface (stdlib only)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
PY = sys.executable


def test_receipt_includes_privacy_fields() -> None:
    with tempfile.TemporaryDirectory(prefix="ng-priv-rec-") as td:
        out = Path(td) / "receipt.json"
        r = subprocess.run(
            [
                PY,
                str(SCRIPT_DIR / "build_receipt.py"),
                "--profiles",
                "core,product_architecture",
                "--status",
                "PROPOSED",
                "--out",
                str(out),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        rec = json.loads(out.read_text(encoding="utf-8"))
        assert rec["privacy_mode"] == "LOCAL_ONLY"
        assert rec["privacy_contract_version"] == "1.0.0"
        assert rec["telemetry_status"] == "disabled"
        assert rec["external_actions"] == []
        assert rec["research_policy"]["enabled"] is False
        assert rec["research_policy"]["offline"] is True
        assert "privacy" in rec["profiles_loaded"]
        assert "core" in rec["profiles_loaded"]
        print("PASS: receipt privacy fields")


def main() -> int:
    test_receipt_includes_privacy_fields()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
