#!/usr/bin/env python3
"""Append a PROPOSED learning-ledger observation (stdlib only).

Never auto-applies to skill corpus or canon.

Usage:
  python scripts/record_learning.py --class proof_failed --summary "No cash in 7 days" \\
    --ledger out/neon-genie/learning-ledger.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

CLASSES = {
    "failed_opportunity",
    "brittle_integration",
    "buyer_failure",
    "distribution_failure",
    "anti_capture_failure",
    "proof_obtained",
    "proof_failed",
    "data_request_satisfied",
    "other",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append learning ledger entry")
    parser.add_argument(
        "--class",
        dest="obs_class",
        required=True,
        choices=sorted(CLASSES),
        help="Observation class",
    )
    parser.add_argument("--summary", required=True, help="What was observed")
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path("out/neon-genie/learning-ledger.jsonl"),
        help="Append-only JSONL path (default out/neon-genie/learning-ledger.jsonl)",
    )
    parser.add_argument("--source-run", default="", help="Receipt or run id/path")
    parser.add_argument(
        "--profiles",
        default="",
        help="Comma-separated related profiles",
    )
    parser.add_argument(
        "--gates",
        default="",
        help="Comma-separated related gate ids",
    )
    args = parser.parse_args(argv)

    entry = {
        "entry_id": f"ll-{uuid.uuid4().hex[:12]}",
        "observed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_run": args.source_run or "unspecified",
        "observation_class": args.obs_class,
        "summary": args.summary,
        "related_profiles": [p.strip() for p in args.profiles.split(",") if p.strip()],
        "related_gates": [g.strip() for g in args.gates.split(",") if g.strip()],
        "evidence_refs": [],
        "canon_status": "PROPOSED",
        "authority": "advisory_only",
        "auto_apply_forbidden": True,
    }

    # Validate required keys against schema contract
    for key in (
        "entry_id",
        "observed_at",
        "source_run",
        "observation_class",
        "summary",
        "canon_status",
        "authority",
    ):
        if not entry.get(key):
            print(f"FAIL: missing {key}", file=sys.stderr)
            return 1

    ledger: Path = args.ledger
    if not ledger.is_absolute():
        ledger = Path.cwd() / ledger
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")

    print("PASS: learning ledger entry appended")
    print(f"  ledger: {ledger}")
    print(f"  entry_id: {entry['entry_id']}")
    print(f"  class: {entry['observation_class']}")
    print("  canon_status: PROPOSED (never auto-applied)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
