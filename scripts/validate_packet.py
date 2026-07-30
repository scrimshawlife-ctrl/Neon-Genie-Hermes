#!/usr/bin/env python3
"""Validate a JSON packet against a Neon Genie schema (stdlib only).

Usage:
  python scripts/validate_packet.py --packet path.json --type opportunity
  python scripts/validate_packet.py --packet path.json --schema schemas/opportunity-packet.schema.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SCHEMAS = SKILL_ROOT / "schemas"

PACKET_TYPE_TO_SCHEMA = {
    "opportunity": "opportunity-packet.schema.json",
    "product": "product-packet.schema.json",
    "fragmentation": "fragmentation-packet.schema.json",
    "zero_option": "zero-option-packet.schema.json",
    "zero-option": "zero-option-packet.schema.json",
    "agentic": "agentic-service-graph.schema.json",
    "agentic_service": "agentic-service-graph.schema.json",
    "commercial": "commercial-simulation.schema.json",
    "evidence": "evidence-intelligence-packet.schema.json",
    "evidence_intelligence": "evidence-intelligence-packet.schema.json",
    "memetic": "memetic-pressure-packet.schema.json",
    "audit": "audit-delivery-packet.schema.json",
    "audit_delivery": "audit-delivery-packet.schema.json",
    "wayfinder": "wayfinder-execution-packet.schema.json",
    "receipt": "run-receipt.schema.json",
    "run_receipt": "run-receipt.schema.json",
    "envelope": "run-envelope.schema.json",
}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL: cannot read JSON {path}: {exc}") from exc


def validate_required(instance: object, schema: dict) -> list[str]:
    """Minimal JSON Schema subset: type object + required keys present."""
    errors: list[str] = []
    if schema.get("type") == "object":
        if not isinstance(instance, dict):
            return [f"expected object, got {type(instance).__name__}"]
        for key in schema.get("required") or []:
            if key not in instance:
                errors.append(f"missing required property: {key}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Neon Genie packet JSON")
    parser.add_argument("--packet", required=True, type=Path, help="Path to packet JSON")
    parser.add_argument(
        "--type",
        dest="packet_type",
        help=f"Packet type alias: {', '.join(sorted(set(PACKET_TYPE_TO_SCHEMA)))}",
    )
    parser.add_argument("--schema", type=Path, help="Explicit schema path")
    args = parser.parse_args(argv)

    if not args.packet.is_file():
        print(f"FAIL: packet not found: {args.packet}", file=sys.stderr)
        return 1

    if args.schema:
        schema_path = args.schema if args.schema.is_absolute() else SKILL_ROOT / args.schema
    elif args.packet_type:
        key = args.packet_type.strip().lower().replace(" ", "_")
        name = PACKET_TYPE_TO_SCHEMA.get(key)
        if not name:
            print(f"FAIL: unknown packet type: {args.packet_type}", file=sys.stderr)
            print(f"  known: {', '.join(sorted(set(PACKET_TYPE_TO_SCHEMA)))}", file=sys.stderr)
            return 1
        schema_path = SCHEMAS / name
    else:
        print("FAIL: provide --type or --schema", file=sys.stderr)
        return 1

    if not schema_path.is_file():
        print(f"FAIL: schema not found: {schema_path}", file=sys.stderr)
        return 1

    packet = load_json(args.packet)
    schema = load_json(schema_path)
    if not isinstance(schema, dict):
        print("FAIL: schema root must be an object", file=sys.stderr)
        return 1

    errors = validate_required(packet, schema)
    if errors:
        print(f"FAIL: {args.packet} vs {schema_path.name}", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"PASS: packet validates required fields against {schema_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
