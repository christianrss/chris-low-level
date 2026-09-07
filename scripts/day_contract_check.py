#!/usr/bin/env python3
"""Validate day-level contract: module count, track coverage, infra sync, learning paths."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
TRACKS_YAML = ROOT / "openspec/specs/day-contract/tracks.yaml"
LEARNING_PATHS = ROOT / "docs/LEARNING_PATHS.md"
MODULE_MAP = ROOT / "scripts/module_project_map.py"
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
CODE_EXT = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js", ".cs", ".rs", ".asm", ".s", ".yar", ".sh"}
MODULE_COUNT_RE = re.compile(r"(\d+)\s*módulos", re.IGNORECASE)
MODULE_COUNT_EN_RE = re.compile(r"(\d+)\s*modules?", re.IGNORECASE)
GENERIC_START_HERE = "Laboratório unificado de low-level"


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def module_rel_paths(day_dir: Path) -> list[str]:
    return [m.relative_to(day_dir).as_posix() for m in find_modules(day_dir)]


def tracks_present(day_dir: Path) -> set[str]:
    return {p.split("/")[0] for p in module_rel_paths(day_dir)}


def parse_module_count_from_text(content: str) -> int | None:
    for pat in (MODULE_COUNT_RE, MODULE_COUNT_EN_RE):
        m = pat.search(content)
        if m:
            return int(m.group(1))
    m2 = re.search(r"Módulos\s*\((\d+)\)", content, re.IGNORECASE)
    if m2:
        return int(m2.group(1))
    return None


def load_tracks_config() -> dict:
    if not TRACKS_YAML.exists():
        return {}
    text = TRACKS_YAML.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text) or {}
    # Minimal parser for tracks.yaml (no PyYAML dependency)
    cfg: dict = {"tiers": {"tier_a": {"min_modules": 13, "days": {}}}}
    tier_a = cfg["tiers"]["tier_a"]
    m_min = re.search(r"min_modules:\s*(\d+)", text)
    if m_min:
        tier_a["min_modules"] = int(m_min.group(1))
    for day_m in re.finditer(
        r'"(\d{4}-\d{2}-\d{2})":\s*\n\s*required_tracks:\s*\n((?:\s*-\s*\w+\s*\n)+)',
        text,
    ):
        day_name = day_m.group(1)
        tracks = re.findall(r"-\s*(\w+)", day_m.group(2))
        tier_a["days"][day_name] = {"required_tracks": tracks}
    return cfg


def load_day_contract(day_dir: Path) -> dict | None:
    path = day_dir / "day.contract.yaml"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    # Minimal: only min_modules and required_tracks lists
    out: dict = {}
    m_min = re.search(r"min_modules:\s*(\d+)", text)
    if m_min:
        out["min_modules"] = int(m_min.group(1))
    tracks = re.findall(r"^\s*-\s*(\w+)\s*$", text, re.MULTILINE)
    if tracks:
        out["required_tracks"] = tracks
    return out or None


def tier_rules_for_day(day_name: str, cfg: dict, day_contract: dict | None) -> dict | None:
    if day_contract:
        return day_contract
    tier_a = (cfg.get("tiers") or {}).get("tier_a") or {}
    days = tier_a.get("days") or {}
    if day_name in days:
        return {
            "tier": "tier_a",
            "min_modules": tier_a.get("min_modules", 13),
            "required_tracks": days[day_name].get("required_tracks", []),
        }
    return None


def collect_starter_todos(day_dir: Path) -> set[str]:
    ids: set[str] = set()
    for module in find_modules(day_dir):
        starter = module / "starter"
        if not starter.exists():
            continue
        for p in starter.rglob("*"):
            if p.is_file() and p.suffix.lower() in CODE_EXT:
                ids.update(TODO_RE.findall(p.read_text(encoding="utf-8")))
    return ids


def collect_todo_map_ids(todo_map: str) -> set[str]:
    bullet = set(re.findall(r"^-\s*`([A-Z0-9-]+)`", todo_map, re.MULTILINE))
    headers = set(re.findall(r"^##\s*`([A-Z0-9-]+)`", todo_map, re.MULTILINE))
    return bullet | headers


def count_todo_map_entries(todo_map: str) -> int:
    return len(collect_todo_map_ids(todo_map))


def check_learning_paths(day_name: str, rel_modules: list[str], errors: list[str]) -> None:
    if not LEARNING_PATHS.exists() or not MODULE_MAP.exists():
        errors.append("missing LEARNING_PATHS.md or module_project_map.py")
        return
    lp = LEARNING_PATHS.read_text(encoding="utf-8")
    mp = MODULE_MAP.read_text(encoding="utf-8")
    for rel in rel_modules:
        key = f"{day_name}/{rel}"
        if key not in lp and key not in mp:
            errors.append(f"{day_name}: module not in LEARNING_PATHS or module_project_map: {key}")


def check_validation_lists_modules(day_dir: Path, rel_modules: list[str], errors: list[str]) -> None:
    val = day_dir / "VALIDATION.md"
    if not val.exists():
        errors.append(f"{day_dir.name}: missing VALIDATION.md")
        return
    text = val.read_text(encoding="utf-8")
    for rel in rel_modules:
        mod_name = rel.split("/")[-1]
        if mod_name not in text and rel not in text:
            errors.append(f"{day_dir.name}: VALIDATION.md does not mention module {rel}")


def check_start_here_curated(day_dir: Path, warnings: list[str]) -> None:
    path = day_dir / "START_HERE.md"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if GENERIC_START_HERE in content and "| Bloco |" not in content:
        warnings.append(
            f"{day_dir.name}: START_HERE looks like generic scaffold "
            "(missing block table); use curated template or --overwrite-docs intentionally"
        )


def check_day(day_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    day_name = day_dir.name
    rel_modules = module_rel_paths(day_dir)
    actual_count = len(rel_modules)

    for name in ("README.md", "START_HERE.md", "ATIVIDADES.md", "TODO_MAP.md", "VALIDATION.md", "MANIFEST.json"):
        if not (day_dir / name).exists():
            errors.append(f"{day_name}: missing {name}")

    readme_path = day_dir / "README.md"
    if readme_path.exists():
        readme_count = parse_module_count_from_text(readme_path.read_text(encoding="utf-8"))
        if readme_count is not None and readme_count != actual_count:
            errors.append(f"{day_name}: README says {readme_count} modules, filesystem has {actual_count}")

    ativ_path = day_dir / "ATIVIDADES.md"
    if ativ_path.exists():
        ativ_count = parse_module_count_from_text(ativ_path.read_text(encoding="utf-8"))
        if ativ_count is not None and ativ_count != actual_count:
            errors.append(f"{day_name}: ATIVIDADES says {ativ_count} modules, filesystem has {actual_count}")

    manifest_path = day_dir / "MANIFEST.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if "modules" in manifest and manifest["modules"] != actual_count:
                errors.append(
                    f"{day_name}: MANIFEST.modules={manifest['modules']} != filesystem {actual_count}"
                )
        except json.JSONDecodeError as e:
            errors.append(f"{day_name}: invalid MANIFEST.json: {e}")

    todo_map_path = day_dir / "TODO_MAP.md"
    if todo_map_path.exists():
        starter_ids = collect_starter_todos(day_dir)
        map_ids = collect_todo_map_ids(todo_map_path.read_text(encoding="utf-8"))
        missing = sorted(starter_ids - map_ids)
        if missing:
            errors.append(
                f"{day_name}: TODO_MAP missing {len(missing)} starter TODO(s): "
                + ", ".join(missing[:8])
                + ("..." if len(missing) > 8 else "")
            )

    rules = tier_rules_for_day(day_name, load_tracks_config(), load_day_contract(day_dir))
    if rules:
        min_mod = rules.get("min_modules", 13)
        if actual_count < min_mod:
            errors.append(f"{day_name}: tier requires >= {min_mod} modules, found {actual_count}")
        required = rules.get("required_tracks") or []
        present = tracks_present(day_dir)
        missing = [t for t in required if t not in present]
        if missing:
            errors.append(f"{day_name}: missing required tracks: {', '.join(missing)}")
        check_learning_paths(day_name, rel_modules, errors)
        check_validation_lists_modules(day_dir, rel_modules, errors)

    check_start_here_curated(day_dir, warnings)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Day contract check (multi-trilha + infra sync)")
    parser.add_argument("--day", required=True, help="Day folder name e.g. 2026-09-07")
    args = parser.parse_args()

    if yaml is None:
        pass  # tracks.yaml parsed via minimal loader

    day_dir = ROOT / "days" / args.day
    if not day_dir.is_dir():
        print(f"Not found: {day_dir}")
        return 1

    errors, warnings = check_day(day_dir)
    for w in warnings:
        print(f"WARN: {w}")

    if errors:
        print("DAY CONTRACT CHECK FAILED")
        for e in errors:
            print(f" - {e}")
        return 1

    print(f"DAY CONTRACT CHECK PASS — {args.day}: {len(module_rel_paths(day_dir))} modules, infra consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
