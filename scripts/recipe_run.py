#!/usr/bin/env python3
"""Multi-recipe packaging runner for Neon Genie.

Usage:
  python scripts/recipe_run.py --list
  python scripts/recipe_run.py --name product-audit
  python scripts/recipe_run.py --name zero-option --out out/neon-genie/zero-option
  python scripts/recipe_run.py --name fragmentation
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

import recipe_common as rc

SKILL_ROOT = rc.SKILL_ROOT

RecipeFn = Callable[[Path], int]


def recipe_product_audit(out: Path) -> int:
    brief = SKILL_ROOT / "examples" / "product-audit.brief.yaml"
    route = rc.route_request(brief)
    rc.write_json(out / "profile-route.json", route)
    profiles = route.get("selected") or ["core"]

    handoff = {
        "packet": "WayfinderExecutionPacket",
        "status": "PROPOSED",
        "product_intent_changes_require_neon_genie_review": True,
        "profiles_loaded": profiles,
        "objective": "Audit product coherence and produce Wayfinder-ready handoff",
        "non_goals": [
            "Do not rewrite product intent in execution planning",
            "Do not grant execution or spending authority",
        ],
        "authority": "advisory_only",
        "grants_execution": False,
        "brief": rc.rel(brief),
        "note": "Stub handoff from packaging recipe. Full product packet is prose-runtime.",
    }
    handoff_path = out / "wayfinder-handoff.stub.json"
    rc.write_json(handoff_path, handoff)

    product_stub = {
        "target_user": "operator building a governed multi-skill product",
        "job_to_be_done": "clarify product boundary and handoff without inventing feasibility",
        "product_boundary": {
            "in": ["product intent", "scorecard", "wayfinder handoff stub"],
            "out": ["implementation status", "spend", "publish"],
        },
        "system_inventory": ["profiles", "schemas", "packaging CLI"],
        "core_loops": ["OPEN→SEAL advisory loop"],
        "conflict_scan": {"status": "PROPOSED", "conflicts": []},
        "experience_architecture": "operator CLI + Hermes skill prose",
        "validation_path": ["do check", "do eval", "human review"],
        "completion_proof": "Operator accepts product packet + handoff stub in review without intent rewrite",
        "proof_path": [
            "human reviews product-packet.stub.json",
            "confirm open DataRequests listed",
            "optional: satisfy access request then re-score integration",
            "append learning ledger on real outcome",
        ],
        "promotion_state": "SPEC_COMPLETE",
        "authority": "advisory_only",
        "post_seal_checklist": "references/post-seal-verification.md",
    }
    product_path = out / "product-packet.stub.json"
    rc.write_json(product_path, product_stub)
    rc.validate_packet(product_path, "product")

    # Example brief has empty canonical_sources → open private access DataRequest
    data_req = {
        "request_id": "dr-product-access",
        "field": "critical_integration_access",
        "why_decision_critical": (
            "Integration feasibility cannot be OBSERVED without declared access"
        ),
        "sensitivity": "private",
        "suggested_source": "Operator environment credentials or access inventory",
        "blocks_promotion": True,
        "status": "open",
    }
    data_requests = [data_req]
    rc.write_json(out / "data-requests.json", data_requests)

    receipt_path = out / "run-receipt.json"
    rc.build_receipt(
        receipt_path,
        profiles,
        status="PROPOSED",
        promotion_state="SPEC_COMPLETE",
        packets=[product_path, handoff_path],
        data_requests=data_requests,
    )
    return rc.finish(
        recipe="product-audit",
        brief=brief,
        out=out,
        route=route,
        artifacts=[
            out / "profile-route.json",
            product_path,
            handoff_path,
            out / "data-requests.json",
            receipt_path,
            out / "recipe-summary.json",
        ],
    )


def recipe_zero_option(out: Path) -> int:
    brief = SKILL_ROOT / "examples" / "zero-option.brief.yaml"
    route = rc.route_request(brief)
    rc.write_json(out / "profile-route.json", route)
    profiles = route.get("selected") or ["core", "zero_option"]

    # Example brief declares no skills/access → honest NOT_COMPUTABLE packet
    packet = {
        "constraints": ["no capital", "no fictional resources"],
        "capabilities": [],
        "opportunities": [],
        "shadow_flags": ["NON_EXECUTION", "FICTIONAL_RESOURCE_RISK_IF_INVENTED"],
        "system_state": "NOT_COMPUTABLE",
        "status": "NOT_COMPUTABLE",
        "reason": "No executable capabilities or access supplied",
        "completion_proof": "NOT_COMPUTABLE: no skills/access to prove first cash",
        "proof_path": [
            "declare skills and access",
            "re-run zero-option-executable recipe or Hermes zero_option profile",
        ],
        "authority": "advisory_only",
        "grants_execution": False,
    }
    packet_path = out / "zero-option-packet.json"
    rc.write_json(packet_path, packet)
    rc.validate_packet(packet_path, "zero_option")

    receipt_path = out / "run-receipt.json"
    rc.build_receipt(
        receipt_path,
        profiles,
        status="NOT_COMPUTABLE",
        promotion_state="NOT_COMPUTABLE",
        not_computable="capabilities,access,opportunities",
        packets=[packet_path],
    )
    return rc.finish(
        recipe="zero-option",
        brief=brief,
        out=out,
        route=route,
        artifacts=[
            out / "profile-route.json",
            packet_path,
            receipt_path,
            out / "recipe-summary.json",
        ],
        extra={"outcome": "NOT_COMPUTABLE", "gate": "G"},
    )


def recipe_zero_option_executable(out: Path) -> int:
    """Constrained but declared assets → micro-loop stub (still advisory)."""
    brief = SKILL_ROOT / "examples" / "zero-option-with-skills.brief.yaml"
    route = rc.route_request(brief)
    rc.write_json(out / "profile-route.json", route)
    profiles = route.get("selected") or ["core", "zero_option"]

    packet = {
        "constraints": ["no capital", "7 day window"],
        "capabilities": ["writing", "existing audience channel", "public portfolio"],
        "opportunities": [
            {
                "name": "paid micro-audit from existing network",
                "proof": "first paid engagement or honest no",
                "window_days": 7,
            }
        ],
        "shadow_flags": [],
        "system_state": "OPTIONALITY",
        "micro_loop": {
            "narrative": "Use only declared skills/access",
            "action": "Offer one bounded paid diagnostic to known warm contacts",
            "result": "cash or documented refusal",
            "reinforcement": "log outcome; no fictional pipeline",
        },
        "completion_proof": "Paid engagement booked or written refusal within 7 days",
        "proof_path": [
            "list warm contacts from declared access",
            "send one bounded paid diagnostic offer",
            "record cash or refusal",
            "append learning ledger (proof_obtained or proof_failed)",
        ],
        "status": "PROPOSED",
        "authority": "advisory_only",
        "grants_execution": False,
    }
    packet_path = out / "zero-option-packet.json"
    rc.write_json(packet_path, packet)
    rc.validate_packet(packet_path, "zero_option")

    receipt_path = out / "run-receipt.json"
    rc.build_receipt(
        receipt_path,
        profiles,
        status="PROPOSED",
        promotion_state="TESTABLE",
        packets=[packet_path],
    )
    return rc.finish(
        recipe="zero-option-executable",
        brief=brief,
        out=out,
        route=route,
        artifacts=[
            out / "profile-route.json",
            packet_path,
            receipt_path,
            out / "recipe-summary.json",
        ],
        extra={"outcome": "PROPOSED_MICRO_LOOP"},
    )


def recipe_fragmentation(out: Path) -> int:
    brief = SKILL_ROOT / "examples" / "fragmentation.brief.yaml"
    route = rc.route_request(brief)
    rc.write_json(out / "profile-route.json", route)
    profiles = route.get("selected") or ["core", "fragmentation"]

    packet = {
        "target_outcome": "Reduce multi-portal status reconciliation tax",
        "scale": "team-to-org",
        "fragmentation_types": ["workflow", "identity", "payment", "data"],
        "systems_involved": ["portal_a", "portal_b", "spreadsheet_status"],
        "friction_events": [
            {
                "site": "multi-portal status lookup",
                "frequency": "daily",
                "severity": "high",
                "who_pays_tax": "operator / end user",
                "authority_to_fix": "unknown",
            }
        ],
        "coordination_gap": "Systems work alone but force repeated handoffs",
        "proposed_defragmentation_layer": {
            "archetype": "status unifier",
            "integration_burden": "medium",
            "capturable_value": "time saved on status reconciliation",
            "reject_if": "integration burden exceeds capturable value",
        },
        "scorecard": {
            "integration_feasibility": "NOT_COMPUTABLE_without_access"
        },
        "completion_proof": "Measured friction reduction after access inventory OR explicit reject (burden > value)",
        "proof_path": [
            "satisfy access DataRequest",
            "measure handoff time tax",
            "compare integration burden vs capturable value",
            "promote only if net positive",
        ],
        "status": "PROPOSED",
        "promotion_state": "MAPPED",
        "authority": "advisory_only",
        "grants_execution": False,
    }
    packet_path = out / "fragmentation-packet.json"
    rc.write_json(packet_path, packet)
    rc.validate_packet(packet_path, "fragmentation")

    receipt_path = out / "run-receipt.json"
    rc.build_receipt(
        receipt_path,
        profiles,
        status="PROPOSED",
        promotion_state="MAPPED",
        not_computable="critical_integration_access",
        packets=[packet_path],
    )
    return rc.finish(
        recipe="fragmentation",
        brief=brief,
        out=out,
        route=route,
        artifacts=[
            out / "profile-route.json",
            packet_path,
            receipt_path,
            out / "recipe-summary.json",
        ],
    )


RECIPES: dict[str, RecipeFn] = {
    "product-audit": recipe_product_audit,
    "zero-option": recipe_zero_option,
    "zero-option-executable": recipe_zero_option_executable,
    "fragmentation": recipe_fragmentation,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Neon Genie packaging recipes")
    parser.add_argument("--list", action="store_true", help="List recipe names")
    parser.add_argument(
        "--name",
        default="product-audit",
        help=f"Recipe name (default product-audit). Known: {', '.join(RECIPES)}",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default out/neon-genie/<name>)",
    )
    # Accept leftover so `do recipe product-audit` style can be layered later
    args, _unknown = parser.parse_known_args(argv)

    if args.list:
        for name in sorted(RECIPES):
            print(name)
        return 0

    name = args.name
    # Allow first positional-like unknown as name: handled via --name only for clarity
    if name not in RECIPES:
        print(f"FAIL: unknown recipe {name!r}", file=sys.stderr)
        print(f"  known: {', '.join(sorted(RECIPES))}", file=sys.stderr)
        return 1

    out = args.out or (SKILL_ROOT / "out" / "neon-genie" / name)
    out.mkdir(parents=True, exist_ok=True)
    try:
        return RECIPES[name](out)
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
