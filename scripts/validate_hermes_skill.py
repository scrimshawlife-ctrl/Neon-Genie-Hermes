#!/usr/bin/env python3
"""Validate Neon Genie as a portable, self-contained Hermes skill.

Uses only the Python standard library. Run from any working directory:
    python scripts/validate_hermes_skill.py
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILL_FILE = SKILL_ROOT / "SKILL.md"
VERSION_FILE = SKILL_ROOT / "VERSION"
MANIFEST_FILE = SKILL_ROOT / "manifest.json"

REQUIRED_FRONTMATTER = {"name", "description", "version", "author"}
REQUIRED_PATHS = [
    "SKILL.md",
    "QUICKSTART.md",
    "manifest.json",
    "VERSION",
    "references/hermes-runtime-contract.md",
    "references/CAPABILITY_MAP.md",
    "references/GOLDEN_TESTS.md",
    "profiles",
    "schemas",
    "schemas/data-request.schema.json",
    "templates/request.yaml",
    "evals",
    "evals/rubric.md",
    "examples/README.md",
    "scripts/validate_hermes_skill.py",
    "scripts/neon_genie.py",
    "scripts/validate_packet.py",
    "scripts/route_profiles.py",
    "scripts/build_receipt.py",
    "scripts/run_fixture_invariants.py",
    "scripts/audit_release_version.py",
    "scripts/run_hermes_evals.py",
    "scripts/check_transcripts.py",
    "scripts/record_learning.py",
    "references/post-seal-verification.md",
    "schemas/learning-ledger-entry.schema.json",
    "scripts/recipe_run.py",
    "scripts/recipe_common.py",
    "scripts/recipe_product_audit.py",
    "examples/fragmentation.brief.yaml",
    "examples/zero-option-with-skills.brief.yaml",
    "examples/packets/sample-opportunity.packet.json",
    "evals/transcripts/README.md",
    "evals/transcripts/rubric.md",
    "install.sh",
    ".github/workflows/hermes-evals.yml",
]

FORBIDDEN_PATTERNS = [
    re.compile(r"pip install -e"),
    re.compile(r"/Users/"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\"),
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        val = value.strip().strip('"').strip("'")
        if key in fields:
            continue
        fields[key] = val
    return fields


def referenced_relative_paths(text: str) -> set[str]:
    candidates: set[str] = set()
    for match in re.finditer(
        r"`((?:profiles|schemas|references|scripts|evals|templates|examples)/[^`\n]+)`",
        text,
    ):
        value = match.group(1)
        if " " not in value and not value.startswith("/"):
            candidates.add(value.rstrip(".,;:"))
    return candidates


def validate_python(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeError) as exc:
        errors.append(f"Python compile failure: {path.relative_to(SKILL_ROOT)}: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(a in {"-h", "--help"} for a in argv):
        print("Validate Neon Genie as a portable Hermes skill (stdlib only).")
        print("Usage: python scripts/validate_hermes_skill.py")
        print("Exit 0 on PASS; non-zero on FAIL with reasons on stderr.")
        return 0

    errors: list[str] = []

    if not SKILL_FILE.is_file():
        print("FAIL: SKILL.md missing", file=sys.stderr)
        return 1

    skill_text = SKILL_FILE.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(skill_text)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    missing_fields = sorted(REQUIRED_FRONTMATTER - set(frontmatter))
    if missing_fields:
        errors.append(f"Missing frontmatter fields: {', '.join(missing_fields)}")
    if frontmatter.get("name") != "neon-genie":
        errors.append("Frontmatter name must be 'neon-genie'")

    version_fm = frontmatter.get("version", "")
    if not VERSION_FILE.is_file():
        errors.append("VERSION file missing")
        version_file = ""
    else:
        version_file = VERSION_FILE.read_text(encoding="utf-8").strip()

    manifest: dict = {}
    if not MANIFEST_FILE.is_file():
        errors.append("manifest.json missing")
    else:
        try:
            manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"manifest.json invalid JSON: {exc}")

    version_manifest = str(manifest.get("version", ""))
    if version_file and version_fm and version_file != version_fm:
        errors.append(
            f"VERSION ({version_file}) != SKILL frontmatter version ({version_fm})"
        )
    if version_file and version_manifest and version_file != version_manifest:
        errors.append(
            f"VERSION ({version_file}) != manifest.json version ({version_manifest})"
        )
    if version_fm and version_manifest and version_fm != version_manifest:
        errors.append(
            f"SKILL frontmatter version ({version_fm}) != manifest.json version ({version_manifest})"
        )

    for relative in REQUIRED_PATHS:
        path = SKILL_ROOT / relative
        if not path.exists():
            errors.append(f"Missing required path: {relative}")

    profiles = manifest.get("profiles") or []
    if not isinstance(profiles, list) or not profiles:
        errors.append("manifest.json profiles must be a non-empty list")
    else:
        for name in profiles:
            p = SKILL_ROOT / "profiles" / f"{name}.md"
            if not p.is_file():
                errors.append(
                    f"Profile listed in manifest but missing: profiles/{name}.md"
                )

    for rel in sorted(referenced_relative_paths(skill_text)):
        target = SKILL_ROOT / rel
        if not target.exists():
            errors.append(f"SKILL.md references missing path: {rel}")

    scripts_dir = SKILL_ROOT / "scripts"
    if scripts_dir.is_dir():
        for py in sorted(scripts_dir.glob("*.py")):
            errors.extend(validate_python(py))

    for rel in (
        "SKILL.md",
        "QUICKSTART.md",
        "references/hermes-runtime-contract.md",
        "README.md",
    ):
        path = SKILL_ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pat in FORBIDDEN_PATTERNS:
            if pat.search(text):
                errors.append(f"Forbidden pattern {pat.pattern!r} in {rel}")

    if errors:
        print("FAIL: Neon Genie skill validation", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("PASS: Neon Genie skill validation")
    print(f"  root: {SKILL_ROOT}")
    print(f"  version: {version_file or version_fm or version_manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
