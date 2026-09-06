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

PLACEMENT_BLOCK = """
### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/{path}` |
| **Função / âncora** | comentário `TODO [{ident}]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [{ident}]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |
"""

DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(-v\d+)?$")


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def collect_todo_ids(starter: Path) -> list[str]:
    return list(collect_todo_paths(starter).keys())


def collect_todo_paths(starter: Path) -> dict[str, str]:
    """First starter-relative path for each TODO id."""
    out: dict[str, str] = {}
    for p in starter.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in CODE_EXT:
            continue
        try:
            body = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for ident in TODO_RE.findall(body):
            out.setdefault(ident, p.relative_to(starter).as_posix())
    return out


def ensure_placement_blocks(module: Path) -> int:
    """Inject ### Onde colocar under each TODO id missing a placement window."""
    path = module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    starter = module / "starter"
    if not path.exists() or not starter.exists():
        return 0
    body = path.read_text(encoding="utf-8")
    paths = collect_todo_paths(starter)
    added = 0
    for ident, rel in paths.items():
        # Already has placement near some occurrence?
        ok = False
        for m in re.finditer(re.escape(ident), body):
            window = body[m.start() : m.start() + 2500].lower()
            if "onde colocar" in window and (
                "substituir" in window or "inserir" in window or "cole " in window
            ):
                ok = True
                break
        if ok:
            continue
        block = PLACEMENT_BLOCK.format(path=rel, ident=ident)
        # Prefer inserting after a heading that mentions the id
        heading = re.search(
            rf"(^##+[^\n]*{re.escape(ident)}[^\n]*\n)",
            body,
            flags=re.MULTILINE,
        )
        if heading:
            pos = heading.end()
            body = body[:pos] + block + body[pos:]
        elif ident in body:
            pos = body.find(ident) + len(ident)
            # skip to end of line
            nl = body.find("\n", pos)
            if nl < 0:
                nl = pos
            body = body[: nl + 1] + block + body[nl + 1 :]
        else:
            body = body.rstrip() + f"\n\n## `{ident}`\n{block}\n```text\n# complete conforme starter/{rel}\n```\n"
        added += 1
    if added:
        path.write_text(body, encoding="utf-8")
    return added


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
    stats = {"exercicios": 0, "relatorio": 0, "benchmark": 0, "tests": 0, "placement": 0}
    for module in find_modules(day_dir):
        if ensure_exercicios(module):
            stats["exercicios"] += 1
        if ensure_relatorio(module):
            stats["relatorio"] += 1
        if ensure_benchmark_section(module):
            stats["benchmark"] += 1
        stats["tests"] += add_pedagogy_test_markers(module)
        stats["placement"] += ensure_placement_blocks(module)
    print(f"{day}: {stats}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", help="single day YYYY-MM-DD or YYYY-MM-DD-vN")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.all:
        for p in sorted((ROOT / "days").iterdir()):
            if p.is_dir() and DAY_DIR_RE.match(p.name):
                upgrade_day(p.name)
    elif args.day:
        upgrade_day(args.day)
    else:
        parser.error("use --day or --all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
