#!/usr/bin/env python3
"""Inspect merge conflict sides for days 08-11 infra files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sides(path: Path) -> None:
    t = path.read_text(encoding="utf-8")
    if "<<<<<<<" not in t:
        print(path, "NO CONFLICT")
        return
    m = re.search(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>>[^\n]*\n?", t, re.S)
    if not m:
        print(path, "parse fail")
        return
    a, b = m.group(1), m.group(2)
    print("===", path.relative_to(ROOT))
    print("HEAD lines", len(a.splitlines()), "| INC lines", len(b.splitlines()))
    print("HEAD first:", (a.splitlines() or [""])[0][:90])
    print("INC first:", (b.splitlines() or [""])[0][:90])
    ha = set(re.findall(r"`([a-z]+/[a-z0-9_]+)`", a))
    hb = set(re.findall(r"`([a-z]+/[a-z0-9_]+)`", b))
    print("only HEAD", sorted(ha - hb))
    print("only INC", sorted(hb - ha))
    print("shared", sorted(ha & hb)[:8], "...")
    print()


def main() -> None:
    for p in [
        "days/2026-09-08/ATIVIDADES.md",
        "days/2026-09-08/TODO_MAP.md",
        "days/2026-09-08/VALIDATION.md",
        "days/2026-09-09/ATIVIDADES.md",
        "days/2026-09-09/README.md",
        "days/2026-09-09/TODO_MAP.md",
        "days/2026-09-09/VALIDATION.md",
        "days/2026-09-10/ATIVIDADES.md",
        "days/2026-09-10/README.md",
        "days/2026-09-10/TODO_MAP.md",
        "days/2026-09-10/VALIDATION.md",
        "days/2026-09-11/ATIVIDADES.md",
        "days/2026-09-11/README.md",
        "days/2026-09-11/TODO_MAP.md",
        "days/2026-09-11/VALIDATION.md",
    ]:
        sides(ROOT / p)


if __name__ == "__main__":
    main()
