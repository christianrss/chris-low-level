#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for day in ("2026-09-08", "2026-09-09", "2026-09-10", "2026-09-11"):
    day_dir = ROOT / "days" / day
    ids: list[str] = []
    seen: set[str] = set()
    for p in day_dir.rglob("*"):
        if "starter" not in p.parts or not p.is_file():
            continue
        if any(x in p.parts for x in ("build_ci", "__pycache__", ".git")):
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for tid in re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", t):
            if tid not in seen:
                seen.add(tid)
                ids.append(tid)
    body = "# TODO map — " + day + "\n\n" + "\n".join(f"- `{i}`" for i in ids) + "\n"
    (day_dir / "TODO_MAP.md").write_text(body, encoding="utf-8", newline="\n")
    print(day, len(ids))
