"""Unified pedagogy gate for any day folder under days/YYYY-MM-DD/."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_EXT = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js", ".mjs", ".cs",
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
    "verlet_rope_3d", "graphics_reference",
    "clvm_js_codegen", "clvm_bytecode_verifier", "clvm_v2_strings",
    "hid_keyboard_boot", "ps2_mouse_input", "clvm_v2_verify", "input_event_span",
    "artillery_trajectory_2d", "raster_depth_parity",
    "hid_report_fuzz", "measurement_born", "input_event_entropy", "input_event_transform",
}
COMPLEX_TODOS = {
    "CLVM-JS-CALL-01", "CLVM-VFY-STACK-01", "CLVM-V2-POOL-01", "CLVM-V2-PRINTS-01",
    "HID-KBD-READ-04", "PS2-MOUSE-READ-04", "CLVM-RS-V2-STACK-04", "DN-INPUT-HID-03",
}
DELEGATION_RE = re.compile(
    r"(?:^|[^ãá])\b(?:copie|veja)\b(?!\s+(?:o\s+)?gabarito)[^\n]*\bsolutions\b|"
    r"\bcomo em\b.*\bsolutions\b|"
    r"\bcompare com solutions\b",
    re.IGNORECASE | re.MULTILINE,
)
STRICT_PEDAGOGY_FROM = "2026-09-03"
LEGACY_GOLD_DAY = "2026-09-03"
STRICT_ALL_OVERRIDE: bool = False
MIN_CODE_LINES_SIMPLE = 3
MIN_CODE_LINES_COMPLEX = 8
DUPLICATE_LINE_THRESHOLD = 0.15

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


def is_gfx_module(module: Path, root: Path) -> bool:
    rel = module.relative_to(root).as_posix()
    return "/graphics/" in f"/{rel}/" or module.name == "graphics_reference"


GFX_VISUAL_EXEMPT = {
    "graphics_reference",
    "vulkan_d3d12_resource_states",
    "resource_state_tracker",
    "pipeline_state_object",
    "gpu_timer_query",
    "shader_stage_fsm",
    "alpha_blend_scanline",
}
GFX_WIN32_DIRS = (
    "software_win32",
    "opengl_win32",
    "d3d11_win32",
    "extension",
    "src",  # portal / legacy layout
)


def gfx_solution_win32_sources(module: Path) -> list[Path]:
    sol = module / "solutions"
    if not sol.exists():
        return []
    out: list[Path] = []
    for sub in GFX_WIN32_DIRS:
        base = sol / sub
        if not base.exists():
            continue
        for p in base.rglob("*.cpp"):
            if any(s in SKIP_DIR_NAMES for s in p.parts):
                continue
            try:
                body = text(p)
            except (OSError, UnicodeDecodeError):
                continue
            if "WinMain" in body or "wWinMain" in body:
                out.append(p)
    # legacy: solutions/src/main_opengl.cpp
    for p in sol.glob("src/main_opengl.cpp"):
        if p.is_file():
            out.append(p)
    return out


def gfx_solution_has_present(module: Path) -> bool:
    sol = module / "solutions"
    if not sol.exists():
        return False
    for p in sol.rglob("*.cpp"):
        if any(s in SKIP_DIR_NAMES for s in p.parts):
            continue
        try:
            body = text(p)
        except (OSError, UnicodeDecodeError):
            continue
        if (
            "StretchDIBits" in body
            or "SwapBuffers" in body
            or ".Present(" in body
            or ("Present(" in body and "SwapChain" in body)
        ):
            return True
    return False


def check_gfx_visual_solutions(rel: str, module: Path, errors: list[str]) -> None:
    if module.name in GFX_VISUAL_EXEMPT:
        return
    if not is_gfx_module(module, ROOT):
        return
    module_present = gfx_solution_has_present(module)
    entries = gfx_solution_win32_sources(module)
    if not entries:
        return
    for src in entries:
        body = text(src)
        rel_src = src.relative_to(module).as_posix()
        if "CreateWindow" not in body and "CreateWindowEx" not in body:
            errors.append(f"{rel}: GFX solutions {rel_src} missing CreateWindow (visual required)")
        if not module_present:
            errors.append(f"{rel}: GFX solutions missing present (StretchDIBits/SwapBuffers/D3D Present)")
            break
        if "MessageBox" in body and not module_present:
            if "while (" not in body and "PeekMessage" not in body:
                errors.append(f"{rel}: GFX solutions {rel_src} looks like MessageBox demo stub")


def check_gfx_module(rel: str, module: Path, tg: str, errors: list[str]) -> None:
    comp = module / "docs" / "COMPARISON.md"
    if not comp.exists():
        errors.append(f"{rel}: GFX module missing docs/COMPARISON.md")
        return
    body = text(comp).lower()
    if "software" not in body and "cpu" not in body:
        errors.append(f"{rel}: COMPARISON.md missing CPU/software column")
    if "opengl" not in body and "| gl" not in body:
        errors.append(f"{rel}: COMPARISON.md missing OpenGL column")
    if module.name not in GFX_VISUAL_EXEMPT and "visual-01" not in tg.lower():
        errors.append(f"{rel}: GFX module missing VISUAL-01 in TESTES_GUIADOS")
    check_gfx_visual_solutions(rel, module, errors)


def is_legacy_gold_day(module: Path) -> bool:
    return LEGACY_GOLD_DAY in module.parts


def legacy_todo_satisfied(res: str, ident: str) -> bool:
    """Day 03 gold modules: mapa + substantive RESOLUCAO counts as per-TODO coverage."""
    if ident not in res or "```" not in res or "starter/" not in res:
        return False
    return bool(re.search(rf"\|\s*`?{re.escape(ident)}`?\s*\|", res))


def is_starter_frozen(module: Path) -> bool:
    readme = module / "README.md"
    if not readme.exists():
        return False
    body = readme.read_text(encoding="utf-8", errors="replace").lower()
    return "starter_frozen" in body or "starter já resolvido" in body or "starters já resolvidos" in body


def is_strict_day(module: Path) -> bool:
    if is_starter_frozen(module):
        return True  # strict on pedagogy docs only; starters untouched by policy
    if STRICT_ALL_OVERRIDE:
        return True
    for part in module.parts:
        if DAY_DIR_RE.match(part):
            return part[:10] >= STRICT_PEDAGOGY_FROM
    return False


DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(-v\d+)?$")


def has_placement_block(window: str) -> bool:
    """True if the RESOLUCAO window tells exactly where to edit code."""
    low = window.lower()
    if "onde colocar" in low:
        return True
    has_file = "arquivo" in low or "starter/" in low
    has_anchor = (
        "função" in low
        or "funcao" in low
        or "âncora" in low
        or "ancora" in low
        or "todo [" in low
        or "localize" in low
    )
    has_edit = (
        "substituir" in low
        or "inserir" in low
        or "cole " in low
        or "cole isto" in low
        or "cole o" in low
        or "substitua" in low
    )
    return has_file and has_anchor and has_edit


def duplicate_line_ratio(body: str) -> float:
    skip_prefixes = (
        "| **Arquivo** |",
        "| **Função / âncora** |",
        "| **Funcao / ancora** |",
        "| **Substituir** |",
        "| **Não mexer** |",
        "| **Nao mexer** |",
        "| | |",
        "|--|--|",
        "### Onde colocar",
        "### 5. Verifique",
    )
    lines = []
    for ln in body.splitlines():
        s = ln.strip()
        if not s:
            continue
        if any(s.startswith(p) for p in skip_prefixes):
            continue
        if "Rode os testes do módulo com" in s:
            continue
        if "**Esperado:** caso(s) em TESTES_GUIADOS" in s:
            continue
        if s == "|--|--|" or s.startswith("|---"):
            continue
        if s == "---":
            continue
        if s.startswith("```"):
            continue
        lines.append(s)
    if len(lines) < 5:
        return 0.0
    from collections import Counter
    counts = Counter(lines)
    dup_chars = sum(c - 1 for c in counts.values() if c > 1)
    return dup_chars / len(lines)


LAZY_FILLER_RES = [
    re.compile(r"anote no papel valores concretos antes de editar", re.I),
    re.compile(r"valide compreens[aã]o b[aá]sica do conceito central", re.I),
    re.compile(r"implemente os todos principais do", re.I),
    re.compile(r"satisfaz o caso documentado em testes_guiados", re.I),
    re.compile(r"caso extra \d+ — edge case documentado", re.I),
    re.compile(r"ver teste com pedagogy-test", re.I),
    re.compile(r"leia readme e fixtures", re.I),
    re.compile(r"amplie o laborat[oó]rio \(performance, formato real", re.I),
    re.compile(r"trate edge cases documentados em `?testes_guiados", re.I),
    re.compile(r"m[oó]dulo [a-z0-9_/]+ no dia 0\d", re.I),
    re.compile(r"tema dia 0[89]|tema dia 10", re.I),
    re.compile(r"para `?[A-Z0-9-]+`?: a implementa[cç][aã]o em `starter/", re.I),
    re.compile(r"anote entrada → transforma[cç][aã]o → sa[ií]da num[eé]rica", re.I),
    re.compile(r"desenhe no papel o fluxo de dados", re.I),
    re.compile(r"anote cada byte ou estado com offset", re.I),
    re.compile(r"vocabul[aá]rio usado nos testes", re.I),
    re.compile(r"erros devem ir para o relat[oó]rio de", re.I),
    re.compile(r"evita falha silenciosa quando integrado", re.I),
]


def has_lazy_filler(body: str) -> str | None:
    for rx in LAZY_FILLER_RES:
        if rx.search(body):
            return rx.pattern
    return None


def has_teoria_padding(body: str, strict: bool) -> bool:
    if re.search(r"nota pedag[oó]gica\s+\d+", body, re.IGNORECASE):
        return True
    if "revise o todo e escreva um parágrafo" in body.lower():
        return True
    if not strict:
        return False
    if duplicate_line_ratio(body) > DUPLICATE_LINE_THRESHOLD:
        return True
    # consecutive near-duplicate lines
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    run = 1
    for i in range(1, len(lines)):
        if lines[i] == lines[i - 1]:
            run += 1
            if run > 10:
                return True
        else:
            run = 1
    return False


def check_anti_delegation(rel: str, body: str, errors: list[str], label: str) -> None:
    for line in body.splitlines():
        if re.search(r"não copie|nao copie", line, re.I):
            continue
        if DELEGATION_RE.search(line):
            errors.append(f"{rel}: {label} delegates to solutions (forbidden)")


def count_code_lines_in_window(window: str) -> int:
    blocks = re.findall(r"```[^\n]*\n(.*?)```", window, re.DOTALL)
    total = 0
    for block in blocks:
        for ln in block.splitlines():
            if ln.strip() and not ln.strip().startswith("#"):
                total += 1
    return total


def todo_windows_for_ident(res: str, ident: str) -> list[str]:
    """Prefer ## sections headed by TODO id; skip mapa-table-only matches."""
    heading = re.compile(
        rf"^##[^\n]*{re.escape(ident)}[^\n]*\n",
        re.MULTILINE | re.IGNORECASE,
    )
    windows: list[str] = []
    for m in heading.finditer(res):
        start = m.start()
        windows.append(res[start : start + 8000])
    if windows:
        return windows
    # Exercício headings
    ex = re.compile(
        rf"^##\s+Exercício[^\n]*{re.escape(ident)}[^\n]*\n",
        re.MULTILINE | re.IGNORECASE,
    )
    for m in ex.finditer(res):
        start = m.start()
        windows.append(res[start : start + 8000])
    if windows:
        return windows
    positions = [m.start() for m in re.finditer(re.escape(ident), res)]
    for pos in positions:
        # skip if inside markdown table row
        line_start = res.rfind("\n", 0, pos) + 1
        line_end = res.find("\n", pos)
        line = res[line_start:line_end if line_end != -1 else len(res)]
        if line.strip().startswith("|"):
            continue
        windows.append(res[pos : pos + 4000])
    return windows


def todo_section_ok(window: str, ident: str) -> tuple[bool, str]:
    low = window.lower()
    has_problem = (
        "o problema" in low
        or "### 1." in low
        or "## 1." in low
        or "**o quê:**" in low
        or "### o quê" in low
        or "#### problema" in low
        or "parte a" in low
        or "localize" in low
        or "abra" in low
    )
    has_verify = (
        "verifique" in low
        or "verificação" in low
        or "verificacao" in low
        or "checkpoint" in low
        or "deve ser" in low
        or "deve apontar" in low
        or "resultado deve" in low
        or "ctest" in low
    )
    min_lines = MIN_CODE_LINES_COMPLEX if ident in COMPLEX_TODOS else MIN_CODE_LINES_SIMPLE
    code_lines = count_code_lines_in_window(window)
    if not has_problem:
        return False, "missing O problema / ### 1."
    if not has_verify:
        return False, "missing Verifique"
    if code_lines < min_lines:
        return False, f"code block has {code_lines} lines (min {min_lines})"
    return True, ""


def check_module(module: Path, root: Path, errors: list[str]) -> int:
    rel = module.relative_to(root)
    strict = is_strict_day(module)
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

    tg_path = module / "TESTES_GUIADOS.md"
    tg_early = text(tg_path) if tg_path.exists() else ""
    if is_gfx_module(module, root):
        check_gfx_module(rel, module, tg_early, errors)

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
        lazy = has_lazy_filler(body)
        if lazy:
            errors.append(f"{rel}: TEORIA contains lazy scaffold filler ({lazy})")
        teoria_strict_pad = strict and duplicate_line_ratio(body) > 0.28
        if has_teoria_padding(body, strict) and (teoria_strict_pad or re.search(r"nota pedag[oó]gica\s+\d+", body, re.I)):
            errors.append(f"{rel}: TEORIA contains padding or excessive duplicate lines")
        if strict:
            check_anti_delegation(rel, body, errors, "TEORIA")
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
        if "mapa exato" not in low and "mapa starter" not in low:
            errors.append(f"{rel}: RESOLUCAO missing 'Mapa exato starter → resolução' section")
        if strict and "## baseline" not in low and not re.search(r"^##\s*\d*\.?\s*baseline", res_body, re.I | re.M):
            errors.append(f"{rel}: RESOLUCAO missing '## Baseline' section")
        if strict and not is_legacy_gold_day(module):
            check_anti_delegation(rel, res_body, errors, "RESOLUCAO")
            placement_count = res_body.lower().count("onde colocar")
            pad_threshold = 0.40 if placement_count >= 2 else DUPLICATE_LINE_THRESHOLD
            if duplicate_line_ratio(res_body) > pad_threshold:
                errors.append(f"{rel}: RESOLUCAO contains padding or excessive duplicate lines")
            elif has_teoria_padding(res_body, strict) and placement_count < 2:
                errors.append(f"{rel}: RESOLUCAO contains padding or excessive duplicate lines")
        lazy_res = has_lazy_filler(res_body)
        if lazy_res:
            errors.append(f"{rel}: RESOLUCAO contains lazy scaffold filler ({lazy_res})")

    for extra_name in ("EXERCICIOS.md", "TESTES_GUIADOS.md", "PESQUISA_GUIADA.md"):
        extra_path = module / extra_name
        if not extra_path.exists():
            continue
        lazy_extra = has_lazy_filler(text(extra_path))
        if lazy_extra:
            errors.append(f"{rel}: {extra_name} contains lazy scaffold filler ({lazy_extra})")

    starter = module / "starter"
    tg = tg_early if tg_early else (text(tg_path) if tg_path.exists() else "")
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
    appendice_path = module / "RESOLUCAO_APENDICE.md"
    if appendice_path.exists():
        res = res + "\n\n" + text(appendice_path)
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
            # Semantic: RESOLUCAO should include a code fence + placement for each TODO
            legacy_ok = is_legacy_gold_day(module) and legacy_todo_satisfied(res, ident)
            positions = [m.start() for m in re.finditer(re.escape(ident), res)]
            windows = todo_windows_for_ident(res, ident)
            if not windows and positions:
                windows = [res[pos : pos + 4000] for pos in positions]
            if windows:
                has_code = any("```" in w for w in windows)
                if not has_code:
                    sections = re.split(r"\n(?=## )", res)
                    has_code = any(ident in s and "```" in s for s in sections)
                if not has_code and not legacy_ok:
                    errors.append(f"{rel}: {ident} missing code block in RESOLUCAO near TODO section")
                has_place = any(has_placement_block(w) for w in windows)
                if not has_place:
                    sections = re.split(r"\n(?=## )", res)
                    has_place = any(
                        ident in s and has_placement_block(s) for s in sections
                    )
                if not has_place and not legacy_ok:
                    errors.append(
                        f"{rel}: {ident} missing placement block "
                        f"(Onde colocar / Arquivo+Função+Substituir|Inserir)"
                    )
                for w in windows:
                    ok, reason = todo_section_ok(w, ident)
                    if ok:
                        break
                else:
                    if strict and not legacy_ok and windows and any(
                        w.lstrip().startswith("##") for w in windows
                    ):
                        errors.append(f"{rel}: {ident} shallow RESOLUCAO section ({reason})")
            elif strict and not legacy_ok:
                errors.append(f"{rel}: {ident} missing RESOLUCAO section for TODO")

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
    parser.add_argument("--day", help="Day folder name, e.g. 2026-09-03 or 2026-09-05-v2")
    parser.add_argument("--all-days", action="store_true", help="Check all days under days/")
    parser.add_argument(
        "--strict-all",
        action="store_true",
        help="Apply strict pedagogy rules to every day (same as STRICT_PEDAGOGY_FROM=2026-09-03)",
    )
    args = parser.parse_args()

    global STRICT_ALL_OVERRIDE
    if args.strict_all:
        STRICT_ALL_OVERRIDE = True

    if not args.all_days and not args.day:
        parser.error("provide --day or --all-days")

    day_dirs: list[Path] = []
    if args.all_days:
        day_dirs = sorted(
            p for p in (ROOT / "days").iterdir()
            if p.is_dir() and DAY_DIR_RE.match(p.name) and not p.name.endswith("-v2")
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

    # Day-level contract (multi-trilha + infra sync)
    try:
        from day_contract_check import check_day as check_day_contract
    except ImportError:
        sys.path.insert(0, str(ROOT / "scripts"))
        from day_contract_check import check_day as check_day_contract

    for day_dir in day_dirs:
        contract_errors, contract_warnings = check_day_contract(day_dir)
        for w in contract_warnings:
            print(f"WARN: {w}")
        all_errors.extend(contract_errors)

    if all_errors:
        print("PEDAGOGY CHECK UNIFIED FAILED (day contract)")
        for e in all_errors:
            print(" -", e)
        return 1

    print(f"PEDAGOGY CHECK UNIFIED PASS — {grand_total} TODO mappings across {len(day_dirs)} day(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
