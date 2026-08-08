#!/usr/bin/env python3
"""Neon Genie packaging wizard — plan resolver + quick onboarding.

Packaging only. Does not invent opportunities or grant execution authority.
Stdlib only.

Usage:
  python scripts/wizard.py --preset product-audit --print-only --json
  python scripts/wizard.py --answers answers.json --run
  python scripts/wizard.py --path quick --auto --out out/neon-genie/wizard-quick
  python scripts/neon_genie.py do wizard --preset doctor --print-only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PY = sys.executable

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

ANSWERS_SCHEMA = "neon-genie-wizard-answers.v1"
PLAN_SCHEMA = "neon-genie-wizard-plan.v1"

PATHS = frozenset({"resolve", "quick"})
INTENTS = frozenset({"doctor", "check", "privacy", "route", "run", "recipe"})

ALLOWED_KEYS = frozenset(
    {
        "schema",
        "path",
        "intent",
        "recipe",
        "recipe_name",
        "brief",
        "text",
        "out",
        "packet",
        "packet_type",
        "validate_packet",
        "json_out",
    }
)

DEFAULT_OUT_RUN = "out/neon-genie/wizard-run"
DEFAULT_OUT_QUICK = "out/neon-genie/wizard-quick"

HERMES_COACH_BASE = [
    "Open Hermes with Neon Genie loaded",
    "OPEN → ALIGN → ASCEND → CLEAR → SEAL",
    "Do not invent buyers, capital, or skills the operator did not declare",
    "Label claims: OBSERVED | INFERRED | SPECULATIVE | NOT_COMPUTABLE",
    "Advisory only — no spend, publish, contact, or repo mutation",
]

SAFETY_NOTES = [
    "advisory_only",
    "packaging only — product judgment remains in Hermes + SKILL.md",
    "no spend / publish / repo mutation",
]

PRESETS: dict[str, dict[str, Any]] = {
    "doctor": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "doctor",
    },
    "check": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "check",
    },
    "privacy": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "privacy",
        "json_out": True,
    },
    "product-audit": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "run",
        "recipe": "product-audit",
        "out": "out/neon-genie/wizard-product-audit",
    },
    "zero-option": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "run",
        "recipe": "zero-option",
        "out": "out/neon-genie/wizard-zero-option",
    },
    "opportunity": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "run",
        "recipe": "opportunity",
        "out": "out/neon-genie/wizard-opportunity",
    },
    "audit": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "run",
        "recipe": "audit",
        "out": "out/neon-genie/wizard-audit",
    },
    "route-sample": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "route",
        "text": "zero capital first cash app idea between jobs",
        "json_out": True,
    },
    "offline-scaffold": {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": "run",
        "recipe": "product-audit",
        "out": "out/neon-genie/wizard-offline",
    },
    "quick": {
        "schema": ANSWERS_SCHEMA,
        "path": "quick",
        "out": DEFAULT_OUT_QUICK,
    },
}


class WizardError(Exception):
    def __init__(self, message: str, missing: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.missing = missing or []


def known_recipes() -> frozenset[str]:
    try:
        from recipe_run import RECIPES  # type: ignore

        return frozenset(RECIPES.keys())
    except Exception:  # noqa: BLE001
        return frozenset(
            {
                "agentic",
                "audit",
                "capital-sprint",
                "commercial",
                "evidence",
                "fragmentation",
                "memetic",
                "opportunity",
                "product-audit",
                "zero-option",
                "zero-option-executable",
            }
        )


def load_answers(path_or_dash: str) -> dict[str, Any]:
    if path_or_dash == "-":
        text = sys.stdin.read()
    else:
        text = Path(path_or_dash).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise WizardError("answers must be a JSON object")
    return data


def merge_preset(preset: str | None, answers: dict[str, Any] | None) -> dict[str, Any]:
    base: dict[str, Any] = {}
    if preset:
        if preset not in PRESETS:
            raise WizardError(
                f"unknown preset: {preset}; known: {', '.join(sorted(PRESETS))}"
            )
        base = dict(PRESETS[preset])
    if answers:
        base.update(answers)
    if "schema" not in base:
        base["schema"] = ANSWERS_SCHEMA
    if "path" not in base:
        base["path"] = "resolve"
    return base


def validate_answers(answers: dict[str, Any]) -> dict[str, Any]:
    unknown = set(answers) - ALLOWED_KEYS
    if unknown:
        raise WizardError(f"unknown keys: {sorted(unknown)}")
    if answers.get("schema") != ANSWERS_SCHEMA:
        raise WizardError(f"schema must be {ANSWERS_SCHEMA}")

    path = answers.get("path") or "resolve"
    if path not in PATHS:
        raise WizardError(f"unknown path: {path}")

    out = dict(answers)
    out["path"] = path
    if "json_out" not in out:
        out["json_out"] = True
    if "validate_packet" not in out:
        out["validate_packet"] = False

    if path == "quick":
        if not out.get("out"):
            out["out"] = DEFAULT_OUT_QUICK
        return out

    intent = out.get("intent")
    if intent not in INTENTS:
        raise WizardError(
            f"intent required for path=resolve; one of {sorted(INTENTS)}",
            missing=["intent"] if not intent else [],
        )

    recipes = known_recipes()
    recipe = out.get("recipe")
    recipe_name = out.get("recipe_name") or recipe

    if intent == "run":
        if not (recipe or out.get("brief") or out.get("text")):
            raise WizardError(
                "intent=run requires recipe, brief, or text",
                missing=["recipe|brief|text"],
            )
        if recipe and recipe not in recipes:
            raise WizardError(
                f"unknown recipe: {recipe}; known: {', '.join(sorted(recipes))}"
            )
        if not out.get("out"):
            out["out"] = DEFAULT_OUT_RUN
    elif intent == "route":
        if not (out.get("text") or out.get("brief")):
            raise WizardError(
                "intent=route requires text or brief",
                missing=["text|brief"],
            )
    elif intent == "recipe":
        name = recipe_name
        if not name:
            raise WizardError(
                "intent=recipe requires recipe_name or recipe",
                missing=["recipe_name"],
            )
        if name not in recipes:
            raise WizardError(
                f"unknown recipe: {name}; known: {', '.join(sorted(recipes))}"
            )
        out["recipe_name"] = name

    return out


def _do_argv(job: str, *flags: str) -> list[str]:
    """Return argv relative to neon_genie job (without 'do')."""
    return [job, *flags]


def resolve_plan(answers: dict[str, Any], *, run: bool = False) -> dict[str, Any]:
    a = validate_answers(answers)
    path = a["path"]

    if path == "quick":
        out = str(a.get("out") or DEFAULT_OUT_QUICK)
        steps = [
            {
                "id": "env_intro",
                "job": None,
                "argv": None,
                "summary": (
                    f"skill_root={SKILL_ROOT}; export HERMES_SKILL_DIR if needed; "
                    "authority=advisory_only"
                ),
            },
            {
                "id": "doctor",
                "job": "doctor",
                "argv": _do_argv("doctor"),
                "summary": "Full install smoke suite",
            },
            {
                "id": "sample_run",
                "job": "run",
                "argv": _do_argv(
                    "run", "--recipe", "product-audit", "--out", out
                ),
                "summary": f"Sample packaging workspace under {out}",
            },
            {
                "id": "handoff",
                "job": None,
                "argv": None,
                "summary": (
                    f"Open {out}/run-envelope.json and HERMES_NEXT.md; "
                    "resume product judgment in Hermes chat"
                ),
            },
        ]
        coach = list(HERMES_COACH_BASE) + [
            f"After quick path: open {out}/run-envelope.json",
            "Hermes may set research.enabled=false for offline-only work",
        ]
        return {
            "schema": PLAN_SCHEMA,
            "path": "quick",
            "intent": None,
            "job": "sequence",
            "argv": None,
            "steps": steps,
            "rationale": "Week-one onboarding: smoke + sample product-audit package",
            "safety_notes": SAFETY_NOTES + ["writes only under --out when executed"],
            "hermes_coach": coach,
            "authority": "advisory_only",
            "will_run": bool(run),
        }

    intent = a["intent"]
    json_out = bool(a.get("json_out", True))
    argv: list[str]
    rationale: str
    job = intent

    if intent == "doctor":
        argv = _do_argv("doctor")
        rationale = "Install smoke suite"
    elif intent == "check":
        argv = _do_argv("check")
        rationale = "Skill integrity check"
    elif intent == "privacy":
        argv = _do_argv("privacy", "--json") if json_out else _do_argv("privacy")
        rationale = "Resolved repository privacy boundary"
    elif intent == "route":
        parts = ["route"]
        if a.get("brief"):
            parts.extend(["--request", str(a["brief"])])
        if a.get("text"):
            parts.extend(["--text", str(a["text"])])
        if json_out:
            parts.append("--json")
        argv = parts
        rationale = "Suggest profiles from text/brief (packaging router only)"
    elif intent == "recipe":
        name = a.get("recipe_name") or a.get("recipe")
        parts = ["recipe", "--name", str(name)]
        if a.get("out"):
            parts.extend(["--out", str(a["out"])])
        argv = parts
        rationale = f"Named example recipe: {name}"
    elif intent == "run":
        parts = ["run"]
        if a.get("recipe"):
            parts.extend(["--recipe", str(a["recipe"])])
        if a.get("brief"):
            parts.extend(["--brief", str(a["brief"])])
        if a.get("text"):
            parts.extend(["--text", str(a["text"])])
        if a.get("out"):
            parts.extend(["--out", str(a["out"])])
        if a.get("packet"):
            parts.extend(["--packet", str(a["packet"])])
        if a.get("packet_type"):
            parts.extend(["--type", str(a["packet_type"])])
        if a.get("validate_packet"):
            parts.append("--validate")
        argv = parts
        bits = []
        if a.get("recipe"):
            bits.append(f"recipe={a['recipe']}")
        if a.get("brief"):
            bits.append(f"brief={a['brief']}")
        if a.get("text"):
            bits.append("text")
        rationale = "Operator packaging run: " + (", ".join(bits) or "run")
    else:
        raise WizardError(f"unhandled intent: {intent}")

    coach = list(HERMES_COACH_BASE)
    if intent == "run" and a.get("out"):
        coach.append(f"After packaging run: open {a['out']}/run-envelope.json")
    if a.get("recipe") == "product-audit" and "offline" in str(a.get("out") or ""):
        coach.append(
            "Offline coach: tell Hermes research.enabled=false / offline: true in chat"
        )

    return {
        "schema": PLAN_SCHEMA,
        "path": "resolve",
        "intent": intent,
        "job": job,
        "argv": argv,
        "steps": None,
        "rationale": rationale,
        "safety_notes": list(SAFETY_NOTES),
        "hermes_coach": coach,
        "authority": "advisory_only",
        "will_run": bool(run),
    }


def format_plan_json(plan: dict[str, Any]) -> str:
    return json.dumps(plan, indent=2, sort_keys=False) + "\n"


def format_plan_human(
    plan: dict[str, Any],
    skill_root_hint: str = "scripts/neon_genie.py",
) -> str:
    lines = [
        f"Neon Genie wizard plan — path={plan.get('path')} job={plan.get('job')}",
        f"authority: {plan.get('authority', 'advisory_only')}",
        f"rationale: {plan.get('rationale', '')}",
        "",
    ]
    if plan.get("path") == "quick" and plan.get("steps"):
        lines.append("steps:")
        for step in plan["steps"]:
            sid = step.get("id")
            if step.get("argv"):
                cmd = " ".join(step["argv"])
                lines.append(f"  - {sid}: python {skill_root_hint} do {cmd}")
            else:
                lines.append(f"  - {sid}: {step.get('summary', '')}")
    elif plan.get("argv"):
        cmd = " ".join(plan["argv"])
        lines.append(f"command: python {skill_root_hint} do {cmd}")
    lines.append("")
    lines.append("safety:")
    for n in plan.get("safety_notes") or []:
        lines.append(f"  - {n}")
    lines.append("")
    lines.append("hermes_coach:")
    for c in plan.get("hermes_coach") or []:
        lines.append(f"  - {c}")
    if plan.get("will_run"):
        lines.append("")
        lines.append("mode: RUN (will execute packaging jobs)")
    else:
        lines.append("")
        lines.append("mode: PRINT-ONLY (pass --run to execute)")
    return "\n".join(lines) + "\n"


Runner = Callable[[list[str]], int]


def default_runner(job_argv: list[str]) -> int:
    """Run a job argv like ['run', '--recipe', 'product-audit', ...] via neon_genie."""
    cli = SCRIPT_DIR / "neon_genie.py"
    full = [PY, str(cli), "do", *job_argv]
    r = subprocess.run(full, cwd=SKILL_ROOT)
    return int(r.returncode)


def execute_plan(plan: dict[str, Any], *, runner: Runner | None = None) -> int:
    run = runner or default_runner
    if plan.get("path") == "quick":
        code = 0
        for step in plan.get("steps") or []:
            argv = step.get("argv")
            if not argv:
                print(f"==> {step.get('id')}: {step.get('summary', '')}")
                continue
            print(f"==> {step.get('id')}: do {' '.join(argv)}")
            rc = run(list(argv))
            if rc != 0:
                print(
                    f"FAIL: wizard step {step.get('id')} exit {rc}",
                    file=sys.stderr,
                )
                return rc
            print(f"OK: {step.get('id')}")
        print("PASS: wizard quick path")
        return code

    argv = plan.get("argv")
    if not argv:
        print("FAIL: plan has no argv", file=sys.stderr)
        return 1
    print(f"==> do {' '.join(argv)}")
    rc = run(list(argv))
    if rc != 0:
        print(f"FAIL: wizard run exit {rc}", file=sys.stderr)
        return rc
    print("PASS: wizard resolve path")
    return 0


def interactive_collect() -> dict[str, Any]:
    print("Neon Genie packaging wizard (advisory only)")
    print("Paths: 1=resolve (default)  2=quick onboarding")
    path_choice = input("Path [1]: ").strip() or "1"
    if path_choice in {"2", "quick"}:
        out = input(f"Out dir [{DEFAULT_OUT_QUICK}]: ").strip() or DEFAULT_OUT_QUICK
        return {
            "schema": ANSWERS_SCHEMA,
            "path": "quick",
            "out": out,
        }

    intents = sorted(INTENTS)
    print("Intents:", ", ".join(intents))
    intent = input("Intent [run]: ").strip() or "run"
    answers: dict[str, Any] = {
        "schema": ANSWERS_SCHEMA,
        "path": "resolve",
        "intent": intent,
        "json_out": True,
    }
    if intent == "run":
        recipes = ", ".join(sorted(known_recipes()))
        print(f"Recipes: {recipes}")
        recipe = input("Recipe [product-audit]: ").strip() or "product-audit"
        answers["recipe"] = recipe
        answers["out"] = (
            input(f"Out [{DEFAULT_OUT_RUN}]: ").strip() or DEFAULT_OUT_RUN
        )
    elif intent == "route":
        text = input("Text to route: ").strip()
        if not text:
            raise WizardError("text required for route", missing=["text"])
        answers["text"] = text
    elif intent == "recipe":
        name = input("Recipe name [product-audit]: ").strip() or "product-audit"
        answers["recipe_name"] = name
        out = input("Out (optional): ").strip()
        if out:
            answers["out"] = out
    return answers


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Neon Genie packaging wizard — resolve plan or quick onboarding "
            "(advisory only; packaging only)"
        )
    )
    p.add_argument(
        "--path",
        choices=sorted(PATHS),
        default=None,
        help="resolve (default) or quick onboarding",
    )
    p.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default=None,
        help="Seed answers from a named preset",
    )
    p.add_argument(
        "--answers",
        default=None,
        help="JSON answers file path, or - for stdin",
    )
    p.add_argument(
        "--print-only",
        action="store_true",
        help="Print plan only (default on resolve path)",
    )
    p.add_argument(
        "--run",
        action="store_true",
        help="Execute packaging jobs from the plan",
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit plan as neon-genie-wizard-plan.v1 JSON",
    )
    p.add_argument(
        "--auto",
        action="store_true",
        help="Non-interactive quick path defaults (implies run unless --print-only)",
    )
    p.add_argument(
        "--out",
        default=None,
        help="Output directory override (run / quick)",
    )
    p.add_argument(
        "--intent",
        choices=sorted(INTENTS),
        default=None,
        help="Shortcut: set resolve intent without full answers file",
    )
    p.add_argument(
        "--recipe",
        default=None,
        help="Shortcut: recipe name for intent=run or recipe",
    )
    p.add_argument(
        "--text",
        default=None,
        help="Shortcut: free text for route/run",
    )
    p.add_argument(
        "--brief",
        default=None,
        help="Shortcut: brief YAML path for route/run",
    )
    return p


def _answers_from_cli(args: argparse.Namespace) -> dict[str, Any]:
    file_answers: dict[str, Any] | None = None
    if args.answers:
        file_answers = load_answers(args.answers)

    merged = merge_preset(args.preset, file_answers)

    if args.path:
        merged["path"] = args.path
    if args.intent:
        merged["intent"] = args.intent
        merged.setdefault("path", "resolve")
    if args.recipe:
        if merged.get("intent") == "recipe":
            merged["recipe_name"] = args.recipe
        else:
            merged["recipe"] = args.recipe
            merged.setdefault("intent", "run")
            merged.setdefault("path", "resolve")
    if args.text:
        merged["text"] = args.text
        merged.setdefault("intent", "route")
        merged.setdefault("path", "resolve")
    if args.brief:
        merged["brief"] = args.brief
        merged.setdefault("intent", "run")
        merged.setdefault("path", "resolve")
    if args.out:
        merged["out"] = args.out

    if args.auto:
        merged.setdefault("path", "quick")
        if merged.get("path") == "quick" and not merged.get("out"):
            merged["out"] = DEFAULT_OUT_QUICK

    return merged


def _decide_run(args: argparse.Namespace, path: str) -> bool:
    if args.print_only and args.run:
        raise WizardError("pass only one of --print-only or --run")
    if args.print_only:
        return False
    if args.run:
        return True
    if path == "quick":
        if args.auto:
            return True
        if sys.stdin.isatty() and sys.stdout.isatty():
            return True
        raise WizardError(
            "quick path on non-TTY requires --auto, --run, or --print-only"
        )
    # resolve default print-only
    return False


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        has_input = bool(
            args.answers
            or args.preset
            or args.intent
            or args.recipe
            or args.text
            or args.brief
            or args.auto
            or args.path
        )
        if not has_input:
            if not (sys.stdin.isatty() and sys.stdout.isatty()):
                raise WizardError(
                    "non-TTY requires --answers, --preset, --path quick --auto, "
                    "or other flags"
                )
            answers = interactive_collect()
        else:
            answers = _answers_from_cli(args)

        answers = validate_answers(answers)
        will_run = _decide_run(args, answers["path"])
        plan = resolve_plan(answers, run=will_run)

        if args.as_json:
            sys.stdout.write(format_plan_json(plan))
        else:
            sys.stdout.write(format_plan_human(plan))

        if will_run:
            return execute_plan(plan)
        return 0
    except WizardError as exc:
        print(f"FAIL: wizard: {exc.message}", file=sys.stderr)
        if exc.missing:
            print(f"  missing: {', '.join(exc.missing)}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL: wizard: invalid JSON: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nFAIL: wizard: interrupted", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
