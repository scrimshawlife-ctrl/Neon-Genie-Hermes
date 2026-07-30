#!/usr/bin/env python3
"""Build a deterministic NeonGenieRunReceipt skeleton from inputs (stdlib only).

Does not grant authority. Emits PROPOSED packaging metadata + content hashes.

Usage:
  python scripts/build_receipt.py --profiles core,product_architecture --out receipt.json
  python scripts/build_receipt.py --packet path.json --profiles core --status SEALED
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
VERSION_FILE = SKILL_ROOT / "VERSION"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Neon Genie run receipt skeleton")
    parser.add_argument(
        "--profiles",
        default="core",
        help="Comma-separated profiles loaded (default: core)",
    )
    parser.add_argument("--packet", type=Path, action="append", default=[], help="Input packet path (repeatable)")
    parser.add_argument("--input-hash", help="Optional precomputed input hash")
    parser.add_argument(
        "--status",
        default="PROPOSED",
        help="Receipt status (default PROPOSED; never implies execution authority)",
    )
    parser.add_argument(
        "--promotion-state",
        default="RAW_SIGNAL",
        help="Promotion ladder state (default RAW_SIGNAL)",
    )
    parser.add_argument("--out", type=Path, help="Write JSON to path (default stdout)")
    parser.add_argument(
        "--not-computable",
        default="",
        help="Comma-separated NOT_COMPUTABLE field names",
    )
    args = parser.parse_args(argv)

    profiles = [p.strip() for p in args.profiles.split(",") if p.strip()]
    if "core" not in profiles:
        profiles = ["core"] + profiles

    packet_hashes: dict[str, str] = {}
    for path in args.packet:
        if not path.is_file():
            print(f"FAIL: packet not found: {path}", file=sys.stderr)
            return 1
        packet_hashes[str(path)] = sha256_file(path)

    version = VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.is_file() else "unknown"
    material = {
        "skill": "neon-genie",
        "version": version,
        "profiles": profiles,
        "packet_hashes": packet_hashes,
        "status": args.status,
        "promotion_state": args.promotion_state,
    }
    content_hash = sha256_text(json.dumps(material, sort_keys=True, separators=(",", ":")))
    input_hash = args.input_hash or (
        sha256_text(json.dumps(packet_hashes, sort_keys=True)) if packet_hashes else content_hash
    )

    nc = [x.strip() for x in args.not_computable.split(",") if x.strip()]

    receipt = {
        "status": args.status,
        "profiles_loaded": profiles,
        "claims_by_label": {
            "OBSERVED": [],
            "INFERRED": [],
            "SPECULATIVE": [],
            "NOT_COMPUTABLE": nc,
        },
        "not_computable_fields": nc,
        "promotion_state": args.promotion_state,
        "human_review_required": True,
        "authority": "advisory_only",
        "grants_execution": False,
        "skill_version": version,
        "input_hash": input_hash,
        "output_hash": content_hash,
        "packet_hashes": packet_hashes,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "scripts/build_receipt.py",
        "note": "Packaging receipt only. Does not authorize spend, publish, or execution.",
    }

    text = json.dumps(receipt, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"PASS: wrote receipt {args.out}")
        print(f"  output_hash: {content_hash}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
