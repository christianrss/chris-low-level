#!/usr/bin/env python3
"""Validate depth-first curriculum coverage across 7-10 day cycles."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from day_contract_check import check_day, load_day_contract, load_tracks_config
from depth_manifest import load_yaml

ROOT = Path(__file__).resolve().parents[1]
CYCLES = ROOT / "openspec" / "specs" / "day-contract" / "cycles"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_STATUS = {"planned", "active", "complete"}


def cycle_path(cycle_id: str) -> Path:
    return CYCLES / f"{cycle_id}.yaml"


def check_cycle(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = load_yaml(path)
    except (OSError, ValueError) as exc:
        return [str(exc)], warnings

    cycle_id = str(data.get("id") or path.stem)
    if path.stem != cycle_id:
        errors.append(f"{cycle_id}: filename must match cycle id")
    status = str(data.get("status") or "")
    if status not in VALID_STATUS:
        errors.append(f"{cycle_id}: status must be planned, active, or complete")

    required = [str(item) for item in data.get("required_lanes") or []]
    known_lanes = set((load_tracks_config().get("curriculum_lanes") or {}).keys())
    unknown_required = sorted(set(required) - known_lanes)
    if unknown_required:
        errors.append(f"{cycle_id}: unknown required lanes: {', '.join(unknown_required)}")

    rows = data.get("days") or []
    if not isinstance(rows, list):
        return [f"{cycle_id}: days must be a list"], warnings
    if not 7 <= len(rows) <= 10:
        errors.append(f"{cycle_id}: cycle must schedule 7-10 days, found {len(rows)}")

    dates: list[str] = []
    lanes: list[str] = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            errors.append(f"{cycle_id}: days[{index}] must be a mapping")
            continue
        day_name = str(row.get("day") or "")
        lane = str(row.get("primary_lane") or "")
        published = row.get("published") is True
        if not DATE_RE.match(day_name):
            errors.append(f"{cycle_id}: invalid day at entry {index}: {day_name!r}")
            continue
        if lane not in known_lanes:
            errors.append(f"{cycle_id}: invalid lane for {day_name}: {lane!r}")
        dates.append(day_name)
        lanes.append(lane)

        day_dir = ROOT / "days" / day_name
        must_exist = status == "complete" or (status == "active" and published)
        if must_exist and not day_dir.is_dir():
            errors.append(f"{cycle_id}: published day missing: {day_name}")
            continue
        if not day_dir.is_dir():
            continue

        contract = load_day_contract(day_dir)
        if not contract:
            errors.append(f"{cycle_id}: {day_name} missing day.contract.yaml")
            continue
        if contract.get("profile") != "depth_first":
            errors.append(f"{cycle_id}: {day_name} must use profile depth_first")
        if contract.get("cycle") != cycle_id:
            errors.append(
                f"{cycle_id}: {day_name} contract references {contract.get('cycle')!r}"
            )
        if contract.get("primary_lane") != lane:
            errors.append(
                f"{cycle_id}: {day_name} lane mismatch "
                f"({contract.get('primary_lane')!r} != {lane!r})"
            )
        day_errors, day_warnings = check_day(day_dir)
        errors.extend(day_errors)
        warnings.extend(day_warnings)

    if len(dates) != len(set(dates)):
        errors.append(f"{cycle_id}: duplicate day dates")
    missing_lanes = sorted(set(required) - set(lanes))
    if missing_lanes:
        errors.append(f"{cycle_id}: missing required lanes: {', '.join(missing_lanes)}")
    if status == "complete" and any(row.get("published") is not True for row in rows if isinstance(row, dict)):
        errors.append(f"{cycle_id}: complete cycle has unpublished entries")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate depth-first curriculum cycles")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--cycle", help="Cycle id, e.g. depth-core-01")
    target.add_argument("--all", action="store_true", help="Validate every cycle manifest")
    args = parser.parse_args()

    paths = sorted(CYCLES.glob("*.yaml")) if args.all else [cycle_path(args.cycle)]
    errors: list[str] = []
    warnings: list[str] = []
    for path in paths:
        if not path.exists():
            errors.append(f"cycle not found: {path}")
            continue
        cycle_errors, cycle_warnings = check_cycle(path)
        errors.extend(cycle_errors)
        warnings.extend(cycle_warnings)

    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        print("CYCLE CONTRACT CHECK FAILED")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"CYCLE CONTRACT CHECK PASS — {len(paths)} cycle(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
