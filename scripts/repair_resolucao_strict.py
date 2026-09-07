#!/usr/bin/env python3
"""Inject Baseline + placement blocks into RESOLUCAO files for strict pedagogy gate."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(-v\d+)?$")
CODE_EXT = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js", ".cs", ".rs", ".asm", ".s", ".sh"}

PLACEMENT_TEMPLATE = """
### Onde colocar

| | |
|--|--|
| **Arquivo** | `{file}` |
| **Função / âncora** | `{anchor}` — comentário `TODO [{ident}]` |
| **Substituir** | o stub / corpo / case marcado por `TODO [{ident}]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |
"""

DELEGATION_FIXES = [
    (re.compile(r"\bveja\s+solutions\b", re.I), "consulte a RESOLUCAO após tentativa"),
    (re.compile(r"\bcopie\s+solutions\b", re.I), "implemente conforme os passos abaixo"),
    (re.compile(r"\bcompare com solutions\b", re.I), "valide com os testes do starter"),
    (re.compile(r"nota pedag[oó]gica\s+\d+", re.I), ""),
]


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def parse_mapa(res: str) -> dict[str, tuple[str, str]]:
    """Parse TODO ID -> (starter path, function) from mapa table."""
    mapping: dict[str, tuple[str, str]] = {}
    for m in re.finditer(
        r"\|\s*`?([A-Z][A-Z0-9-]+)`?\s*\|\s*`?(starter/[^`|]+)`?\s*\|\s*([^|]+)\|",
        res,
        re.I,
    ):
        ident, path, func = m.group(1), m.group(2).strip(), m.group(3).strip().strip("`")
        if not path.startswith("starter/"):
            path = f"starter/{path}" if "/" in path else f"starter/{path}"
        mapping[ident] = (path, func)
    # alternate: | ID | starter/foo | func |
    for m in re.finditer(
        r"\|\s*`?([A-Z][A-Z0-9-]+)`?\s*\|\s*`?(starter/[^`|]+)`?\s*\|",
        res,
    ):
        ident, path = m.group(1), m.group(2).strip()
        if ident not in mapping:
            mapping[ident] = (path, f"âncora `TODO [{ident}]`")
    return mapping


def scan_starter_todos(starter: Path) -> dict[str, tuple[str, str]]:
    """Find TODO locations in starter code."""
    found: dict[str, tuple[str, str]] = {}
    if not starter.exists():
        return found
    for p in starter.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in CODE_EXT:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = f"starter/{p.relative_to(starter).as_posix()}"
        for ident in TODO_RE.findall(text):
            anchor = f"comentário `TODO [{ident}]` em `{p.name}`"
            # try to find function name above TODO
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if f"TODO [{ident}]" in line:
                    for j in range(i, max(-1, i - 15), -1):
                        fn = re.search(
                            r"(?:def|fn|function|void|int|bool|static|class)\s+(\w+)",
                            lines[j],
                        )
                        if fn:
                            anchor = f"`{fn.group(1)}` — `TODO [{ident}]`"
                            break
                    break
            found[ident] = (rel, anchor)
    return found


def infer_baseline(module: Path) -> str:
    readme = module / "README.md"
    starter = module / "starter"
    lines = [
        "## Baseline",
        "",
        "Antes de editar, confirme que o starter falha por causa dos TODOs (não por ambiente):",
        "",
    ]
    if (starter / "CMakeLists.txt").exists():
        lines += [
            "```powershell",
            f"cmake -S starter -B starter/build",
            f"cmake --build starter/build",
            f"ctest --test-dir starter/build --output-on-failure",
            "```",
            "",
            "**Esperado:** build OK; testes FAIL até completar os TODOs.",
        ]
    elif (starter / "Cargo.toml").exists():
        lines += [
            "```powershell",
            "cd starter",
            "cargo test",
            "```",
            "",
            "**Esperado:** testes FAIL até completar os TODOs.",
        ]
    elif list(starter.glob("*.csproj")) or list(starter.rglob("*.csproj")):
        lines += [
            "```powershell",
            "cd starter",
            "dotnet test",
            "```",
            "",
            "**Esperado:** testes FAIL até completar os TODOs (requer SDK .NET).",
        ]
    elif (starter / "package.json").exists():
        lines += [
            "```powershell",
            "cd starter",
            "npm test",
            "```",
            "",
            "**Esperado:** testes FAIL até completar os TODOs.",
        ]
    elif list(starter.glob("test_*.py")) or list(starter.rglob("tests/*.py")):
        lines += [
            "```powershell",
            "cd starter",
            "python -m pytest tests/ -v",
            "```",
            "",
            "**Esperado:** testes FAIL até completar os TODOs.",
        ]
    else:
        lines += [
            "```powershell",
            "# consulte README.md do módulo para comando de teste",
            "```",
            "",
            "**Esperado:** falha documentada em TESTES_GUIADOS até completar os TODOs.",
        ]
    lines.append("")
    return "\n".join(lines)


def has_baseline(res: str) -> bool:
    return bool(re.search(r"^##\s*baseline\b", res, re.I | re.M))


def has_placement_near(text: str) -> bool:
    low = text.lower()
    if "onde colocar" in low:
        return True
    return (
        ("arquivo" in low or "starter/" in low)
        and ("função" in low or "funcao" in low or "âncora" in low or "ancora" in low)
        and ("substituir" in low or "inserir" in low or "cole " in low)
    )


def section_headings(res: str, ident: str) -> list[int]:
    """Return start indices of ## sections for this TODO id (not table rows)."""
    positions: list[int] = []
    patterns = [
        rf"^##[^\n]*{re.escape(ident)}[^\n]*$",
        rf"^##\s+Exercício[^\n]*{re.escape(ident)}",
    ]
    for pat in patterns:
        for m in re.finditer(pat, res, re.I | re.M):
            if m.start() not in positions:
                positions.append(m.start())
    return sorted(positions)


def inject_placement(res: str, ident: str, file: str, anchor: str) -> str:
    block = PLACEMENT_TEMPLATE.format(ident=ident, file=file, anchor=anchor)
    positions = section_headings(res, ident)
    if not positions:
        return res
    # use first section that lacks placement
    for pos in positions:
        # find end of heading line
        line_end = res.find("\n", pos)
        if line_end == -1:
            line_end = len(res)
        window = res[pos : pos + 1200]
        if has_placement_near(window):
            continue
        insert_at = line_end + 1
        res = res[:insert_at] + block + res[insert_at:]
        return res
    return res


def inject_verifique(res: str, ident: str) -> str:
    """Do not inject generic stubs — modules should have real verification steps."""
    return res


def fix_delegation(text: str) -> str:
    for pat, repl in DELEGATION_FIXES:
        text = pat.sub(repl, text)
    # remove empty lines from removed nota pedagogica
    lines = [ln for ln in text.splitlines() if ln.strip() or True]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def repair_module(module: Path, dry_run: bool = False, baseline_only: bool = False) -> dict[str, int]:
    res_path = module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    if not res_path.exists():
        return {}
    res = res_path.read_text(encoding="utf-8")
    original = res
    stats = {"baseline": 0, "placement": 0, "verifique": 0, "delegation": 0}

    mapa = parse_mapa(res)
    starter_map = scan_starter_todos(module / "starter")
    all_ids = sorted(set(mapa) | set(starter_map))

    if not has_baseline(res):
        baseline = infer_baseline(module)
        # insert after mapa block ends (before next ## heading)
        insert_pos = 0
        mapa_m = re.search(r"##\s*mapa exato", res, re.I)
        if mapa_m:
            rest = res[mapa_m.end() :]
            next_sec = re.search(r"\n## [^#]", rest)
            if next_sec:
                insert_pos = mapa_m.end() + next_sec.start() + 1
        if insert_pos == 0:
            first_h2 = re.search(r"\n## [^#]", res)
            insert_pos = first_h2.start() + 1 if first_h2 else len(res)
        res = res[:insert_pos] + "\n" + baseline + "\n" + res[insert_pos:]
        stats["baseline"] = 1

    for ident in all_ids:
        if baseline_only:
            continue
        file, anchor = mapa.get(ident, starter_map.get(ident, (f"starter/", f"`TODO [{ident}]`")))
        if ident not in mapa and ident in starter_map:
            file, anchor = starter_map[ident]
        elif ident in mapa:
            file, anchor = mapa[ident]
            if anchor and not anchor.startswith("`") and "âncora" not in anchor.lower():
                anchor = f"`{anchor}` — `TODO [{ident}]`"

        before = res
        res = inject_placement(res, ident, file, anchor)
        if res != before:
            stats["placement"] += 1
        before = res
        res = inject_verifique(res, ident)
        if res != before:
            stats["verifique"] += 1

    fixed = fix_delegation(res)
    if fixed != res:
        stats["delegation"] = 1
        res = fixed

    if res != original and not dry_run:
        res_path.write_text(res, encoding="utf-8")

    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", action="append", help="Day folder name(s)")
    parser.add_argument("--all-canonical", action="store_true", help="Days 03-07 without -v2")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--baseline-only",
        action="store_true",
        help="Only insert ## Baseline; skip placement injection",
    )
    args = parser.parse_args()

    day_names: list[str] = []
    if args.all_canonical:
        day_names = [f"2026-09-{d:02d}" for d in range(3, 8)]
    elif args.day:
        day_names = args.day
    else:
        parser.error("provide --day or --all-canonical")

    totals = {"baseline": 0, "placement": 0, "verifique": 0, "delegation": 0, "modules": 0}
    for name in day_names:
        day_dir = ROOT / "days" / name
        if not day_dir.exists():
            print(f"skip missing {name}")
            continue
        for module in find_modules(day_dir):
            stats = repair_module(module, dry_run=args.dry_run, baseline_only=args.baseline_only)
            if any(stats.values()):
                totals["modules"] += 1
                for k in ("baseline", "placement", "verifique", "delegation"):
                    totals[k] += stats.get(k, 0)
                print(f"{module.relative_to(ROOT)}: {stats}")

    print("repair_resolucao_strict totals:", totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
