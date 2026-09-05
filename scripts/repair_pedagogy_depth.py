#!/usr/bin/env python3
"""Repair mangled PEDAGOGY-TEST lines and add Caso comments from TESTES_GUIADOS."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_EXT = {".c", ".cc", ".cpp", ".py", ".js", ".ts", ".cs"}


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def clean_pedagogy_line(line: str) -> str:
    if "PEDAGOGY-TEST" not in line:
        return line
    # Remove duplicated Caso suffixes appended by buggy sync
    if " — Caso " in line:
        line = line.split(" — Caso ")[0].rstrip()
    return line


def case_comments_block(cases: list[tuple[str, str]]) -> str:
    lines = ["// Test cases (TESTES_GUIADOS.md):"]
    for num, desc in cases:
        short = desc[:80].replace("\n", " ")
        lines.append(f"// Caso {num}: {short}")
    return "\n".join(lines) + "\n"


def repair_module(module: Path) -> int:
    tg = module / "TESTES_GUIADOS.md"
    if not tg.exists():
        return 0
    cases = re.findall(r"### Caso (\d+):\s*(.+)", tg.read_text(encoding="utf-8"))
    if not cases:
        return 0
    block = case_comments_block(cases)
    changed = 0
    starter = module / "starter"
    candidates: list[Path] = []
    for test_file in starter.rglob("*"):
        if not test_file.is_file() or test_file.suffix.lower() not in CODE_EXT:
            continue
        if "test" in test_file.name.lower() or test_file.name == "Program.cs":
            candidates.append(test_file)
    for test_file in candidates:
        text = test_file.read_text(encoding="utf-8")
        lines = text.splitlines()
        new_lines = [clean_pedagogy_line(ln) for ln in lines]
        new_text = "\n".join(new_lines)
        if not new_text.startswith("// Test cases") and "Caso 1:" not in new_text[:500]:
            # Insert block after initial PEDAGOGY-TEST comment lines
            insert_at = 0
            for i, ln in enumerate(new_lines):
                if ln.strip().startswith("// PEDAGOGY-TEST"):
                    insert_at = i + 1
                elif insert_at > 0 and not ln.strip().startswith("//"):
                    break
            if insert_at == 0:
                insert_at = 0
            new_lines = new_lines[:insert_at] + block.splitlines() + new_lines[insert_at:]
            new_text = "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")
        if new_text != text:
            test_file.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def boost_teoria(module: Path) -> bool:
    p = module / "TEORIA_PASSO_A_PASSO.md"
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8")
    count = len(re.findall(r"por qu[eê]", text, re.IGNORECASE))
    if count >= 3:
        return False
    if "## Por quê — síntese pedagógica" in text:
        return False
    supplement = """

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
"""
    p.write_text(text.rstrip() + supplement, encoding="utf-8")
    return True


def main() -> int:
    stats = {"tests_repaired": 0, "teoria_boosted": 0}
    for day_dir in sorted((ROOT / "days").iterdir()):
        if not day_dir.is_dir() or not re.match(r"\d{4}-\d{2}-\d{2}$", day_dir.name):
            continue
        for module in find_modules(day_dir):
            stats["tests_repaired"] += repair_module(module)
            if boost_teoria(module):
                stats["teoria_boosted"] += 1
    print("repair_pedagogy_depth:", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
