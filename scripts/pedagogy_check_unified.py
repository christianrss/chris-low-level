"""Unified pedagogy gate for any day folder under days/YYYY-MM-DD/."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_EXT = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js", ".cs",
    ".rs", ".asm", ".s", ".yar", ".sh", ".glsl", ".hlsl",
}
SKIP_DIR_NAMES = {
    "build",
    "build_ci",
    "build_bench",
    "build-starter",
    "build-solution",
    "build-demo",
    "node_modules",
    "CMakeFiles",
    "bin",
    "obj",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "target",
    "TestResults",
    "BenchmarkDotNet.Artifacts",
    ".vs",
    ".idea",
    ".cache",
    "dist",
    "out",
    "coverage",
    "htmlcov",
    ".local-build",
    ".local-build-bench",
}
SKIP_FILE_SUFFIXES = {
    ".bin", ".png", ".wav", ".exe", ".dll", ".obj", ".lib", ".a", ".o", ".so",
    ".dylib", ".gz", ".pdb", ".ilk", ".recipe", ".ko", ".spv", ".cso", ".pyc",
    ".nupkg",
}
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
UNTAGGED_RE = re.compile(r"(?:^|\s)(?://|#|/\*)\s*TODO\b(?!\s*\[[A-Z0-9-]+\])")
DIAGRAM_RE = re.compile(
    r"```|^\s*[|+\-=>]{3,}|\|.+\||offset|byte\s*\d|mermaid|diagrama",
    re.IGNORECASE | re.MULTILINE,
)
COMPLEX_MODULES = {
    "dual_backend_3d", "clvm", "http_parser", "bytecode_vm_from_scratch",
    "bytecode_branch_vm", "miniobjdump", "linear_autograd", "tiled_matmul_cache",
    "distro_pkg_rootfs", "kernel_module_driver_lab", "vulkan_d3d12_resource_states",
    "portal_verlet_physics",
}

MIN_TEORIA = 120
MIN_RESOLUCAO_SIMPLE = 80
MIN_RESOLUCAO_COMPLEX = 100
MAX_RESOLUCAO = 450
MAX_LINE_CHARS = 200


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def line_count(path: Path) -> int:
    return len(text(path).splitlines())


def has_test_marker(test_text: str, ident: str) -> bool:
    return (
        f"PEDAGOGY-TEST: {ident}" in test_text
        or f"PEDAGOGY-TEST [{ident}]" in test_text
        or f"PEDAGOGY-TEST [{ident}]:" in test_text
    )


def has_solution_marker(sol_text: str, ident: str) -> bool:
    return (
        f"PEDAGOGY-SOLUTION: {ident}" in sol_text
        or f"SOLVES [{ident}]" in sol_text
    )


def collect_test_text(starter: Path) -> str:
    parts: list[str] = []
    for candidate in [starter / "tests", starter]:
        if not candidate.exists():
            continue
        for p in candidate.rglob("*"):
            if any(part in SKIP_DIR_NAMES for part in p.parts):
                continue
            if p.suffix.lower() in SKIP_FILE_SUFFIXES:
                continue
            if p.is_file() and (
                p.suffix.lower() in CODE_EXT
                or p.name.startswith("test_")
                or p.name == "test.js"
                or p.name.endswith("_test.py")
            ):
                try:
                    parts.append(text(p))
                except UnicodeDecodeError:
                    continue
    return "\n".join(parts)


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def is_complex(module: Path) -> bool:
    return module.name in COMPLEX_MODULES


def check_module(module: Path, root: Path, errors: list[str]) -> int:
    rel = module.relative_to(root)
    total = 0
    required = [
        "README.md",
        "TEORIA_PASSO_A_PASSO.md",
        "PESQUISA_GUIADA.md",
        "EXERCICIOS.md",
        "RESOLUCAO_GUIADA_PASSO_A_PASSO.md",
        "TESTES_GUIADOS.md",
        "BENCHMARK_GUIADO.md",
        "starter",
        "solutions",
    ]
    for req in required:
        if not (module / req).exists():
            errors.append(f"{rel}: missing {req}")

    teoria_path = module / "TEORIA_PASSO_A_PASSO.md"
    res_path = module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    if teoria_path.exists():
        tl = line_count(teoria_path)
        if tl < MIN_TEORIA:
            errors.append(f"{rel}: TEORIA has {tl} lines (min {MIN_TEORIA})")
        body = text(teoria_path)
        if not DIAGRAM_RE.search(body):
            errors.append(f"{rel}: TEORIA missing diagram/table/offset block")
        if "ao implementar este tópico, consulte os todos" in body.lower():
            errors.append(f"{rel}: TEORIA contains generic filler paragraphs")
        pq_count = len(re.findall(r"por qu[eê]", body, re.IGNORECASE))
        if pq_count < 3:
            errors.append(f"{rel}: TEORIA needs >=3 'Por quê/Por que' sections (found {pq_count})")

    if res_path.exists():
        rl = line_count(res_path)
        min_r = MIN_RESOLUCAO_COMPLEX if is_complex(module) else MIN_RESOLUCAO_SIMPLE
        if rl < min_r:
            errors.append(f"{rel}: RESOLUCAO has {rl} lines (min {min_r})")
        if rl > MAX_RESOLUCAO and not (module / "RESOLUCAO_APENDICE.md").exists():
            errors.append(
                f"{rel}: RESOLUCAO has {rl} lines (max {MAX_RESOLUCAO}); add RESOLUCAO_APENDICE.md"
            )
        res_body = text(res_path)
        if "relatório de resolução" not in res_body.lower() and "relatorio de resolucao" not in res_body.lower():
            errors.append(f"{rel}: RESOLUCAO missing '## Relatório de resolução' section")
        low = res_body.lower()
        for label, needles in [
            ("debug/depur", ("debug", "depur")),
            ("esperad", ("esperad",)),
            ("starter/", ("starter/",)),
        ]:
            if not any(n in low for n in needles):
                errors.append(f"{rel}: resolution missing operational token {label}")
        if "bloco completo de loops está no gabarito" in low:
            errors.append(f"{rel}: resolution delegates essential work to solution")
        if "parte a — preparação" in low and "mapa exato" not in low:
            errors.append(f"{rel}: RESOLUCAO uses generic template without 'Mapa exato starter'")
        if not any(x in low for x in ("por que", "por quê", "porque funciona")):
            errors.append(f"{rel}: RESOLUCAO missing 'Por que funciona?' reasoning per step")
        if "mapa exato" not in low:
            errors.append(f"{rel}: RESOLUCAO missing 'Mapa exato starter → resolução' section")

    starter = module / "starter"
    tg_path = module / "TESTES_GUIADOS.md"
    tg = text(tg_path) if tg_path.exists() else ""
    test_text_early = collect_test_text(starter) if starter.exists() else ""

    bench_path = module / "BENCHMARK_GUIADO.md"
    if bench_path.exists():
        bench_full = text(bench_path)
        bench = bench_full.lower()
        if "resultados observados" not in bench:
            errors.append(f"{rel}: BENCHMARK_GUIADO missing '## Resultados observados'")
        else:
            obs = bench_full.lower().split("## resultados observados", 1)[-1]
            has_number = bool(re.search(r"\d", obs))
            has_skip = "não executado" in obs or "nao executado" in obs or "n/a" in obs
            if not has_number and not has_skip:
                errors.append(f"{rel}: BENCHMARK_GUIADO results need numeric metric or honest skip")

    sol = module / "solutions"
    if not starter.exists() or not sol.exists():
        return total

    res = text(res_path) if res_path.exists() else ""
    if not tg:
        tg = text(tg_path) if tg_path.exists() else ""
    test_text = collect_test_text(starter) if starter.exists() else test_text_early
    seen_ids: set[str] = set()

    caso_nums = re.findall(r"### Caso (\d+):", tg)
    for num in caso_nums:
        if f"Caso {num}" not in test_text and f"caso {num}" not in test_text.lower():
            errors.append(f"{rel}: TESTES_GUIADOS Caso {num} not referenced in starter test code")

    for p in starter.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if not p.is_file() or p.suffix.lower() not in CODE_EXT:
            continue
        if p.suffix.lower() in SKIP_FILE_SUFFIXES:
            continue
        try:
            st = text(p)
        except UnicodeDecodeError:
            continue
        for line in st.splitlines():
            if len(line) > MAX_LINE_CHARS and "http" not in line.lower():
                if "PEDAGOGY-TEST" in line and line.strip().startswith("//"):
                    continue  # allow long pedagogy marker lines in tests
                errors.append(
                    f"{rel}: starter/{p.relative_to(starter)} line >{MAX_LINE_CHARS} chars (minified?)"
                )
                break
        found = TODO_RE.findall(st)
        cleaned = TODO_RE.sub("", st)
        if "TODO" in cleaned and UNTAGGED_RE.search(cleaned):
            errors.append(f"{rel}: untagged TODO in starter/{p.relative_to(starter)}")
        rp = p.relative_to(starter)
        sp = sol / rp
        for ident in found:
            if ident in seen_ids:
                continue
            seen_ids.add(ident)
            total += 1
            if not sp.exists():
                errors.append(f"{rel}: TODO {ident} has no solutions/{rp}")
                continue
            stsol = text(sp)
            if not has_solution_marker(stsol, ident):
                errors.append(f"{rel}: {ident} missing PEDAGOGY-SOLUTION in solutions/{rp}")
            if ident in TODO_RE.findall(stsol):
                errors.append(f"{rel}: {ident} remains TODO in solution/{rp}")
            if ident not in res:
                errors.append(f"{rel}: {ident} missing from resolution")
            starter_ref = f"starter/{rp.as_posix()}"
            if starter_ref not in res and f"`{starter_ref}`" not in res:
                errors.append(f"{rel}: resolution missing {starter_ref} for {ident}")
            if ident not in tg:
                errors.append(f"{rel}: {ident} missing from TESTES_GUIADOS")
            if "REVIEW" not in ident and not has_test_marker(test_text, ident):
                errors.append(f"{rel}: {ident} missing PEDAGOGY-TEST in test code")
            # Semantic: RESOLUCAO should include a code fence for each TODO
            ident_pos = res.find(ident)
            if ident_pos >= 0:
                window = res[ident_pos : ident_pos + 2500]
                if "```" not in window:
                    errors.append(f"{rel}: {ident} missing code block in RESOLUCAO near TODO section")

    if not seen_ids:
        errors.append(f"{rel}: no tagged TODOs in starter")

    if (starter / "CMakeLists.txt").exists():
        tests_dir = starter / "tests"
        if tests_dir.exists():
            for label, base in [("starter", starter), ("solutions", sol)]:
                cm = base / "CMakeLists.txt"
                if not cm.exists():
                    errors.append(f"{rel}: {label}/CMakeLists.txt missing")
                    continue
                c = text(cm)
                if "enable_testing" not in c or "add_test" not in c:
                    errors.append(f"{rel}: {label} does not register CTest")

    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified pedagogy check for a day folder")
    parser.add_argument("--day", required=True, help="Day folder name, e.g. 2026-09-03")
    parser.add_argument("--all-days", action="store_true", help="Check all days under days/")
    args = parser.parse_args()

    day_dirs: list[Path] = []
    if args.all_days:
        day_dirs = sorted(
            p for p in (ROOT / "days").iterdir()
            if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", p.name)
        )
    else:
        day_dirs = [ROOT / "days" / args.day]

    all_errors: list[str] = []
    grand_total = 0
    for day_dir in day_dirs:
        if not day_dir.exists():
            all_errors.append(f"day folder missing: {day_dir}")
            continue
        modules = find_modules(day_dir)
        if not modules:
            all_errors.append(f"{day_dir.name}: no modules found")
            continue
        day_total = 0
        for module in modules:
            day_total += check_module(module, ROOT, all_errors)
        grand_total += day_total
        print(f"{day_dir.name}: {len(modules)} modules, {day_total} TODO mappings")

    if all_errors:
        print("PEDAGOGY CHECK UNIFIED FAILED")
        for e in all_errors:
            print(" -", e)
        return 1

    print(f"PEDAGOGY CHECK UNIFIED PASS — {grand_total} TODO mappings across {len(day_dirs)} day(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
