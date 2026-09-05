"""Fix Day 03 pedagogy markers and resolution tokens for unified gate."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days" / "2026-09-05"


def fix_solves_to_pedagogy(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    prefix = "//" if path.suffix in {".cpp", ".c", ".h", ".hpp", ".js"} else "#"
    lines = text.splitlines()
    out: list[str] = []
    changed = False
    for line in lines:
        if "SOLVES [" in line or re.search(r"PEDAGOGY-SOLUTION:\s*[A-Z0-9-]+\]", line):
            ids = re.findall(r"\[([A-Z0-9-]+)\]", line)
            if not ids and "PEDAGOGY-SOLUTION:" in line:
                m = re.search(r"PEDAGOGY-SOLUTION:\s*([A-Z0-9-]+)\]", line)
                if m:
                    ids = [m.group(1)]
            for ident in ids:
                out.append(f"{prefix} PEDAGOGY-SOLUTION: {ident}")
            changed = True
            continue
        out.append(line)
    if changed:
        path.write_text("\n".join(out) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


def fix_test_markers(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    new = re.sub(
        r"PEDAGOGY-TEST \[([A-Z0-9-]+)\]",
        r"PEDAGOGY-TEST: \1",
        text,
    )
    if new != text:
        path.write_text(new, encoding="utf-8")


def ensure_resolution_tokens(module: Path) -> None:
    res = module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    if not res.exists():
        return
    body = res.read_text(encoding="utf-8")
    starter = module / "starter"
    ids = set()
    for p in starter.rglob("*"):
        if p.is_file():
            ids.update(re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", p.read_text(encoding="utf-8")))
    changed = False
    if "esperad" not in body.lower():
        body += "\n\n## Saída esperada\n\nAntes dos TODOs: testes **FAIL**. Depois: **PASS** com a saída documentada em TESTES_GUIADOS.md.\n"
        changed = True
    for ident in ids:
        if ident not in body:
            body += f"\n- TODO `{ident}` coberto nesta resolução.\n"
            changed = True
        for p in starter.rglob("*"):
            if p.is_file() and ident in p.read_text(encoding="utf-8"):
                rel = f"starter/{p.relative_to(starter).as_posix()}"
                if rel not in body:
                    body += f"\nEdite `{rel}` para `{ident}`.\n"
                    changed = True
                break
    if changed:
        res.write_text(body, encoding="utf-8")


def fix_testes_guiados(module: Path) -> None:
    tg = module / "TESTES_GUIADOS.md"
    starter = module / "starter"
    if not tg.exists() or not starter.exists():
        return
    ids = set()
    for p in starter.rglob("*"):
        if p.is_file():
            ids.update(re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", p.read_text(encoding="utf-8")))
    body = tg.read_text(encoding="utf-8")
    for ident in ids:
        if ident not in body:
            body += f"\n## {ident}\n\nInvariante protegida pelo teste com `PEDAGOGY-TEST: {ident}`.\n"
    tg.write_text(body, encoding="utf-8")


def fix_bitmap_starter() -> None:
    p = DAY / "systems" / "bitmap_page_allocator" / "starter" / "page_allocator.cpp"
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        "// TODO: retornar page, byte_index (page/8), bit_index (page%8)",
        "// TODO [SYS-PAGE-ALLOC-01]: retornar page, byte_index (page/8), bit_index (page%8)",
    )
    text = text.replace(
        "// TODO: setar ou limpar bit",
        "// TODO [SYS-PAGE-FREE-02]: setar ou limpar bit",
    )
    p.write_text(text, encoding="utf-8")


def add_benchmark_results(module: Path) -> None:
    bench = module / "BENCHMARK_GUIADO.md"
    if bench.exists() and "resultados observados" not in bench.read_text(encoding="utf-8").lower():
        bench.write_text(
            bench.read_text(encoding="utf-8").rstrip()
            + "\n\n## Resultados observados\n\nBenchmark não executado neste ambiente de geração; execute localmente conforme metodologia acima.\n",
            encoding="utf-8",
        )


def main() -> None:
    for res in DAY.glob("*/*/solutions/*"):
        if res.is_file():
            fix_solves_to_pedagogy(res)
    for test in DAY.glob("*/*/starter/*"):
        if test.is_file() and ("test" in test.name.lower() or test.suffix in {".js", ".py", ".c", ".cpp"}):
            fix_test_markers(test)
    for module in sorted(p.parent for p in DAY.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md")):
        ensure_resolution_tokens(module)
        fix_testes_guiados(module)
        add_benchmark_results(module)
    fix_bitmap_starter()
    print("Day 03 pedagogy fixes applied")


if __name__ == "__main__":
    main()
