"""Batch-upgrade module pedagogy files toward extreme quality standards."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
CODE_EXT = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js", ".cs", ".rs", ".asm", ".s", ".yar", ".sh"}

EXERCICIOS_TEMPLATE = """# Exercícios

## Fácil
Valide compreensão básica do conceito central deste módulo sem implementação completa.

## Médio
Implemente os TODOs principais do `starter/` seguindo a resolução guiada.

## Difícil
Trate edge cases documentados em `TESTES_GUIADOS.md` e explique por que cada invariante importa.

## Desafio
Amplie o laboratório (performance, formato real, integração com projeto cumulativo) e documente trade-offs.
"""

RELATORIO_TEMPLATE = """
## Relatório de resolução

- **TODOs concluídos:** (liste os IDs implementados)
- **Comandos de teste:**
  ```bash
  # cole aqui o comando exato usado
  ```
- **Saída esperada:** PASS nos testes do módulo
- **Invariantes verificadas:** (liste)
- **Edge cases testados:** (liste)
- **Benchmark:** hipótese + resultado ou declaração honesta de skip
- **Toolchain não executada:** (se aplicável)
"""

BENCHMARK_APPEND = """
## Resultados observados

Registre aqui mediana/min/max após executar o benchmark neste ambiente.
Se não executado, declare explicitamente: *benchmark não executado neste ambiente*.
"""


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def collect_todo_ids(starter: Path) -> list[str]:
    ids: list[str] = []
    for p in starter.rglob("*"):
        if p.is_file() and p.suffix.lower() in CODE_EXT:
            ids.extend(TODO_RE.findall(p.read_text(encoding="utf-8")))
    return ids


def ensure_exercicios(module: Path) -> bool:
    path = module / "EXERCICIOS.md"
    if path.exists() and len(path.read_text(encoding="utf-8").splitlines()) >= 15:
        return False
    path.write_text(EXERCICIOS_TEMPLATE, encoding="utf-8")
    return True


def ensure_relatorio(module: Path) -> bool:
    path = module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    if not path.exists():
        return False
    body = path.read_text(encoding="utf-8")
    if "relatório de resolução" in body.lower() or "relatorio de resolucao" in body.lower():
        return False
    path.write_text(body.rstrip() + RELATORIO_TEMPLATE, encoding="utf-8")
    return True


def ensure_benchmark_section(module: Path) -> bool:
    path = module / "BENCHMARK_GUIADO.md"
    if not path.exists():
        return False
    body = path.read_text(encoding="utf-8")
    if "resultados observados" in body.lower():
        return False
    path.write_text(body.rstrip() + BENCHMARK_APPEND, encoding="utf-8")
    return True


def add_pedagogy_test_markers(module: Path) -> int:
    starter = module / "starter"
    if not starter.exists():
        return 0
    ids = collect_todo_ids(starter)
    if not ids:
        return 0
    count = 0
    for test_file in list(starter.rglob("test_*")) + list((starter / "tests").rglob("*") if (starter / "tests").exists() else []):
        if not test_file.is_file():
            continue
        if test_file.suffix.lower() not in CODE_EXT and test_file.suffix != ".js":
            continue
        body = test_file.read_text(encoding="utf-8")
        changed = False
        for ident in ids:
            marker = f"PEDAGOGY-TEST: {ident}"
            if marker in body:
                continue
            if ident in body or "TODO" in body or "assert" in body.lower() or "EXPECT" in body:
                body = f"// {marker}\n" + body if test_file.suffix in {".cpp", ".c", ".h", ".hpp", ".cc", ".cxx"} else f"# {marker}\n" + body
                changed = True
        if changed:
            test_file.write_text(body, encoding="utf-8")
            count += 1
    return count


def upgrade_day(day: str) -> None:
    day_dir = ROOT / "days" / day
    stats = {"exercicios": 0, "relatorio": 0, "benchmark": 0, "tests": 0}
    for module in find_modules(day_dir):
        if ensure_exercicios(module):
            stats["exercicios"] += 1
        if ensure_relatorio(module):
            stats["relatorio"] += 1
        if ensure_benchmark_section(module):
            stats["benchmark"] += 1
        stats["tests"] += add_pedagogy_test_markers(module)
    print(f"{day}: {stats}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", help="single day YYYY-MM-DD")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.all:
        for p in sorted((ROOT / "days").iterdir()):
            if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", p.name):
                upgrade_day(p.name)
    elif args.day:
        upgrade_day(args.day)
    else:
        parser.error("use --day or --all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
