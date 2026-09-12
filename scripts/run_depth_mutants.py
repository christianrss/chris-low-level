#!/usr/bin/env python3
"""Run project-provided checks that prove critical mutants are rejected."""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from pathlib import Path

from day_contract_check import find_modules, load_day_contract
from depth_manifest import load_yaml

ROOT = Path(__file__).resolve().parents[1]


def run_mutants(day_dir: Path) -> list[str]:
    errors: list[str] = []
    contract = load_day_contract(day_dir)
    if not contract or contract.get("profile") != "depth_first":
        return errors
    modules = find_modules(day_dir)
    if len(modules) != 1:
        return [f"{day_dir.name}: mutant gate requires exactly one project"]
    assessment = load_yaml(day_dir / "ASSESSMENT.yaml")
    for mutant in assessment.get("critical_mutants") or []:
        if not isinstance(mutant, dict):
            errors.append(f"{day_dir.name}: invalid mutant entry")
            continue
        mutant_id = str(mutant.get("id") or "<missing>")
        command = mutant.get("command")
        if not isinstance(command, str) or not command.strip():
            errors.append(f"{day_dir.name}: {mutant_id} missing command")
            continue
        proc = subprocess.run(
            shlex.split(command, posix=os.name != "nt"),
            cwd=modules[0],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            output = ((proc.stdout or "") + (proc.stderr or "")).strip()
            errors.append(
                f"{day_dir.name}: {mutant_id} survived or could not run "
                f"(exit {proc.returncode})\n{output}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Run depth-first critical mutant checks")
    parser.add_argument("--day", required=True)
    args = parser.parse_args()
    day_dir = ROOT / "days" / args.day
    if not day_dir.is_dir():
        print(f"Day not found: {day_dir}")
        return 1
    errors = run_mutants(day_dir)
    if errors:
        print("DEPTH MUTANT CHECK FAILED")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"DEPTH MUTANT CHECK PASS — {args.day}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
