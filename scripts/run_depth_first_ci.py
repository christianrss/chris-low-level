#!/usr/bin/env python3
"""Discover and validate every published depth-first day."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from depth_manifest import load_yaml

ROOT = Path(__file__).resolve().parents[1]


def depth_days() -> list[str]:
    days: list[str] = []
    for contract in sorted((ROOT / "days").glob("*/day.contract.yaml")):
        try:
            data = load_yaml(contract)
        except ValueError as exc:
            raise RuntimeError(str(exc)) from exc
        if data.get("profile") == "depth_first":
            days.append(contract.parent.name)
    return days


def run(args: list[str]) -> int:
    print("+", " ".join(args), flush=True)
    return subprocess.run(args, cwd=ROOT).returncode


def main() -> int:
    commands: list[list[str]] = [
        [sys.executable, "-m", "unittest", "tests.test_depth_first_contracts", "-v"],
        [sys.executable, "scripts/cycle_contract_check.py", "--all"],
    ]
    for day in depth_days():
        commands.extend(
            [
                [sys.executable, "scripts/day_contract_check.py", "--day", day],
                [sys.executable, "scripts/pedagogy_check_unified.py", "--day", day],
                [
                    sys.executable,
                    "scripts/run_day_tests.py",
                    "--day",
                    day,
                    "--mode",
                    "starter",
                    "--expect-fail",
                ],
                [
                    sys.executable,
                    "scripts/run_day_tests.py",
                    "--day",
                    day,
                    "--mode",
                    "solutions",
                ],
                [
                    sys.executable,
                    "scripts/run_depth_mutants.py",
                    "--day",
                    day,
                ],
            ]
        )

    failed = [command for command in commands if run(command) != 0]
    if failed:
        print(f"DEPTH-FIRST CI FAILED — {len(failed)} command(s)")
        return 1
    print(f"DEPTH-FIRST CI PASS — {len(depth_days())} published day(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
