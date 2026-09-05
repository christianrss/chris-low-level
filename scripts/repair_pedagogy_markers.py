"""Repair broken PEDAGOGY-SOLUTION markers from bad SOLVES conversion."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days" / "2026-09-05"


def comment_prefix(path: Path) -> str:
    if path.suffix in {".cpp", ".c", ".h", ".hpp", ".js"}:
        return "//"
    return "#"


def repair_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "PEDAGOGY-SOLUTION:" not in text and "SOLVES" not in text:
        return False
    lines = text.splitlines()
    out: list[str] = []
    changed = False
    prefix = comment_prefix(path)
    for line in lines:
        m = re.match(r"^\s*(?://|#)\s*PEDAGOGY-SOLUTION:\s*([A-Z0-9-]+)\](.*)$", line)
        if m:
            ids = [m.group(1)]
            rest = m.group(2)
            for extra in re.findall(r"\[([A-Z0-9-]+)\]", rest):
                ids.append(extra)
            for ident in ids:
                out.append(f"{prefix} PEDAGOGY-SOLUTION: {ident}")
            changed = True
            continue
        if line.startswith("// SOLVES [") or line.startswith("# SOLVES ["):
            ids = re.findall(r"\[([A-Z0-9-]+)\]", line)
            for ident in ids:
                out.append(f"{prefix} PEDAGOGY-SOLUTION: {ident}")
            changed = True
            continue
        out.append(line)
    if changed:
        path.write_text("\n".join(out) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return changed


def main() -> None:
    count = 0
    for p in DAY.rglob("solutions/*"):
        if p.is_file() and repair_file(p):
            print("fixed", p.relative_to(ROOT))
            count += 1
    print(f"repaired {count} files")


if __name__ == "__main__":
    main()
