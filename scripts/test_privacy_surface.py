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


def test_validate_rejects_local_only_with_sent_action() -> None:
    with tempfile.TemporaryDirectory(prefix="ng-priv-val-") as td:
        path = Path(td) / "bad-receipt.json"
        # minimal receipt with violation
        bad = {
            "status": "SEALED",
            "profiles_loaded": ["core", "privacy"],
            "claims_by_label": {
                "OBSERVED": [],
                "INFERRED": [],
                "SPECULATIVE": [],
                "NOT_COMPUTABLE": [],
            },
            "not_computable_fields": [],
            "promotion_state": "RAW_SIGNAL",
            "human_review_required": True,
            "privacy_mode": "LOCAL_ONLY",
            "privacy_contract_version": "1.0.0",
            "data_sources_used": ["operator_input"],
            "external_actions": [
                {
                    "action_id": "ea_1",
                    "outcome": "ALLOW",
                    "sent": True,
                    "destination": "example.com",
                    "tool_or_provider": "web_search",
                    "purpose": "test",
                    "data_categories": ["public_web"],
                    "payload_redacted": True,
                }
            ],
            "artifact_paths": [],
            "telemetry_status": "disabled",
            "retention_statement": "x",
            "privacy_warnings": [],
            "deletion_instructions": "x",
            "redaction": {
                "enabled": True,
                "blocked_categories": [],
                "events": [],
            },
            "research_policy": {"enabled": False, "offline": True},
        }
        path.write_text(json.dumps(bad), encoding="utf-8")
        r = subprocess.run(
            [
                PY,
                str(SCRIPT_DIR / "validate_packet.py"),
                "--packet",
                str(path),
                "--type",
                "receipt",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert r.returncode != 0
        assert "NG-PRIV-003" in (r.stderr + r.stdout)
        print("PASS: LOCAL_ONLY + sent rejected")


def test_validate_rejects_telemetry_enabled() -> None:
    with tempfile.TemporaryDirectory(prefix="ng-priv-tel-") as td:
        path = Path(td) / "tel.json"
        rec = {
            "status": "PROPOSED",
            "profiles_loaded": ["core", "privacy"],
            "claims_by_label": {
                "OBSERVED": [],
                "INFERRED": [],
                "SPECULATIVE": [],
                "NOT_COMPUTABLE": [],
            },
            "not_computable_fields": [],
            "promotion_state": "RAW_SIGNAL",
            "human_review_required": True,
            "telemetry_status": "enabled",
            "privacy_mode": "LOCAL_ONLY",
            "privacy_contract_version": "1.0.0",
            "data_sources_used": [],
            "external_actions": [],
            "artifact_paths": [],
            "retention_statement": "x",
            "privacy_warnings": [],
            "deletion_instructions": "x",
            "redaction": {},
            "research_policy": {"enabled": False, "offline": True},
        }
        path.write_text(json.dumps(rec), encoding="utf-8")
        r = subprocess.run(
            [
                PY,
                str(SCRIPT_DIR / "validate_packet.py"),
                "--packet",
                str(path),
                "--type",
                "receipt",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert r.returncode != 0
        assert "NG-PRIV-002" in (r.stderr + r.stdout)
        print("PASS: telemetry enabled rejected")


def test_route_includes_privacy() -> None:
    r = subprocess.run(
        [
            PY,
            str(SCRIPT_DIR / "neon_genie.py"),
            "do",
            "route",
            "--text",
            "product audit for missing buyer",
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(r.stdout)
    selected = data.get("selected") or data.get("profiles") or []
    assert "core" in selected
    assert "privacy" in selected
    # privacy must sit immediately after core
    assert selected.index("privacy") == selected.index("core") + 1
    print("PASS: route includes privacy")


def test_do_privacy_json() -> None:
    r = subprocess.run(
        [PY, str(SCRIPT_DIR / "neon_genie.py"), "do", "privacy", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(r.stdout)
    assert data["telemetry_status"] == "disabled"
    assert data["preflight_self_test"] == "pass"
    assert data["wayfinder_required"] is False
    print("PASS: do privacy --json")


def _minimal_receipt_base(**overrides: object) -> dict:
    base: dict = {
        "status": "SEALED",
        "profiles_loaded": ["core", "privacy"],
        "claims_by_label": {
            "OBSERVED": [],
            "INFERRED": [],
            "SPECULATIVE": [],
            "NOT_COMPUTABLE": [],
        },
        "not_computable_fields": [],
        "promotion_state": "RAW_SIGNAL",
        "human_review_required": True,
        "privacy_mode": "LOCAL_ONLY",
        "privacy_contract_version": "1.0.0",
        "data_sources_used": ["operator_input"],
        "external_actions": [],
        "artifact_paths": [],
        "telemetry_status": "disabled",
        "retention_statement": "x",
        "privacy_warnings": [],
        "deletion_instructions": "x",
        "redaction": {
            "enabled": True,
            "blocked_categories": [],
            "events": [],
        },
        "research_policy": {"enabled": False, "offline": True},
    }
    base.update(overrides)
    return base


def test_sealed_missing_privacy_mode_ng_priv_005() -> None:
    """Gate Y: SEALED receipt missing privacy_mode → NG-PRIV-005."""
    with tempfile.TemporaryDirectory(prefix="ng-priv-y-") as td:
        path = Path(td) / "sealed-incomplete.json"
        rec = _minimal_receipt_base()
        del rec["privacy_mode"]
        path.write_text(json.dumps(rec), encoding="utf-8")
        r = subprocess.run(
            [
                PY,
                str(SCRIPT_DIR / "validate_packet.py"),
                "--packet",
                str(path),
                "--type",
                "receipt",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert r.returncode != 0
        assert "NG-PRIV-005" in (r.stderr + r.stdout)
        print("PASS: SEALED missing privacy_mode → NG-PRIV-005")


def test_research_offline_with_sent_ng_priv_003() -> None:
    """Gate T: research offline + sent true → NG-PRIV-003 (even if not LOCAL_ONLY)."""
    with tempfile.TemporaryDirectory(prefix="ng-priv-t-") as td:
        path = Path(td) / "offline-sent.json"
        rec = _minimal_receipt_base(
            status="PROPOSED",
            privacy_mode="EXTERNAL_RESEARCH_ALLOWED",
            research_policy={"enabled": True, "offline": True},
            external_actions=[
                {
                    "action_id": "ea_1",
                    "outcome": "ALLOW",
                    "sent": True,
                    "destination": "example.com",
                    "tool_or_provider": "web_search",
                    "purpose": "test",
                    "data_categories": ["public_web"],
                    "payload_redacted": True,
                }
            ],
        )
        path.write_text(json.dumps(rec), encoding="utf-8")
        r = subprocess.run(
            [
                PY,
                str(SCRIPT_DIR / "validate_packet.py"),
                "--packet",
                str(path),
                "--type",
                "receipt",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert r.returncode != 0
        assert "NG-PRIV-003" in (r.stderr + r.stdout)
        print("PASS: research offline + sent → NG-PRIV-003")


def main() -> int:
    test_receipt_includes_privacy_fields()
    test_validate_rejects_local_only_with_sent_action()
    test_validate_rejects_telemetry_enabled()
    test_route_includes_privacy()
    test_do_privacy_json()
    test_sealed_missing_privacy_mode_ng_priv_005()
    test_research_offline_with_sent_ng_priv_003()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
