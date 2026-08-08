#!/usr/bin/env python3
"""Tests for Neon Genie packaging wizard (stdlib only)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
PY = sys.executable
CLI = SCRIPT_DIR / "neon_genie.py"
WIZARD = SCRIPT_DIR / "wizard.py"

sys.path.insert(0, str(SCRIPT_DIR))
import wizard as wz  # noqa: E402


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(CLI), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def run_wizard(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(WIZARD), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_preset_product_audit_plan() -> None:
    answers = wz.merge_preset("product-audit", None)
    plan = wz.resolve_plan(answers, run=False)
    assert plan["schema"] == wz.PLAN_SCHEMA
    assert plan["path"] == "resolve"
    assert plan["intent"] == "run"
    assert plan["job"] == "run"
    assert plan["authority"] == "advisory_only"
    assert plan["argv"][0] == "run"
    assert "--recipe" in plan["argv"]
    assert "product-audit" in plan["argv"]
    assert plan["will_run"] is False
    print("PASS: preset product-audit plan")


def test_preset_doctor_plan() -> None:
    answers = wz.merge_preset("doctor", None)
    plan = wz.resolve_plan(answers)
    assert plan["job"] == "doctor"
    assert plan["argv"] == ["doctor"]
    print("PASS: preset doctor plan")


def test_route_missing_text_fails() -> None:
    try:
        wz.validate_answers(
            {
                "schema": wz.ANSWERS_SCHEMA,
                "path": "resolve",
                "intent": "route",
            }
        )
        raise AssertionError("expected WizardError")
    except wz.WizardError as exc:
        assert "text" in exc.message or exc.missing
    print("PASS: route missing text fails")


def test_unknown_key_rejected() -> None:
    try:
        wz.validate_answers(
            {
                "schema": wz.ANSWERS_SCHEMA,
                "path": "resolve",
                "intent": "doctor",
                "bogus": True,
            }
        )
        raise AssertionError("expected WizardError")
    except wz.WizardError as exc:
        assert "unknown keys" in exc.message
    print("PASS: unknown key rejected")


def test_unknown_recipe_rejected() -> None:
    try:
        wz.validate_answers(
            {
                "schema": wz.ANSWERS_SCHEMA,
                "path": "resolve",
                "intent": "run",
                "recipe": "not-a-real-recipe",
            }
        )
        raise AssertionError("expected WizardError")
    except wz.WizardError as exc:
        assert "unknown recipe" in exc.message
    print("PASS: unknown recipe rejected")


def test_quick_print_only_steps() -> None:
    answers = {
        "schema": wz.ANSWERS_SCHEMA,
        "path": "quick",
        "out": "out/neon-genie/wizard-quick-test",
    }
    plan = wz.resolve_plan(answers, run=False)
    assert plan["path"] == "quick"
    assert plan["job"] == "sequence"
    assert plan["argv"] is None
    ids = [s["id"] for s in plan["steps"]]
    assert ids == ["env_intro", "doctor", "sample_run", "handoff"]
    sample = plan["steps"][2]
    assert sample["argv"][0] == "run"
    assert "product-audit" in sample["argv"]
    print("PASS: quick print-only steps")


def test_execute_plan_injectable_runner() -> None:
    calls: list[list[str]] = []

    def fake(argv: list[str]) -> int:
        calls.append(list(argv))
        return 0

    plan = wz.resolve_plan(
        {
            "schema": wz.ANSWERS_SCHEMA,
            "path": "resolve",
            "intent": "doctor",
        },
        run=True,
    )
    rc = wz.execute_plan(plan, runner=fake)
    assert rc == 0
    assert calls == [["doctor"]]
    print("PASS: execute_plan injectable runner")


def test_execute_quick_sequence_runner() -> None:
    calls: list[list[str]] = []

    def fake(argv: list[str]) -> int:
        calls.append(list(argv))
        return 0

    plan = wz.resolve_plan(
        {
            "schema": wz.ANSWERS_SCHEMA,
            "path": "quick",
            "out": "/tmp/ng-wiz-test",
        },
        run=True,
    )
    rc = wz.execute_plan(plan, runner=fake)
    assert rc == 0
    assert len(calls) == 2  # doctor + sample_run
    assert calls[0] == ["doctor"]
    assert calls[1][0] == "run"
    assert "product-audit" in calls[1]
    print("PASS: execute quick sequence runner")


def test_cli_preset_print_json() -> None:
    r = run_cli(
        "do", "wizard", "--preset", "product-audit", "--print-only", "--json"
    )
    assert r.returncode == 0, r.stderr + r.stdout
    plan = json.loads(r.stdout)
    assert plan["schema"] == wz.PLAN_SCHEMA
    assert plan["authority"] == "advisory_only"
    assert plan["intent"] == "run"
    assert "product-audit" in plan["argv"]
    print("PASS: do wizard --preset product-audit --print-only --json")


def test_cli_non_tty_incomplete_exit_2() -> None:
    r = run_wizard()
    # no flags, non-TTY → exit 2
    assert r.returncode == 2, r.stdout + r.stderr
    assert "FAIL: wizard" in r.stderr or "non-TTY" in r.stderr
    print("PASS: non-TTY incomplete exit 2")


def test_cli_quick_print_only() -> None:
    r = run_cli(
        "do",
        "wizard",
        "--path",
        "quick",
        "--print-only",
        "--json",
        "--out",
        "out/neon-genie/wiz-q",
    )
    assert r.returncode == 0, r.stderr + r.stdout
    plan = json.loads(r.stdout)
    assert plan["path"] == "quick"
    assert len(plan["steps"]) == 4
    print("PASS: do wizard --path quick --print-only --json")


def test_cli_run_recipe_via_wizard() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="ng-wiz-run-"))
    out = tmp / "demo"
    try:
        r = run_cli(
            "do",
            "wizard",
            "--preset",
            "zero-option",
            "--run",
            "--out",
            str(out),
        )
        assert r.returncode == 0, r.stderr + r.stdout
        assert (out / "run-envelope.json").is_file(), r.stdout
        env = json.loads((out / "run-envelope.json").read_text(encoding="utf-8"))
        assert env["authority"] == "advisory_only"
        print("PASS: do wizard --preset zero-option --run")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_answers_file() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="ng-wiz-ans-"))
    try:
        ans = {
            "schema": wz.ANSWERS_SCHEMA,
            "path": "resolve",
            "intent": "route",
            "text": "zero capital first cash",
            "json_out": True,
        }
        path = tmp / "answers.json"
        path.write_text(json.dumps(ans), encoding="utf-8")
        r = run_cli(
            "do", "wizard", "--answers", str(path), "--print-only", "--json"
        )
        assert r.returncode == 0, r.stderr + r.stdout
        plan = json.loads(r.stdout)
        assert plan["job"] == "route"
        assert "--text" in plan["argv"]
        print("PASS: answers file route plan")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    failed = 0
    for fn in (
        test_preset_product_audit_plan,
        test_preset_doctor_plan,
        test_route_missing_text_fails,
        test_unknown_key_rejected,
        test_unknown_recipe_rejected,
        test_quick_print_only_steps,
        test_execute_plan_injectable_runner,
        test_execute_quick_sequence_runner,
        test_cli_preset_print_json,
        test_cli_non_tty_incomplete_exit_2,
        test_cli_quick_print_only,
        test_cli_run_recipe_via_wizard,
        test_answers_file,
    ):
        try:
            fn()
        except AssertionError as exc:
            print(f"FAIL: {fn.__name__}: {exc}", file=sys.stderr)
            failed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: {fn.__name__}: {exc}", file=sys.stderr)
            failed += 1
    if failed:
        print(f"FAIL: {failed} wizard test(s)", file=sys.stderr)
        return 1
    print("PASS: wizard tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
