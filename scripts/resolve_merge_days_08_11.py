#!/usr/bin/env python3
"""Resolve merge conflicts for days 08–11: keep deep local curriculum + add GitHub tracks."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def strip_conflict(text: str, prefer: str = "head") -> str:
    """Remove conflict markers; prefer head or incoming body for single-conflict files."""

    def repl(m: re.Match) -> str:
        head, inc = m.group(1), m.group(2)
        return head if prefer == "head" else inc

    return re.sub(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>>[^\n]*\n?", repl, text, flags=re.S)


def head_only(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    if "<<<<<<<" not in t:
        return t
    return strip_conflict(t, "head").rstrip() + "\n"


GH08 = [
    ("systems/spsc_ring_buffer", "C++", "SPSC ring push/pop/size", "D6-SPSC-01..03", "push até cheio; pop FIFO"),
    ("architecture/cache_set_sim", "C++", "cache set decode/hit/evict", "D6-CACHE-*", "set/tag decode → hit → evict"),
    ("ai/online_softmax", "Python", "online softmax stats/normalize", "D6-SM-*", "mesmo contrato numérico estável"),
    ("redteam/wasm_binary_triage", "Python", "WASM header/ULEB/sections", "D6-WASM-*", "magic \\0asm + uleb"),
    ("parsers/nfa_to_dfa", "Python", "ε-closure / subset / match", "D6-DFA-*", "NFA→DFA no papel"),
    ("agent/bm25_code_ranker", "Python", "BM25 tokenize/index/score", "D6-BM25-*", "rank docs=score"),
    ("unix/xargs_lite", "Python", "split/batch/run", "D6-XARGS-*", "batch sem shell=True"),
    ("nodejs/worker_transfer", "JS", "worker transferables", "D6-NODE-*", "ArrayBuffer transfer"),
    ("dotnet/gc_allocation_probe", ".NET", "alloc/new/pool probe", "D6-DN-*", "contagem de alocações"),
]

GH08_TODOS = [
    "D6-SPSC-PUSH", "D6-SPSC-POP", "D6-SPSC-SIZE",
    "D6-CACHE-DECODE", "D6-CACHE-HIT", "D6-CACHE-EVICT",
    "D6-SM-STATS", "D6-SM-NORMALIZE", "D6-SM-REFERENCE",
    "D6-WASM-HEADER", "D6-WASM-ULEB", "D6-WASM-SECTIONS",
    "D6-DFA-CLOSURE", "D6-DFA-SUBSET", "D6-DFA-MATCH",
    "D6-BM25-TOKENIZE", "D6-BM25-INDEX", "D6-BM25-SCORE", "D6-BM25-EVAL",
    "D6-XARGS-SPLIT", "D6-XARGS-BATCH", "D6-XARGS-RUN",
    "D6-NODE-WORKER", "D6-NODE-TRANSFER", "D6-NODE-RECEIVE",
    "D6-DN-ALLOC", "D6-DN-NEW", "D6-DN-POOL",
]

CORE08 = [
    ("systems/clvm_disassembler", "C", "PUSH/JMP sizes"),
    ("systems/clvm_peephole_opt", "C++", "peephole fold"),
    ("linux/input_event_ring_mux", "C", "ring CAP4"),
    ("rust/clvm_disasm", "Rust", "ISA Result"),
    ("dotnet/pe_export_span", ".NET", "e_lfanew/export"),
    ("graphics/shader_stage_fsm", "C++", "shader FSM"),
    ("redteam/pe_export_triage", "Python", "MZ triage"),
    ("quantum/bell_state_prep", "C++", "Bell P=0.5"),
    ("ai/softmax_stable", "C", "stable softmax"),
    ("nodejs/duplex_event_pipe", "JS", "24B framing"),
    ("parsers/json_rd_lexer", "C", "JSON lexer"),
    ("agent/tool_protocol_fsm", "Python", "tool FSM"),
    ("tooling/wasm_section_header", "ASM", "WASM magic"),
]


def resolve_day08() -> None:
    day = ROOT / "days" / "2026-09-08"
    base = head_only(day / "ATIVIDADES.md")
    # drop trailing if any leftover markers
    base = re.sub(r"=======[\s\S]*$", "", base).rstrip()

    appendix = """

---

## Trilha paralela A — GitHub (concorrência, cache, ranking) (10–14 h)

Estas pastas vieram do remote e **também estão no dia**. São um eixo diferente (SPSC/cache/BM25/NFA),
não substituto do toolchain CLVM acima. Faça depois do Bloco 1–4 ou em paralelo se já dominar bytecode.

| Módulo | Linguagem | Paper-trace / foco |
|--------|-----------|-------------------|
"""
    for path, lang, focus, _todos, trace in GH08:
        appendix += f"| `{path}` | {lang} | {trace} — {focus} |\n"

    appendix += """
**Checkpoint conceitual (trilha A):**

- [ ] Desenhei SPSC cheio vs vazio (índices head/tail)
- [ ] Decodei set/tag de um endereço no cache sim
- [ ] Tracei ε-closure de um NFA mínimo no papel
- [ ] Sei por que `xargs_lite` usa `shell=False`
- [ ] Diferencio `softmax_stable` (C, dia core) de `online_softmax` (Python, trilha A)

**Gate trilha A:**

```powershell
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions
```

(os módulos novos devem aparecer no runner junto com o core)

### Por que manter as duas trilhas

- **Core (local):** ISA CLVM + ABI + PE + trilhas obrigatórias tier-A multilíngue — melhor para o fio pedagógico Dias 07→11.
- **Trilha A (GitHub):** laboratórios clássicos (SPSC, cache, NFA→DFA, BM25) com benchmarks — melhor para sistemas/IR/search.
- Juntas: **22 módulos**. Não é redundância: `softmax_stable` ≠ `online_softmax`; ring mux ≠ SPSC; wasm asm ≠ wasm triage.
"""
    # Fix header count
    if "**Dia:** 13 módulos" in base:
        base = base.replace("**Dia:** 13 módulos", "**Dia:** 22 módulos (13 core + 9 trilha GitHub)", 1)
    elif "13 módulos" in base[:200]:
        base = base.replace("13 módulos", "22 módulos (13 core + 9 trilha GitHub)", 1)

    (day / "ATIVIDADES.md").write_text(base + appendix + "\n", encoding="utf-8", newline="\n")

    # TODO_MAP: collect all from starters
    ids: list[str] = []
    seen: set[str] = set()
    for mod in sorted(day.glob("*/*")):
        if not (mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").exists():
            continue
        starter = mod / "starter"
        if not starter.exists():
            continue
        for p in starter.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".py", ".c", ".cpp", ".h", ".hpp", ".cs", ".js", ".mjs", ".rs", ".asm", ".S"}:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for tid in re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", text):
                if tid not in seen:
                    seen.add(tid)
                    ids.append(tid)
    todo = "# TODO map — 2026-09-08\n\nCore (CLVM/trilhas) + trilha GitHub (D6-*).\n\n"
    todo += "\n".join(f"- `{i}`" for i in ids) + "\n"
    (day / "TODO_MAP.md").write_text(todo, encoding="utf-8", newline="\n")

    # VALIDATION
    val = """# Validação — 2026-09-08

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-08
python scripts/day_contract_check.py --day 2026-09-08
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions
```

## Módulos core (13)

"""
    for path, lang, _ in CORE08:
        val += f"- `{path}` — {lang}\n"
    val += "\n## Trilha paralela GitHub (9)\n\n"
    for path, lang, focus, *_ in GH08:
        val += f"- `{path}` — {lang} ({focus})\n"
    val += """
## Notas do remote

Benchmarks observados no remote (online_softmax / BM25) estão em `benchmarks/results-2026-09-08.*`.
`dotnet/gc_allocation_probe` exige .NET SDK (presente nesta máquina).
"""
    (day / "VALIDATION.md").write_text(val, encoding="utf-8", newline="\n")

    # README
    readme = """# Day 2026-09-08 — CLVM toolchain + trilha GitHub (cache/SPSC/BM25)

**22 módulos:** 13 core multilíngue (CLVM/PE/ASM) + 9 da trilha paralela trazida do GitHub.

## Core (ordem cognitiva)

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
"""
    for i, (path, lang, fund) in enumerate(CORE08, 1):
        readme += f"| {i} | `{path}` | **{lang}** | {fund} | 2–3 |\n"
    readme += """
## Trilha paralela GitHub

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
"""
    for i, (path, lang, fund, *_ ) in enumerate(GH08, 14):
        readme += f"| {i} | `{path}` | **{lang}** | {fund} | 2–3 |\n"
    readme += """
**Total:** ~40–50 h (pode fatiar core num dia e trilha A no seguinte).

C/C++/ASM: Visual Studio 18 2026 via `run_day_tests.py` (Ninja + cl).
"""
    (day / "README.md").write_text(readme, encoding="utf-8", newline="\n")

    # START_HERE append if needed
    sh = day / "START_HERE.md"
    if sh.exists():
        body = sh.read_text(encoding="utf-8")
        if "Trilha paralela GitHub" not in body:
            body = body.rstrip() + """

## Trilha paralela GitHub (opcional no mesmo dia)

Depois do core CLVM, ou em sessão separada: `spsc_ring_buffer` → `cache_set_sim` → `nfa_to_dfa` → `bm25_code_ranker`.
Ver bloco correspondente em `ATIVIDADES.md`.
"""
            sh.write_text(body + "\n", encoding="utf-8", newline="\n")


def resolve_day_with_appendix(day_name: str, gh_items: list[tuple[str, str]], projects_note: str) -> None:
    day = ROOT / "days" / day_name
    for name in ("ATIVIDADES.md", "README.md", "TODO_MAP.md", "VALIDATION.md"):
        path = day / name
        if not path.exists():
            continue
        body = head_only(path)
        body = re.sub(r"=======[\s\S]*$", "", body).rstrip()
        if name == "ATIVIDADES.md":
            body += "\n\n---\n\n## Atividades extras do GitHub (ainda sem pasta `days/` completa)\n\n"
            body += (
                "O remote listava estes temas; **o código portado está em `projects/`**, "
                "não como módulos canônicos deste dia. Faça como extensão depois do core.\n\n"
            )
            for path_m, title in gh_items:
                body += f"- [ ] `{path_m}` — {title}\n"
            body += f"\n{projects_note}\n"
        path.write_text(body + "\n", encoding="utf-8", newline="\n")


def wire_day08_map() -> None:
    mp = ROOT / "scripts" / "module_project_map.py"
    text = mp.read_text(encoding="utf-8")
    entries = {
        "2026-09-08/systems/spsc_ring_buffer": "projects/chris-driver-lab",
        "2026-09-08/architecture/cache_set_sim": "projects/chris-cpu",
        "2026-09-08/ai/online_softmax": "projects/chris-tensor",
        "2026-09-08/redteam/wasm_binary_triage": "projects/chris-binary-toolkit",
        "2026-09-08/parsers/nfa_to_dfa": "projects/chris-regex",
        "2026-09-08/agent/bm25_code_ranker": "projects/chris-agent-core",
        "2026-09-08/unix/xargs_lite": "projects/chris-xargs",
        "2026-09-08/nodejs/worker_transfer": "projects/chris-node-streaming",
        "2026-09-08/dotnet/gc_allocation_probe": "projects/chris-dotnet-bench",
    }
    if all(k in text for k in entries):
        return
    block = ""
    for key, proj in entries.items():
        if key in text:
            continue
        short = key.split("/")[-1]
        block += f'''
    "{key}": {{
        "project": "{proj}",
        "carry": "{short} from day08 github track",
        "tests": "day08 module tests",
        "milestone": "MILESTONES.md — {short}",
        "commit": "feat(day08): port {short}",
    }},
'''
    if not block:
        return
    idx = text.rfind("\n}")
    # insert before final dict close — find MODULE_PROJECT closing
    # safer: before def module_key
    marker = "\n\ndef module_key"
    if marker in text:
        text = text.replace(marker, ",\n" + block.rstrip().rstrip(",") + "\n}" + marker.replace("\n}", ""), 1)
        # that might break — do cleaner
    text = mp.read_text(encoding="utf-8")
    if "def module_key" in text:
        pre, post = text.split("\ndef module_key", 1)
        # remove trailing } from pre
        pre = pre.rstrip()
        if pre.endswith("}"):
            pre = pre[:-1].rstrip()
            if pre.endswith(","):
                pass
            else:
                pre += ","
            pre = pre + "\n" + block + "\n}\n\n"
            mp.write_text(pre + "def module_key" + post, encoding="utf-8", newline="\n")

    lp = ROOT / "docs" / "LEARNING_PATHS.md"
    lt = lp.read_text(encoding="utf-8")
    if "2026-09-08/systems/spsc_ring_buffer" not in lt:
        lt = lt.rstrip() + "\n\n### Day 08 — trilha paralela GitHub\n\n"
        for i, (path, *_rest) in enumerate(GH08, 1):
            lt += f"| {i} | `2026-09-08/{path}` | trilha A |\n"
        lp.write_text(lt + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    resolve_day08()
    resolve_day_with_appendix(
        "2026-09-09",
        [
            ("systems/buddy_allocator", "Buddy allocator"),
            ("ai/welford_layernorm", "Welford LayerNorm"),
            ("redteam/x86_prologue_triage", "x86 synthetic prologue"),
            ("dotnet/channel_backpressure", "Channel backpressure"),
            ("nodejs/async_context", "AsyncLocalStorage"),
            ("graphics/explicit_barriers", "Vulkan/D3D12 barriers"),
            ("linux/proc_stat_parser", "/proc stat"),
            ("parsers/pratt_expr", "Pratt parser"),
            ("agent/agent_state_machine", "Agent FSM"),
            ("unix/grep_dfa", "grep DFA"),
            ("architecture/branch_predictor", "2-bit predictor"),
        ],
        "Portas em `projects/` (ex.: `chris-agent-core`, `chris-grep`, `chris-render-graph`).",
    )
    resolve_day_with_appendix(
        "2026-09-10",
        [
            ("systems/aba_tagged_freelist", "ABA tagged freelist"),
            ("ai/tiled_attention_online_softmax", "Tiled attention + online softmax"),
            ("architecture/tlb_page_walk", "TLB page walk"),
            ("dotnet/pinned_memory_probe", "Pinned memory probe"),
            ("graphics/descriptor_binding_model", "Descriptor binding"),
            ("linux/procfs_module_lab", "procfs module lab"),
            ("nodejs/message_channel_rpc", "MessageChannel RPC"),
            ("parsers/backtracking_regex_vm", "Backtracking regex VM"),
            ("redteam/elf64_relocation_triage", "ELF64 reloc triage"),
            ("agent/transactional_patcher", "Transactional patcher"),
        ],
        "Portas em `projects/` (ex.: `chris-regex`, `chris-renderer-vulkan`, `chris-linux-module-lab`).",
    )
    resolve_day_with_appendix(
        "2026-09-11",
        [
            ("systems/hazard_pointer_stack", "Hazard pointers"),
            ("ai/kv_cache_ring", "KV-cache ring"),
            ("redteam/dwarf_line_program", "DWARF line program"),
            ("dotnet/jit_callsite_model", "JIT call-site model"),
            ("nodejs/worker_pool_scheduler", "Worker pool scheduler"),
            ("parsers/pike_regex_vm", "Pike regex VM"),
            ("agent/context_budgeter", "Context budgeter"),
            ("quantum/statevector_bitmask", "Statevector bitmask"),
            ("network/length_prefixed_framing", "Length-prefixed framing"),
            ("algorithms/robin_hood_hash", "Robin Hood hash"),
        ],
        "Portas em `projects/` (ex.: `chris-agent-core/context_budgeter.py`, `chris-binary-toolkit/dwarf_line_subset.py`, `chris-qsim`).",
    )
    wire_day08_map()
    # ensure no conflict markers remain
    bad = []
    for p in (ROOT / "days").rglob("*"):
        if p.suffix.lower() not in {".md", ".py", ".json", ".cs", ".js"}:
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if "<<<<<<<" in t:
            bad.append(str(p.relative_to(ROOT)))
    print("resolved; remaining markers:", bad or "none")


if __name__ == "__main__":
    main()
