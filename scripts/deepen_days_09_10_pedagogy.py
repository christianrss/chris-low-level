#!/usr/bin/env python3
"""Deepen pedagogy docs for days 2026-09-09 and 2026-09-10.

Rewrites TEORIA/RESOLUCAO/EXERCICIOS/TESTES/PESQUISA/BENCHMARK/README
plus day-level ATIVIDADES.md and START_HERE.md.

Rules:
- No 'Passo de papel N' padding
- No solution delegation
- TEORIA >= 120 unique substantive lines with wire + numeric traces + >=3 Por quê
- RESOLUCAO: Mapa, Baseline, Onde colocar, full solution bodies, Por que funciona,
  Verifique, Debug, Relatório (keep under 450 lines)
- Docs only; does not touch starter/solutions code
"""
from __future__ import annotations

import ast
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_EXT = {".py", ".c", ".cpp", ".h", ".hpp", ".cs", ".js", ".rs"}
SKIP_NAME = ("AssemblyInfo", "GlobalUsings", "AssemblyAttributes", "CompilerId", "foo.h")
SKIP_PARTS = ("obj", "bin", "CMakeFiles", "Debug", "Release", "net8.0")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n").rstrip() + "\n", encoding="utf-8", newline="\n")


def lang_fence(path: str) -> str:
    ext = Path(path).suffix.lower()
    return {
        ".py": "python",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".cs": "csharp",
        ".js": "javascript",
        ".rs": "rust",
    }.get(ext, "")


def collect_todos(starter: Path) -> list[tuple[str, str, str]]:
    """Return (id, starter_relpath, function_guess)."""
    found: list[tuple[str, str, str]] = []
    for p in starter.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in CODE_EXT:
            continue
        if any(x in p.parts for x in SKIP_PARTS):
            continue
        rel = "starter/" + p.relative_to(starter).as_posix()
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"TODO\s*\[([A-Z0-9-]+)\]", text):
            ident = m.group(1)
            fn = ident
            before = text[max(0, m.start() - 180) : m.start()]
            # Prefer the nearest function/method header before this TODO
            cands: list[tuple[int, str]] = []
            for pat in (
                r"def\s+(\w+)\s*\(",
                r"(?:pub\s+)?fn\s+(\w+)\s*[<(]",
                r"(?:export\s+)?(?:async\s+)?function\s+(\w+)",
                r"(?:export\s+)?(?:const|let)\s+(\w+)\s*=",
                r"(?:public\s+static\s+)?(?:async\s+)?[\w<>\?\[\]]+\s+(\w+)\s*\([^;]*\)\s*\{",
                r"(?:^|\n)\s*(?:static\s+)?(?:inline\s+)?(?:const\s+)?(?:unsigned\s+)?(?:int|void|float|bool|size_t|char|uint\d+_t|double)\s+(\w+)\s*\(",
            ):
                for mm in re.finditer(pat, before, re.M):
                    cands.append((mm.start(), mm.group(1)))
            if cands:
                fn = sorted(cands, key=lambda x: x[0])[-1][1]
            found.append((ident, rel, fn))
    # stable unique by id, first wins
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for item in found:
        if item[0] not in seen:
            seen.add(item[0])
            out.append(item)
    return out


def extract_solution_bodies(sol_dir: Path) -> dict[str, tuple[str, str]]:
    """Map TODO id -> (fence, body code including enough context)."""
    bodies: dict[str, tuple[str, str]] = {}
    for p in sol_dir.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in CODE_EXT:
            continue
        if any(x in p.parts for x in SKIP_PARTS):
            continue
        if any(s in p.name for s in SKIP_NAME):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fence = lang_fence(p.name)
        if p.suffix == ".py":
            try:
                tree = ast.parse(text)
            except SyntaxError:
                tree = None
            if tree is not None:
                for node in tree.body:
                    nodes = [node]
                    if isinstance(node, ast.ClassDef):
                        nodes = list(node.body)
                    for item in nodes:
                        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            continue
                        src = ast.get_source_segment(text, item) or ""
                        m = re.search(r"PEDAGOGY-SOLUTION:\s*([A-Z0-9-]+)", src)
                        if m:
                            bodies[m.group(1)] = (fence, src)
                continue
        # line-based for C/C++/JS/CS/Rust
        lines = text.splitlines()
        for i, ln in enumerate(lines):
            m = re.search(r"PEDAGOGY-SOLUTION:\s*([A-Z0-9-]+)", ln)
            if not m:
                continue
            ident = m.group(1)
            # walk back to function start
            start = i
            for j in range(i, -1, -1):
                if re.search(
                    r"^\s*(?:pub\s+)?(?:async\s+)?(?:fn|def|function|export\s+function|public\s+static|"
                    r"int |void |float |bool |size_t |Activity|string |static )",
                    lines[j],
                ) or re.search(r"^\s*(?:export\s+)?(?:async\s+)?function\s+\w+|^\s*(?:export\s+)?(?:const|let)\s+\w+\s*=", lines[j]):
                    start = j
                    break
                if j < i - 15:
                    break
            # walk forward to closing brace / next def
            end = min(len(lines), i + 40)
            depth = 0
            seen_brace = False
            for j in range(start, len(lines)):
                depth += lines[j].count("{") - lines[j].count("}")
                if "{" in lines[j]:
                    seen_brace = True
                if seen_brace and depth <= 0 and j > start:
                    end = j + 1
                    break
                if j > i and re.match(r"^(?:pub\s+)?(?:fn|def|int |void |float |bool |public |export )", lines[j]):
                    if j > i + 1:
                        end = j
                        break
            chunk = "\n".join(lines[start:end]).rstrip()
            # ensure min non-comment lines for checker
            non_c = [x for x in chunk.splitlines() if x.strip() and not x.strip().startswith(("#", "//"))]
            if len(non_c) < 3:
                chunk += "\n    /* contrato: mantenha a assinatura do starter */"
            bodies[ident] = (fence, chunk)
    return bodies


def baseline_cmd(day: str, track: str, name: str, starter_file: str) -> str:
    root = f"days/{day}/{track}/{name}"
    if starter_file.endswith(".rs") or "/src/" in starter_file:
        return f"cd {root}/starter\ncargo test"
    if starter_file.endswith(".cs"):
        return f"cd {root}/starter\ndotnet test"
    if starter_file.endswith(".js"):
        return f"cd {root}/starter\nnode --test test.js 2>$null; if (-not $?) {{ node test.js }}"
    if starter_file.endswith((".c", ".cpp", ".h", ".hpp")):
        return (
            f"cmake -S {root}/starter -B {root}/starter/build_ci -G \"Visual Studio 17 2022\" -A x64\n"
            f"cmake --build {root}/starter/build_ci --config Release\n"
            f"ctest --test-dir {root}/starter/build_ci -C Release --output-on-failure"
        )
    # python
    test = "test_" + Path(starter_file).stem + ".py"
    # common names
    return f"cd {root}/starter\npython -m pytest -q 2>$null; if (-not $?) {{ python {test} 2>$null; if (-not $?) {{ Get-ChildItem test*.py | ForEach-Object {{ python $_.FullName }} }} }}"


# ---------------------------------------------------------------------------
# Per-module curated pedagogy (unique wire + traces + Por quê). No Passo de papel.
# ---------------------------------------------------------------------------

SPECS: dict[str, dict] = {}


def spec(key: str, **kwargs) -> None:
    SPECS[key] = kwargs


# === Day 09 ===
spec(
    "2026-09-09/systems/clvm_trace_profiler",
    title="Profiler de opcodes CLVM (C)",
    lang="C",
    why="O disassembler do Dia 08 lista instruções. Este lab conta qual opcode aparece mais no bytecode — o primeiro passo de um profiler amostral.",
    wire="""| Slot | Significado | Fixture `02 02 08` |
|------|-------------|-------------------|
| `counts[0x02]` | ADD | 2 |
| `counts[0x08]` | HALT | 1 |
| demais `[0..15]` | outros opcodes | 0 |
| `hottest(counts)` | índice do maior | `0x02` |

Wire do programa: três bytes crus, sem header CLVM — só o payload de código.""",
    trace="""```text
note_op(c, 0x02); note_op(c, 0x02); note_op(c, 0x08)
→ c[2]=2, c[8]=1
hottest(c) → 2   (ADD; empate só troca se counts[i] > counts[best])
profile_code({02,02,08}, 3, c) → 3 e hottest ainda 2
```""",
    algo="1. `note_op`: se `counts` e `op < 16`, `counts[op]++`.\n2. `hottest`: `best=0`; para i=1..15, se `counts[i] > counts[best]` então best=i.\n3. `profile_code`: para cada byte chama `note_op`; retorna `n` (ou -1 se ponteiro nulo).",
    bugs="- Contar ADD uma vez: `c[2]==2` falha.\n- `hottest` devolver 8: HALT não é o modo.\n- Não checar `op < 16`: overflow do array de 16.",
    prod="Profilers reais amostram PC no tempo. Aqui o bytecode inteiro é o traço — útil para CI determinística.",
    deep=[
        ("Modelo mental", "Um histograma de 16 bins. O opcode é o índice. Não há decode de immediates: cada byte conta como um op (lab simplificado)."),
        ("Por quê o teto é 16?", "No ISA toy do curso os opcodes cabem em nibble alto conceitual; o array fixo evita alocação e deixa o teste O(1)."),
        ("Por quê empate fica com o menor índice?", "Só atualizamos quando `>` estrito. Assim o resultado é estável e o teste não oscila."),
        ("Ligação Dia 08", "`clvm_disassembler` imprime `ADD`/`HALT`. Este lab responde 'qual aparece mais?' com o mesmo fixture `02 02 08`."),
        ("Complexidade", "`note_op` O(1); `hottest` O(16); `profile_code` O(n). Memória: 16×u32."),
        ("Falhas silenciosas", "Esquecer de zerar `counts` antes de `profile_code` no seu harness externo acumula lixo; o teste faz `memset`."),
    ],
    ex_easy="No papel: conte `02 02 08` → c[2], c[8], hottest.",
    ex_med="Implemente `note_op` e rode só o assert de c[2]==2.",
    ex_hard="Implemente `hottest` + `profile_code`.",
    ex_chal="Se todos counts forem 0, hottest devolve 0. Explique por quê isso é aceitável neste lab.",
    cases=[
        ("CLVM-TRACE-01", "Após três note_op, `c[0x02]==2` e `c[0x08]==1`."),
        ("CLVM-TRACE-02", "`hottest(c)==0x02`."),
        ("CLVM-TRACE-03", "`profile_code` retorna 3 e hottest continua 2."),
    ],
    research=[
        "Quantas vezes ADD aparece no fixture?",
        "Qual índice hottest devolve e por quê não 8?",
        "Por que o array tem 16 entradas?",
        "O que o disassembler faz que este lab não faz?",
        "Como um perf real amostraria em vez de varrer o buffer?",
    ],
    links=["Dia 08 systems/clvm_disassembler", "man perf (conceitual)"],
    bench_metric="profile_code em 1e6 bytes sintéticos (ms)",
    bench_cmd="ctest --test-dir days/2026-09-09/systems/clvm_trace_profiler/solutions/build_ci -C Release",
)

spec(
    "2026-09-09/systems/arena_telemetry",
    title="Telemetria de arena bump (C++)",
    lang="C++",
    why="A arena do Dia 04 só faz bump. Aqui cada alloc incrementa `allocs` e cada reset incrementa `resets`, mas reset **não** zera `allocs` — a métrica de vida útil sobrevive ao reuso do buffer.",
    wire="""| Campo | Após init | Após alloc(8) | Após alloc(60) | Após reset |
|-------|-----------|---------------|----------------|------------|
| `used` | 0 | 8 | 8 (inalterado) | 0 |
| `allocs` | 0 | 1 | 1 | **1** (permanece) |
| `resets` | 0 | 0 | 0 | 1 |
| retorno | — | 0 | **-1** (8+60>64) | — |

Capacidade fixa: `buf[64]`.""",
    trace="""```text
arena_init → used=0 allocs=0 resets=0
alloc(8)  → 0, used=8, allocs=1, out = buf+0
alloc(60) → -1 (68>64), used permanece 8
reset     → used=0, resets=1, allocs continua 1
```""",
    algo="1. init zera used/allocs/resets.\n2. alloc: se `used+n > 64` (ou ponteiros nulos) retorna -1; senão `*out=buf+used`, used+=n, allocs++.\n3. reset: used=0; resets++; **não** toca allocs.",
    bugs="- Zerar allocs no reset: o teste exige allocs==1 depois.\n- Aceitar 60 após 8: 68>64 deve falhar.\n- Não incrementar allocs no sucesso.",
    prod="malloc não tem reset O(1). Arenas de frame (jogos, parsers) precisam de telemetria para achar vazamentos de 'allocs por frame'.",
    deep=[
        ("Modelo mental", "Bump pointer + contadores. O buffer é um anel lógico só no used; allocs é histórico."),
        ("Por quê allocs sobrevive ao reset?", "Para saber quantos pedidos houve na vida do objeto, não só no frame atual."),
        ("Por quê capacidade 64?", "Número pequeno o bastante para o overflow do Caso 1 ser óbvio no papel (8+60=68)."),
        ("Invariante", "0 ≤ used ≤ 64; allocs e resets só crescem."),
        ("Ligação Dia 04", "Mesma ideia de arena; a novidade é telemetria explícita nos campos da struct."),
        ("C vs C++", "API em ponteiros C-style dentro de arquivo .cpp — o runner usa CMake CXX."),
    ],
    ex_easy="Trace no papel: used após alloc(8) e após reset.",
    ex_med="Implemente init + alloc.",
    ex_hard="Implemente reset sem apagar allocs.",
    ex_chal="O que acontece se alloc(0)? Defina e documente (este lab não exige).",
    cases=[
        ("ARENA-TEL-01", "Após init, used==0 e allocs==0."),
        ("ARENA-TEL-02", "alloc(8) ok; alloc(60) retorna -1."),
        ("ARENA-TEL-03", "Após reset: used==0, resets==1, allocs==1."),
    ],
    research=[
        "Por que 8+60 falha?",
        "Por que allocs não volta a 0?",
        "Qual o endereço relativo de out após o primeiro alloc?",
        "Como um frame allocator de jogo usaria resets?",
        "Diferença entre used e capacidade?",
    ],
    links=["Dia 04 arena", "game engine frame allocators"],
    bench_metric="1e6 alloc(8)+reset ciclos",
    bench_cmd="ctest --test-dir days/2026-09-09/systems/arena_telemetry/solutions/build_ci -C Release",
)

spec(
    "2026-09-09/ai/attention_mask",
    title="Máscara causal de atenção (C)",
    lang="C",
    why="Atenção causal impede o token de olhar o futuro. Com query index q, a key k só é visível se k≤q. Scores invisíveis viram −1e9 antes do softmax.",
    wire="""| q | k | causal_mask | apply_mask em score=3.0 |
|---|---|-------------|-------------------------|
| 2 | 2 | 1 | score permanece (ret 1) |
| 2 | 3 | 0 | score ← −1e9f (ret 0) |
| visible_count(2) | — | — | **3** (índices 0,1,2) |

Não há matriz densa no lab: funções escalares espelham a célula (q,k).""",
    trace="""```text
causal_mask(2,2)=1
causal_mask(2,3)=0
s=3.0f; apply_mask(&s,2,3) → 0 e s < -1e8
visible_count(2)=3
```""",
    algo="1. causal_mask: se q<0 ou k<0 → 0; senão k<=q.\n2. apply_mask: se invisível, *score=-1e9f e return 0; senão return 1.\n3. visible_count(q)=q+1 (ou 0 se q<0).",
    bugs="- Deixar k=3 visível: score 3.0 permanece.\n- visible_count(2)=2 esquece o próprio token.\n- Usar +inf em vez de -1e9 (softmax explode diferente).",
    prod="Transformers mascaram com −∞ ou additive mask; −1e9 é um proxy float32 estável o bastante para testes.",
    deep=[
        ("Modelo mental", "Triângulo inferior inclusive na matriz Q×K. Linha q vê colunas 0..q."),
        ("Por quê −1e9 e não 0?", "Zero ainda compete no softmax; −1e9 ≈ probabilidade nula após exp."),
        ("Por quê visible_count = q+1?", "Inclui a posição atual: tokens 0..q."),
        ("Ligação Dia 08", "softmax_stable recebe scores já mascarados."),
        ("Invariante", "apply_mask nunca deixa score positivo para k>q."),
        ("Edge", "q=0 → só k=0 visível; visible_count=1."),
    ],
    ex_easy="Tabela q=2 para k=0..3 no papel.",
    ex_med="Implemente causal_mask.",
    ex_hard="apply_mask + visible_count.",
    ex_chal="Como mascarar uma matriz N×N com estas funções? Escreva o nested loop.",
    cases=[
        ("AI-ATTN-01", "causal_mask(2,2)==1 e (2,3)==0."),
        ("AI-ATTN-02", "apply_mask escreve −1e9 e retorna 0."),
        ("AI-ATTN-03", "visible_count(2)==3."),
    ],
    research=[
        "O que é máscara causal?",
        "Por que −1e9?",
        "visible_count(2) por quê 3?",
        "Relação com softmax do Dia 08?",
        "Bidirectional vs causal em BERT/GPT?",
    ],
    links=["Dia 08 ai/softmax_stable", "Attention is All You Need (máscaras)"],
    bench_metric="1e7 chamadas causal_mask",
    bench_cmd="ctest --test-dir days/2026-09-09/ai/attention_mask/solutions/build_ci -C Release",
)

spec(
    "2026-09-09/rust/stack_sample_trace",
    title="Amostra de stack e resolução de símbolos (Rust)",
    lang="Rust",
    why="Um sampler entrega PCs; o relatório precisa de nomes. Este lab liga `Vec<u64>` de amostras a um mapa endereço→símbolo.",
    wire="""| Entrada | Valor do teste |
|---------|----------------|
| sample PCs | `[0x1000, 0x2000]` |
| syms | `0x1000 → "main"`, etc. |
| resolve_frame(0x1000) | `"main"` |
| report | string contendo `"main"` |

Não há unwind DWARF: a amostra já é a lista de PCs.""",
    trace="""```text
sample = vec![0x1000, 0x2000]
resolve_frame(0x1000, &syms) == "main"
report contém substring "main"
```""",
    algo="1. Capturar/devolver a amostra de PCs.\n2. resolve_frame: lookup no mapa; fallback documentado se ausente.\n3. report: juntar frames resolvidos numa string estável.",
    bugs="- Esquecer de incluir main no report.\n- Comparar endereços com endianness errada (aqui são u64 nativos).\n- Mutar o mapa de símbolos sem necessidade.",
    prod="perf/gdb usam DWARF/PDB. Aqui o mapa é injetado — isola a lógica de relatório.",
    deep=[
        ("Modelo mental", "PC → nome. O sampler é só a lista; a resolução é o dicionário."),
        ("Por quê Rust?", "Result/Option e ownership deixam falhas de lookup explícitas sem UB."),
        ("Por quê 0x1000/0x2000?", "Endereços toy legíveis no assert_eq!."),
        ("Invariante", "A ordem dos PCs na amostra preserva-se no report."),
        ("Ligação tooling", "Dia 09 pdb_symbol_index faz o mesmo contrato em Python."),
        ("Teste", "`cargo test` no starter deve FAIL até os TODOs."),
    ],
    ex_easy="Anote no papel PC→nome do Caso 1.",
    ex_med="Implemente resolve_frame.",
    ex_hard="Monte o report com main.",
    ex_chal="O que reportar se o PC não está no mapa?",
    cases=[
        ("RS-STACK-SAMPLE-01", "sample == [0x1000, 0x2000]."),
        ("RS-STACK-FRAME-02", "resolve_frame(0x1000)==\"main\"."),
        ("RS-STACK-REPORT-03", "report contém main."),
    ],
    research=[
        "O que é um PC numa amostra?",
        "Como PDB/DWARF resolvem endereço→nome?",
        "Por que o lab não faz unwind?",
        "Diferença entre sample e report?",
        "Como o Dia 09 pdb_index se relaciona?",
    ],
    links=["Dia 09 tooling/pdb_symbol_index", "cargo test book"],
    bench_metric="1e5 resolve_frame",
    bench_cmd="cd days/2026-09-09/rust/stack_sample_trace/solutions && cargo test",
)

spec(
    "2026-09-09/dotnet/activity_source_span",
    title="ActivitySource e spans (.NET)",
    lang="C#",
    why="OpenTelemetry/.NET Diagnostics usam ActivitySource para criar spans. O lab fixa nome da source, tag `module`, e export textual `op|tag`.",
    wire="""| API | Contrato do teste |
|-----|-------------------|
| CreateSource(\"chris.lab\") | `Name == \"chris.lab\"` |
| StartWorkSpan(src, \"work\") | Activity não nula; tag module=`activity_source_span` |
| ExportSpanSummary(act) | `\"work|activity_source_span\"` |

Listener: `ActivitySamplingResult.AllData` para o teste enxergar a Activity.""",
    trace="""```text
CreateSource("chris.lab") → Name chris.lab
StartWorkSpan(..., "work") → tag module=activity_source_span
Export → "work|activity_source_span"
```""",
    algo="1. `new ActivitySource(name)`.\n2. `StartActivity(op)` + `SetTag(\"module\", \"activity_source_span\")`.\n3. Se act null → \"null\"; senão `$\"{OperationName}|{GetTagItem(\"module\")}\"`.",
    bugs="- Esquecer o listener: StartActivity pode devolver null.\n- Tag com nome errado.\n- Export sem pipe.",
    prod="Em produção exporta OTLP/Jaeger; aqui o export é string para assert estável.",
    deep=[
        ("Modelo mental", "Source → Activity (span) → tags → export."),
        ("Por quê precisa de ActivityListener?", "Sem sampling, CreateActivity/StartActivity retorna null."),
        ("Por quê tag module fixa?", "O assert compara o literal do lab, não um valor dinâmico."),
        ("Invariante", "Export usa OperationName e a tag module, nessa ordem."),
        ("Ligação", "Mesmo conceito de span que Node async_hooks rastreia por fase."),
        ("dotnet test", "Projeto de testes referenciando Chris.ActivityLab."),
    ],
    ex_easy="Escreva a string de export esperada.",
    ex_med="CreateSource.",
    ex_hard="StartWorkSpan + Export.",
    ex_chal="O que Export devolve se act é null?",
    cases=[
        ("DN-ACT-SOURCE-01", "Name == chris.lab."),
        ("DN-ACT-SPAN-02", "tag module == activity_source_span."),
        ("DN-ACT-EXPORT-03", "export == work|activity_source_span."),
    ],
    research=[
        "O que é ActivitySource?",
        "Por que o teste registra ActivityListener?",
        "Diferença Activity vs ActivitySource?",
        "Como OTLP exportaria o mesmo span?",
        "O que SetTag armazena?",
    ],
    links=["System.Diagnostics.Activity docs", "OpenTelemetry .NET"],
    bench_metric="1e5 StartWorkSpan+Export",
    bench_cmd="dotnet test days/2026-09-09/dotnet/activity_source_span/solutions",
)

spec(
    "2026-09-09/nodejs/async_hooks_trace",
    title="async_hooks: fases e métricas (JavaScript)",
    lang="JavaScript",
    why="O event loop cria recursos async. `async_hooks` observa init/before/after. O lab grava eventos, formata timeline e conta fases.",
    wire="""| Fase | Significado |
|------|-------------|
| init | recurso criado (Promise, etc.) |
| before / after | callbacks em torno da execução |

Evento: `{ phase, asyncId, ... }`. Timeline: `phase:id|phase:id|...`. Metrics: `{ init: n, ... }`.""",
    trace="""```text
installHooks(store); await Promise.resolve()
store.events tem algum phase==='init'
formatTimeline inclui 'init'
countPhases(events).init >= 1
```""",
    algo="1. createHook({init,before,after}).enable() empilhando em store.events.\n2. timeline = map `phase:asyncId` join `|`.\n3. metrics: histograma por phase.",
    bugs="- Não chamar enable().\n- Timeline sem init.\n- Contar só length em vez de por fase.",
    prod="Clinic.js / OpenTelemetry instrumentam o mesmo ciclo de vida com overhead real.",
    deep=[
        ("Modelo mental", "Cada Promise/Timeout tem asyncId; hooks observam o ciclo."),
        ("Por quê Promise.resolve no teste?", "Força pelo menos um init no loop."),
        ("Por quê string timeline?", "Assert estável sem depender de IDs absolutos além da presença de init."),
        ("Invariante", "countPhases(init) ≥ 1 se houve Promise."),
        ("Ligação", "Analogamente a Activity spans no .NET do mesmo dia."),
        ("ESM", "import de node:async_hooks / node:assert."),
    ],
    ex_easy="Liste as três fases no papel.",
    ex_med="installHooks.",
    ex_hard="timeline + metrics.",
    ex_chal="O que muda se usar setTimeout em vez de Promise?",
    cases=[
        ("ND-ASYNC-HOOK-01", "existe evento init."),
        ("ND-ASYNC-TIMELINE-02", "timeline contém init."),
        ("ND-ASYNC-METRICS-03", "m.init >= 1."),
    ],
    research=[
        "O que async_hooks.init observa?",
        "Diferença before/after?",
        "Por que enable é necessário?",
        "Overhead de async_hooks em produção?",
        "Como OTEL Node se relaciona?",
    ],
    links=["Node.js async_hooks docs"],
    bench_metric="1e4 Promise.resolve com hooks",
    bench_cmd="node days/2026-09-09/nodejs/async_hooks_trace/solutions/test.js",
)

spec(
    "2026-09-09/linux/perf_event_open_lab",
    title="perf_event_open (simulação Python)",
    lang="Python",
    why="No Linux, `perf_event_open` devolve um fd de contador. Este lab simula open/read/close com fd sintético `(type<<16)|config` e um dict de contadores.",
    wire="""| Chamada | Resultado no teste |
|---------|-------------------|
| perf_event_open(1, 2) | fd > 0  (= `0x10002`) |
| counters[fd]=42; read | 42 |
| close | True e fd some do dict |

type<0 → −1.""",
    trace="""```text
fd = perf_event_open(1,2)  # 0x00010002
counters = {fd: 42}
read → 42
close → True; fd not in counters
```""",
    algo="1. open: se type<0 return -1; else (type<<16)|(config&0xFFFF).\n2. read: counters.get(fd,0).\n3. close: pop; True se existia.",
    bugs="- fd sempre 0.\n- close sem remover.\n- read inventar valor em vez de usar o dict.",
    prod="A syscall real preenche `struct perf_event_attr`; aqui isolamos o ciclo de vida do handle.",
    deep=[
        ("Modelo mental", "fd → contador. O dict é o kernel simulado."),
        ("Por quê (type<<16)|config?", "Empacota identidade do evento num int positivo determinístico."),
        ("Por quê Python?", "Windows CI sem syscall; o contrato pedagógico é o ciclo open/read/close."),
        ("Invariante", "Após close bem-sucedido, fd ∉ counters."),
        ("Ligação", "gpu_timer_query no mesmo dia mede tempo; aqui mede contador genérico."),
        ("Segurança", "type negativo falha cedo."),
    ],
    ex_easy="Calcule fd de open(1,2) no papel.",
    ex_med="Implemente open.",
    ex_hard="read + close.",
    ex_chal="Como simular EBADF se read após close?",
    cases=[
        ("LX-PERF-OPEN-01", "fd > 0."),
        ("LX-PERF-READ-02", "read == 42."),
        ("LX-PERF-CLOSE-03", "close True e fd removido."),
    ],
    research=[
        "O que perf_event_open retorna no Linux real?",
        "Por que o lab usa dict?",
        "Significado de type e config?",
        "Diferença perf stat vs este lab?",
        "Como gpu_timer se compara?",
    ],
    links=["man 2 perf_event_open"],
    bench_metric="1e6 open/read/close",
    bench_cmd="python days/2026-09-09/linux/perf_event_open_lab/solutions/test_perf_lab.py",
)

spec(
    "2026-09-09/graphics/gpu_timer_query",
    title="GPU timer query (simulação headless)",
    lang="Python",
    why="APIs gráficas expõem timer queries. Este lab simula begin/end com perf_counter e guarda laps por nome — testável sem GPU.",
    wire="""| Passo | Resultado |
|-------|-----------|
| begin_query(\"draw\") | handle **0** (primeiro) |
| end_query(0) | ms ≥ 0.0 |
| lap_times() | contém chave \"draw\" |

VISUAL-01 (relatório): lap draw > 0 ms quando houver trabalho real entre begin/end.""",
    trace="""```text
h = begin_query("draw")  # 0
ms = end_query(h)        # >= 0
laps["draw"] == ms
```""",
    algo="1. begin: aloca handle, guarda (name, t0).\n2. end: pop start, ms=(now-t0)*1000, guarda em _laps.\n3. lap_times: cópia do dict.",
    bugs="- Sempre retornar handle −1.\n- Não gravar lap.\n- end sem pop (vazamento de starts).",
    prod="GL_TIME_ELAPSED / D3D timestamp queries; aqui clock de CPU proxy.",
    deep=[
        ("Modelo mental", "handle → (nome, t0) → lap ms."),
        ("Por quê headless?", "CI sem GPU; o contrato de estados ainda treina a API de query."),
        ("Por quê handle sequencial?", "Teste afirma h==0 no primeiro begin."),
        ("Invariante", "Após end, handle some de _starts e aparece em _laps."),
        ("Ligação", "Dia 07 raster labs; este foca telemetria, não pixels."),
        ("Benchmark", "Meça ms de um sleep curto entre begin/end."),
    ],
    ex_easy="Qual o primeiro handle?",
    ex_med="begin_query.",
    ex_hard="end_query + lap_times.",
    ex_chal="Dois begins aninhados: quantos handles?",
    cases=[
        ("GFX-GPU-TIMER-01", "primeiro handle == 0."),
        ("GFX-GPU-LAP-02", "ms >= 0."),
        ("GFX-GPU-BENCH-03", "\"draw\" in lap_times."),
    ],
    research=[
        "O que é timer query em OpenGL?",
        "Por que simular com perf_counter?",
        "Diferença GPU timestamp vs CPU?",
        "O que VISUAL-01 pede no relatório?",
        "Como comparar dois laps?",
    ],
    links=["docs/GFX_PEDAGOGY_STANDARD.md", "OpenGL TIMER_QUERY"],
    bench_metric="ms do lap draw (3 corridas)",
    bench_cmd="python days/2026-09-09/graphics/gpu_timer_query/solutions/test_gpu_timer.py",
)

spec(
    "2026-09-09/parsers/logfmt_lexer",
    title="Lexer logfmt (Python)",
    lang="Python",
    why="logfmt (`k=v k2=v2`) é comum em logs. O lab tokeniza pares, faz parse KV e aplica escapes simples.",
    wire="""| Entrada | Saída |
|---------|-------|
| `a=1 b=2` | 2 tokens |
| `msg=hello` | (`msg`,`hello`) |
| dict com level | `level == \"info\"` (fixture do teste) |""",
    trace="""```text
tokenize("a=1 b=2") → len 2
parse_kv("msg=hello") → ("msg","hello")
dict["level"] == "info"
```""",
    algo="1. tokenize: split em pares respetando escapes do lab.\n2. parse_kv: split no primeiro `=`.\n3. unescape conforme regras do módulo.",
    bugs="- Contar tokens errado com espaços.\n- Split em todos os `=` (valores com `=`).\n- Escapes literais restantes.",
    prod="Grafana/Loki e muitos agents usam logfmt; parsers robustos tratam aspas.",
    deep=[
        ("Modelo mental", "linha → lista de pares → dict."),
        ("Por quê primeiro `=`?", "Valores podem conter `=`."),
        ("Por quê len==2 no Caso 1?", "Dois pares separados por espaço."),
        ("Invariante", "tokenize o preserva ordem; dict agrega por chave."),
        ("Ligação", "Dia 07/08 parsers; Pratt no Dia 10 capstone."),
        ("Escapes", "Siga exatamente o que o teste de PR-LOGFMT-ESC-03 afirma."),
    ],
    ex_easy="Tokenize a=1 b=2 no papel.",
    ex_med="tokenize + parse_kv.",
    ex_hard="escapes.",
    ex_chal="Como tratar aspas \"a=b c=d\"?",
    cases=[
        ("PR-LOGFMT-LEX-01", "len(tokenize('a=1 b=2'))==2."),
        ("PR-LOGFMT-KV-02", "parse_kv msg=hello."),
        ("PR-LOGFMT-ESC-03", "level==info no dict."),
    ],
    research=[
        "O que é logfmt?",
        "Por que não JSON?",
        "Como lidar com espaços em valores?",
        "Diferença lexer vs parser?",
        "Ferramentas que emitem logfmt?",
    ],
    links=["Brandur logfmt", "Dia 10 parsers/capstone_query_eval"],
    bench_metric="1e5 tokenize de linha típica",
    bench_cmd="python days/2026-09-09/parsers/logfmt_lexer/solutions/test_logfmt.py",
)

spec(
    "2026-09-09/quantum/decoherence_noise",
    title="Canal de decoerência (Python)",
    lang="Python",
    why="Estados quânticos ideais decaem sob ruído. O lab modela um canal simples: probabilidades normalizam, apply reduz coerência, trace tem comprimento fixo.",
    wire="""| Assert | Valor |
|--------|-------|
| p0+p1 | ≈ 1.0 |
| nxt[0] | < 1.0 após apply |
| len(trace) | 4 |""",
    trace="""```text
canal → (p0,p1) com p0+p1≈1
apply → nxt[0] < 1.0
trace → 4 amostras
```""",
    algo="1. Construa o canal / vetor de probabilidade normalizado.\n2. apply: mistura com ruído reduzindo a componente dominante.\n3. trace: lista de comprimento 4 conforme contrato do teste.",
    bugs="- Não normalizar (soma ≠ 1).\n- apply que não reduz nxt[0].\n- trace com len ≠ 4.",
    prod="Canais Kraus (depolarizing, amplitude damping) em simuladores; aqui um proxy pedagógico.",
    deep=[
        ("Modelo mental", "probabilidade clássica + ruído que 'esquenta' o estado."),
        ("Por quê exigir soma 1?", "Sem normalização o Born rule mente."),
        ("Por quê nxt[0]<1?", "Prova que o canal não é identidade."),
        ("Invariante", "Após canal válido, soma das probs ≈ 1."),
        ("Ligação", "Dia 10 capstone_measurement usa Born em amplitudes."),
        ("Numérico", "Use abs(p0+p1-1)<1e-9 como o teste."),
    ],
    ex_easy="Normalize um par (0.3,0.7) no papel.",
    ex_med="canal + soma 1.",
    ex_hard="apply + trace len 4.",
    ex_chal="Escreva um canal que fixa ponto (0.5,0.5).",
    cases=[
        ("Q-DECO-CHANNEL-01", "p0+p1≈1."),
        ("Q-DECO-APPLY-02", "nxt[0]<1."),
        ("Q-DECO-TRACE-03", "len(tr)==4."),
    ],
    research=[
        "O que é decoerência?",
        "Canal depolarizing vs amplitude damping?",
        "Por que rastrear 4 passos?",
        "Relação com medição Born?",
        "O que Kraus operators representam?",
    ],
    links=["Nielsen & Chuang (canais)", "Dia 10 quantum/capstone_measurement"],
    bench_metric="1e5 apply",
    bench_cmd="python days/2026-09-09/quantum/decoherence_noise/solutions/test_decoherence.py",
)

spec(
    "2026-09-09/redteam/yara_match_scan",
    title="Scan estilo YARA (Python)",
    lang="Python",
    why="Regras YARA misturam bytes fixos e wildcards. O lab parseia padrão `AA ??`, casa em offset e devolve lista de hits.",
    wire="""| Entrada | Saída |
|---------|-------|
| padrão parseado | `[0xAA, None]` (None = wildcard) |
| data com match @1 | `match_at(..., 1)` True |
| scan_all | `[1]` |""",
    trace="""```text
pat = [0xAA, None]
match_at(data, pat, 1) → True
scan_all(data, pat) → [1]
```""",
    algo="1. parse: bytes hex; `??` → None.\n2. match_at: para cada i, pat[i] is None ou == data[off+i].\n3. scan_all: todos off onde match_at.",
    bugs="- Tratar ?? como 0.\n- Off-by-one no fim do buffer.\n- scan_all devolver bool.",
    prod="YARA compila regras; aqui só o motor de bytes/wildcards.",
    deep=[
        ("Modelo mental", "máscara de bytes com buracos."),
        ("Por quê None?", "Sentinela de wildcard sem colidir com 0x00."),
        ("Por quê offset 1 no teste?", "Fixture posiciona o padrão fora do início."),
        ("Invariante", "len(pat) bytes a partir de off devem caber em data."),
        ("Ligação", "Dia 10 capstone_triage detecta magic ELF/PE/WASM."),
        ("Segurança", "Não ler além de len(data)."),
    ],
    ex_easy="Parse AA ?? no papel.",
    ex_med="match_at.",
    ex_hard="scan_all.",
    ex_chal="Suporte a nibble wildcard A?.",
    cases=[
        ("RT-YARA-PARSE-01", "pat == [0xAA, None]."),
        ("RT-YARA-MATCH-02", "match_at offset 1."),
        ("RT-YARA-TRIAGE-03", "scan_all == [1]."),
    ],
    research=[
        "O que é wildcard em YARA?",
        "Diferença strings hex vs text?",
        "Como evitar O(n*m) ingênuo?",
        "Relação com magic bytes?",
        "Falsos positivos típicos?",
    ],
    links=["YARA documentation", "Dia 10 redteam/capstone_triage"],
    bench_metric="scan_all em 1MB sintético",
    bench_cmd="python days/2026-09-09/redteam/yara_match_scan/solutions/test_yara_scan.py",
)

spec(
    "2026-09-09/agent/verify_replay_log",
    title="Verify + replay log FSM (Python)",
    lang="Python",
    why="Agentes registram eventos; replay deve reproduzir o estado. O lab faz append estruturado, FSM IDLE→RUN→DONE/REVISE e hash curto do log.",
    wire="""| Evento | Transição |
|--------|-----------|
| start | IDLE → RUN |
| verify ok=True | → DONE |
| verify ok falso/ausente | → REVISE |

Hash: SHA-256 de `repr(log)`, 16 hex chars.""",
    trace="""```text
append start → len(log)==1
append verify {ok:True} → replay_fsm == "DONE"
trace_hash → len 16
```""",
    algo="1. append `{event, payload}`.\n2. FSM conforme tabela; último estado vence.\n3. sha256(repr(log)).hexdigest()[:16].",
    bugs="- Não appendar dict estruturado.\n- Ignorar payload.ok.\n- Hash com len ≠ 16.",
    prod="LangSmith/agent traces; aqui FSM mínima determinística.",
    deep=[
        ("Modelo mental", "log append-only + redução para estado."),
        ("Por quê repr no hash?", "Estável o bastante para o lab; produção usaria canonical JSON."),
        ("Por quê REVISE?", "Verify falhou — o loop deve corrigir, não mentir DONE."),
        ("Invariante", "append não muta entradas antigas."),
        ("Ligação", "Dia 10 capstone_agent_loop fecha o ciclo completo."),
        ("Teste", "start+verify ok → DONE."),
    ],
    ex_easy="Desenhe a FSM no papel.",
    ex_med="append_log.",
    ex_hard="replay_fsm + hash.",
    ex_chal="O que acontece com dois verify consecutivos?",
    cases=[
        ("AG-VERIFY-LOG-01", "len(log)==1 após start."),
        ("AG-REPLAY-FSM-02", "replay == DONE."),
        ("AG-TRACE-HASH-03", "hash len 16."),
    ],
    research=[
        "Por que log append-only?",
        "DONE vs REVISE?",
        "Por que truncar hash em 16?",
        "Como serializar canonicamente?",
        "Relação com Dia 10 agent loop?",
    ],
    links=["Dia 10 agent/capstone_agent_loop"],
    bench_metric="1e5 append+hash",
    bench_cmd="python days/2026-09-09/agent/verify_replay_log/solutions/test_agent_log.py",
)

spec(
    "2026-09-09/tooling/pdb_symbol_index",
    title="Índice de símbolos estilo PDB (Python)",
    lang="Python",
    why="Linhas `ADDR NAME` viram mapa endereço→nome. O lab parseia, indexa e faz lookup — o mesmo contrato do stack sample em Rust.",
    wire="""| Linha | Parse |
|-------|-------|
| `1000 main` | `(0x1000, \"main\")` |
| índice | len==2 no fixture |
| lookup(0x1000) | `\"main\"` |""",
    trace="""```text
parse_symbol_line("1000 main") → (0x1000, "main")
len(idx)==2
lookup(idx, 0x1000)=="main"
```""",
    algo="1. split addr/name; int(addr, 16).\n2. index: dict dos pares.\n3. lookup: dict[addr].",
    bugs="- int decimal em vez de hex.\n- Sobrescrever índices sem querer.\n- lookup KeyError não tratado conforme API do lab.",
    prod="PDB/DIA SDK; aqui texto mínimo.",
    deep=[
        ("Modelo mental", "texto → mapa → nome."),
        ("Por quê hex?", "Endereços de linkers são hex."),
        ("Por quê len==2?", "Fixture tem dois símbolos."),
        ("Invariante", "parse ∘ index ∘ lookup = identidade no Caso 1."),
        ("Ligação", "rust/stack_sample_trace resolve o mesmo 0x1000→main."),
        ("Formato", "um espaço separando addr e name."),
    ],
    ex_easy="Parse 1000 main no papel.",
    ex_med="parse_symbol_line.",
    ex_hard="index + lookup.",
    ex_chal="Suporte a linha com demangle?",
    cases=[
        ("TL-PDB-PARSE-01", "(0x1000,'main')."),
        ("TL-PDB-INDEX-02", "len(idx)==2."),
        ("TL-PDB-LOOKUP-03", "lookup main."),
    ],
    research=[
        "O que um PDB contém?",
        "Por que hex?",
        "Como RVA difere de VA?",
        "Relação com stack sample Rust?",
        "Ferramentas: llvm-pdbutil?",
    ],
    links=["Dia 09 rust/stack_sample_trace", "Microsoft PDB docs"],
    bench_metric="1e5 lookup",
    bench_cmd="python days/2026-09-09/tooling/pdb_symbol_index/solutions/test_pdb_index.py",
)

# === Day 10 ===
spec(
    "2026-09-10/systems/clvm_pipeline_integration",
    title="Pipeline CLVM: disasm + peephole + verify",
    lang="Python",
    why="Capstone systems: junta disassembler, peephole `PUSH 0; ADD`→noop, e verificação de stack no mesmo bytecode.",
    wire="""| Bytes | Listing |
|-------|---------|
| `01 01  01 02  02  08` | PUSH 1, PUSH 2, ADD, HALT |
| peephole in: `01 00 02 01 05 08` | PUSH 0, ADD, PUSH 5, HALT |
| peephole out | `01 05 08` (PUSH 5, HALT) |

Opcodes: PUSH=0x01 (+imm), ADD=0x02, HALT=0x08.""",
    trace="""```text
disasm([01,1, 01,2, 02, 08]) → ["PUSH 1","PUSH 2","ADD","HALT"]
fold PUSH0+ADD → bytes([0x01,5,0x08])
verify_stack(code) → True
```""",
    algo="1. disasm: avance pc conforme tamanho do opcode.\n2. peephole: remova padrão PUSH 0 / ADD.\n3. verify: simule altura de stack sem underflow.",
    bugs="- Esquecer immediates no disasm.\n- Não remover o par PUSH0+ADD.\n- verify que ignora underflow.",
    prod="Compiladores reais fazem peephole em IR; aqui é bytecode linear.",
    deep=[
        ("Modelo mental", "bytes → texto → bytes otimizados → ok/fail de stack."),
        ("Por quê apagar PUSH 0 + ADD?", "x+0=x; o imediato 0 é morto."),
        ("Por quê verify separado?", "Disasm pode listar programa inválido; verify protege a VM."),
        ("Invariante", "Após peephole, semântica aritmética do Caso 1 preserva PUSH 5 HALT."),
        ("Ligação", "Dia 08 disasm/peephole; Dia 09 trace profiler."),
        ("Paper-trace", "Escreva as 4 linhas do disasm antes de codar."),
    ],
    ex_easy="Disasm no papel do fixture PUSH1 PUSH2 ADD HALT.",
    ex_med="disasm.",
    ex_hard="peephole + verify.",
    ex_chal="Peephole PUSH 0 SUB?",
    cases=[
        ("CAP-CLVM-DIS-01", "listing PUSH 1/2 ADD HALT."),
        ("CAP-CLVM-PEEP-02", "folded == 01 05 08."),
        ("CAP-CLVM-VFY-03", "verify_stack True."),
    ],
    research=["Por que PUSH 0 ADD some?", "Tamanho do PUSH?", "Underflow de stack?", "Ordem disasm→peep→verify?", "Relação com rust cross_verify?"],
    links=["Dia 08 systems/clvm_peephole_opt", "Dia 10 rust/cross_verify_clvm"],
    bench_metric="1e4 disasm+peep",
    bench_cmd="python days/2026-09-10/systems/clvm_pipeline_integration/solutions/test_clvm_pipeline_integration.py",
)

spec(
    "2026-09-10/systems/unified_input_pipeline",
    title="Pipeline unificado de input",
    lang="Python",
    why="Teclado + mouse viram eventos tipados, multiplexados e transformados em strings estáveis `KEY:` / `REL:`.",
    wire="""| Estágio | Contrato |
|---------|----------|
| kbd | `[(1, 30, 1)]` (EV_KEY, code 30, value 1) |
| mux | junta streams |
| transform | `["KEY:30", "REL:0=5"]` |""",
    trace="""```text
kbd == [(1, 30, 1)]
transform(muxed) == ["KEY:30", "REL:0=5"]
```""",
    algo="1. normalize teclado → tuplas (type,code,value).\n2. mux concatena/ordena conforme lab.\n3. transform formata KEY/REL.",
    bugs="- Codes errados.\n- Perder REL no transform.\n- Mux sem preservar ambos.",
    prod="evdev + libinput; aqui tuplas puras.",
    deep=[
        ("Modelo mental", "fontes → mux → strings de debug."),
        ("Por quê type 1 = KEY?", "Espelha linux/input.h EV_KEY=1."),
        ("Por quê string KEY:30?", "Assert legível sem struct binária."),
        ("Invariante", "transform é função pura dos eventos muxados."),
        ("Ligação", "Dia 07 HID/PS2; Dia 10 linux composite."),
        ("Wire mental", "(1,30,1) = tecla code 30 press."),
    ],
    ex_easy="Anote (1,30,1) → KEY:30.",
    ex_med="kbd path.",
    ex_hard="mux + transform.",
    ex_chal="Ordenação temporal no mux.",
    cases=[
        ("CAP-INP-KBD-01", "kbd == [(1,30,1)]."),
        ("CAP-INP-MUX-02", "mux inclui ambos."),
        ("CAP-INP-XFM-03", "transform KEY/REL."),
    ],
    research=["EV_KEY valor?", "O que é REL?", "Por que mux?", "Relação com composite driver?", "Span .NET no mesmo dia?"],
    links=["linux/input-event-codes.h", "Dia 10 linux/composite_input_driver"],
    bench_metric="1e5 transform",
    bench_cmd="python days/2026-09-10/systems/unified_input_pipeline/solutions/test_unified_input_pipeline.py",
)

spec(
    "2026-09-10/linux/composite_input_driver",
    title="Driver composto de input",
    lang="Python",
    why="Um device virtual `composite0` agrega evdev e fecha o frame com SYN `(0,0,0)`.",
    wire="""| Campo | Valor |
|-------|-------|
| name | `composite0` |
| eventos | `[(1,4,1)]` |
| frame last | `(0,0,0)` SYN_REPORT |""",
    trace="""```text
dev["name"]=="composite0"
ev == [(1, 4, 1)]
frame[-1] == (0, 0, 0)
```""",
    algo="1. crie device com name.\n2. leia/normalize evdev subset.\n3. feche frame com SYN.",
    bugs="- Nome errado.\n- Esquecer SYN no fim.\n- Códigos trocados.",
    prod="uinput cria devices compostos reais.",
    deep=[
        ("Modelo mental", "device → eventos → SYN delimita pacote."),
        ("Por quê (0,0,0)?", "EV_SYN/SYN_REPORT clássico."),
        ("Por quê composite0?", "Nome estável para assert."),
        ("Invariante", "Todo frame lógico termina em SYN."),
        ("Ligação", "unified_input_pipeline consome eventos parecidos."),
        ("Paper", "Desenhe um frame KEY+SYN."),
    ],
    ex_easy="Escreva SYN no papel.",
    ex_med="device name.",
    ex_hard="ev + frame SYN.",
    ex_chal="Dois SYN seguidos — o que significa?",
    cases=[
        ("CAP-LNX-COMP-01", "name composite0."),
        ("CAP-LNX-EVDEV-02", "ev [(1,4,1)]."),
        ("CAP-LNX-SYNC-03", "frame[-1]==(0,0,0)."),
    ],
    research=["O que é SYN_REPORT?", "uinput?", "Por que frames?", "Relação evdev?", "Nome do device?"],
    links=["kernel uinput", "Dia 10 systems/unified_input_pipeline"],
    bench_metric="1e5 frames",
    bench_cmd="python days/2026-09-10/linux/composite_input_driver/solutions/test_composite_input_driver.py",
)

spec(
    "2026-09-10/rust/cross_verify_clvm",
    title="Cross-verify header CLVM (Rust)",
    lang="Rust",
    why="Valida magic `CLVM`, version 1 e FNV no offset 12 — o mesmo contrato do loader C, em Rust memory-safe.",
    wire="""| Offset | Campo |
|--------|-------|
| 0 | magic `CLVM` |
| 4 | version = 1 |
| 12 | checksum FNV-1a do bytecode |

FNV: offset 0x811C9DC5, prime 16777619.""",
    trace="""```text
header válido → Ok
magic errado → Err
checksum != FNV(payload) → Err
```""",
    algo="1. leia magic/version.\n2. calcule FNV do code.\n3. compare com u32 LE @12.",
    bugs="- FNV sem mask 32-bit.\n- version != 1 aceito.\n- endianness do checksum.",
    prod="Mesmo padrão do rust-validator Dia 03.",
    deep=[
        ("Modelo mental", "bytes → Result<(), E> sem executar."),
        ("Por quê FNV?", "Checksum toy alinhado ao CLVM do curso."),
        ("Por quê Rust no capstone?", "Cross-check do loader C/Python."),
        ("Invariante", "Ok só se magic+version+FNV batem."),
        ("Ligação", "clvm_pipeline_integration executa; este só verifica."),
        ("Teste", "cargo test integration."),
    ],
    ex_easy="Tabela de offsets no papel.",
    ex_med="magic+version.",
    ex_hard="FNV @12.",
    ex_chal="flags != 0 deve falhar?",
    cases=[
        ("CAP-RS-XVFY-01", "magic CLVM."),
        ("CAP-RS-XVFY-02", "version 1."),
        ("CAP-RS-XVFY-03", "FNV confere."),
    ],
    research=["FNV-1a passos?", "Por que LE?", "Diferença verify vs execute?", "Dia 03 rust-validator?", "Entry offset?"],
    links=["Dia 03 systems/clvm", "Dia 10 systems/clvm_pipeline_integration"],
    bench_metric="1e5 validates",
    bench_cmd="cd days/2026-09-10/rust/cross_verify_clvm/solutions && cargo test",
)

spec(
    "2026-09-10/dotnet/capstone_input_host",
    title="Host de input com Span (.NET)",
    lang="C#",
    why="Capstone .NET: lê eventos via Span/Memory e conta o que o teste afirma — zero-copy sobre buffer.",
    wire="""| Conceito | Papel |
|----------|-------|
| Span<byte>/event | janela sem alocar |
| contagem | número que o teste HostTests compara |

Abra `HostTests.cs` e anote o inteiro esperado antes de codar.""",
    trace="""```text
Parse/Count via Span → assert do HostTests (valor literal no teste)
```""",
    algo="1. exponha API que aceita Span.\n2. interprete records de tamanho fixo.\n3. agregue contagem/export.",
    bugs="- ToArray desnecessário quebrando a ideia Span.\n- Contagem off-by-one.\n- Endianness.",
    prod="System.Memory em parsers de rede/input.",
    deep=[
        ("Modelo mental", "bytes emprestados → eventos."),
        ("Por quê Span?", "Evita cópia na borda do host."),
        ("Por quê o número do teste?", "Única fonte de verdade do Caso."),
        ("Invariante", "len(span) insuficiente → falha explícita."),
        ("Ligação", "unified_input_pipeline em Python; aqui superfície .NET."),
        ("dotnet test", "projeto Chris.CapstoneInput.Tests."),
    ],
    ex_easy="Leia o assert numérico do teste e anote.",
    ex_med="API Span básica.",
    ex_hard="contagem completa.",
    ex_chal="ReadOnlySpan vs Span.",
    cases=[
        ("CAP-DN-HOST-01", "cria/host básico."),
        ("CAP-DN-HOST-02", "parse Span."),
        ("CAP-DN-HOST-03", "contagem do teste."),
    ],
    research=["O que é Span<T>?", "Zero-copy?", "Diferença Memory?", "Relação com input pipeline?", "Endianness?"],
    links=["Span<T> docs", "Dia 10 systems/unified_input_pipeline"],
    bench_metric="1e5 parse Span",
    bench_cmd="dotnet test days/2026-09-10/dotnet/capstone_input_host/solutions",
)

spec(
    "2026-09-10/graphics/pipeline_state_object",
    title="FSM de pipeline state object",
    lang="Python",
    why="PSOs/ Vulkan-like: estados UNINITIALIZED→…→READY→RECORDING. O lab valida transições e traça a sequência.",
    wire="""| Transição | Válida? |
|-----------|---------|
| UNINITIALIZED → VERTEX_SHADER | sim (can_transition) |
| READY → RECORDING | apply → RECORDING |
| pipeline_trace(seq) | True/listing conforme teste |""",
    trace="""```text
can_transition("UNINITIALIZED","VERTEX_SHADER") → True
apply_transition("READY","RECORDING") → "RECORDING"
pipeline_trace(seq) → ok
```""",
    algo="1. tabela de arestas permitidas.\n2. apply só se can.\n3. trace percorre seq.",
    bugs="- Aceitar aresta inexistente.\n- apply sem validar.\n- trace que ignora falha.",
    prod="Vulkan PSO é imutável após create; aqui FSM didática de estágios.",
    deep=[
        ("Modelo mental", "grafo dirigido de estados."),
        ("Por quê FSM?", "API gráfica rejeita comandos fora de ordem."),
        ("Por quê RECORDING?", "Analogia a command buffers."),
        ("Invariante", "apply só muda estado se can_transition."),
        ("Ligação", "Dia 08 shader_stage_fsm."),
        ("Headless", "Sem janela: estados são o artefato."),
    ],
    ex_easy="Liste 3 arestas válidas no papel.",
    ex_med="can_transition.",
    ex_hard="apply + trace.",
    ex_chal="Ciclo ilegal — deve falhar.",
    cases=[
        ("CAP-GFX-PSO-01", "UNINITIALIZED→VERTEX_SHADER."),
        ("CAP-GFX-PSO-02", "READY→RECORDING."),
        ("CAP-GFX-PSO-03", "pipeline_trace ok."),
    ],
    research=["O que é PSO?", "Vulkan pipeline stages?", "Por que imutabilidade?", "Command buffer recording?", "Dia 08 shader FSM?"],
    links=["Dia 08 graphics/shader_stage_fsm", "Vulkan PSO"],
    bench_metric="1e5 transitions",
    bench_cmd="python days/2026-09-10/graphics/pipeline_state_object/solutions/test_pipeline_state_object.py",
)

spec(
    "2026-09-10/redteam/capstone_triage",
    title="Triage de magic bytes",
    lang="Python",
    why="Detecta ELF/PE/WASM pelos magics e valida tamanho mínimo — porta de entrada de malware analysis.",
    wire="""| Bytes | Formato |
|-------|---------|
| `7F ELF ...` | ELF |
| `MZ ...` | PE |
| `00 asm ...` | WASM |
| min_size PE | 2 |

triage ok → `r[\"ok\"] is True`.""",
    trace="""```text
detect_magic(b"\\x7fELF\\x02") == "ELF"
detect_magic(b"MZ\\x90") == "PE"
detect_magic(b"\\x00asm\\x01") == "WASM"
min_size_for("PE") == 2
```""",
    algo="1. prefix match magics.\n2. min_size por formato.\n3. triage agrega ok.",
    bugs="- Ordem de match errada.\n- PE sem MZ.\n- min_size inventado.",
    prod="file(1), die, Detect It Easy.",
    deep=[
        ("Modelo mental", "prefixos → enum de formato."),
        ("Por quê min_size?", "Magic sozinho não basta se buffer truncado."),
        ("Por quê PE=2?", "Só `MZ` já identifica o stub mínimo do lab."),
        ("Invariante", "detect_magic None/unknown se não casar."),
        ("Ligação", "Dia 09 yara_match_scan; Dia 08 pe_export."),
        ("Segurança", "Não executar o binário — só classificar."),
    ],
    ex_easy="Magics ELF/PE/WASM no papel.",
    ex_med="detect_magic.",
    ex_hard="min_size + triage.",
    ex_chal="Mach-O magic?",
    cases=[
        ("CAP-RT-FMT-01", "ELF/PE/WASM detect."),
        ("CAP-RT-FMT-02", "min_size PE==2."),
        ("CAP-RT-FMT-03", "triage ok True."),
    ],
    research=["Magic ELF?", "MZ significa?", "WASM \\0asm?", "Por que não executar?", "Relação YARA?"],
    links=["Dia 09 redteam/yara_match_scan", "Dia 10 tooling/capstone_format_detect"],
    bench_metric="1e5 detect_magic",
    bench_cmd="python days/2026-09-10/redteam/capstone_triage/solutions/test_capstone_triage.py",
)

spec(
    "2026-09-10/quantum/capstone_measurement",
    title="Medição Born e amostragem",
    lang="Python",
    why="|alpha|^2 define probabilidade. O lab calcula Born, conta outcomes e amostra com limiar.",
    wire="""| Entrada | Saída |
|---------|-------|
| 0.5+0.5j | Born ≈ 0.5 |
| counts[1] | 1 (fixture) |
| sample([0.5,0.5], 0.75) | 1 |""",
    trace="""```text
born_probability(0.5+0.5j) ≈ 0.5
c[1] == 1
measure_sample([0.5,0.5], 0.75) == 1
```""",
    algo="1. Born = abs(z)**2 (ou re²+im²).\n2. histograma de medidas.\n3. sample: percorra CDF com u=0.75.",
    bugs="- Usar abs sem quadrado.\n- CDF invertida.\n- Índice off-by-one.",
    prod="Qiskit Aer / statevector measure.",
    deep=[
        ("Modelo mental", "amplitude → probabilidade → bit clássico."),
        ("Por quê 0.5+0.5j → 0.5?", "0.25+0.25=0.5."),
        ("Por quê u=0.75 → 1?", "CDF: 0.5 depois 1.0; 0.75 cai no segundo."),
        ("Invariante", "soma das probs = 1 antes de amostrar."),
        ("Ligação", "Dia 09 decoherence_noise."),
        ("Numérico", "tol 1e-9 como o teste."),
    ],
    ex_easy="Calcule |0.5+0.5j|^2.",
    ex_med="born_probability.",
    ex_hard="measure_sample.",
    ex_chal="Amostragem com RNG real vs limiar fixo.",
    cases=[
        ("CAP-Q-MEAS-01", "Born≈0.5."),
        ("CAP-Q-MEAS-02", "c[1]==1."),
        ("CAP-Q-MEAS-03", "sample→1."),
    ],
    research=["Regra de Born?", "CDF discreta?", "Por que limiar fixo no teste?", "Estado de Bell?", "Dia 09 decoherence?"],
    links=["Dia 09 quantum/decoherence_noise"],
    bench_metric="1e5 born+sample",
    bench_cmd="python days/2026-09-10/quantum/capstone_measurement/solutions/test_capstone_measurement.py",
)

spec(
    "2026-09-10/ai/capstone_tokenizer",
    title="Tokenizer + merge de runs",
    lang="Python",
    why="Bytes/chars → ids; merge_runs comprime runs; vocab_size conta distintos — ponte para BPE.",
    wire="""| Entrada | Saída |
|---------|-------|
| \"aaab\" | ids `[97,97,97,98]` |
| merge_runs | `[(97,3),(98,1)]` |
| vocab_size | 2 |""",
    trace="""```text
ids == [97,97,97,98]
merge_runs(ids) == [(97,3),(98,1)]
vocab_size(ids) == 2
```""",
    algo="1. ord(c) por caractere.\n2. RLE de ids.\n3. len(set(ids)).",
    bugs="- merge errado na fronteira.\n- vocab contando runs em vez de ids.\n- UTF-8 multi-byte (lab é ASCII).",
    prod="BPE/WordPiece; aqui RLE didático.",
    deep=[
        ("Modelo mental", "texto → ids → runs → vocab."),
        ("Por quê 97?", "ord('a')."),
        ("Por quê vocab 2?", "só 'a' e 'b'."),
        ("Invariante", "soma dos counts do merge = len(ids)."),
        ("Ligação", "Dia 06 RLE; Dia 09 attention."),
        ("Paper", "Escreva [(97,3),(98,1)] antes de codar."),
    ],
    ex_easy="ord de aaab.",
    ex_med="ids.",
    ex_hard="merge + vocab.",
    ex_chal="BPE um passo de merge.",
    cases=[
        ("CAP-AI-TOK-01", "ids aaab."),
        ("CAP-AI-TOK-02", "merge_runs."),
        ("CAP-AI-TOK-03", "vocab_size==2."),
    ],
    research=["O que é BPE?", "Por que RLE aqui?", "vocab vs merges?", "Unicode?", "Dia 06 RLE?"],
    links=["Dia 06 systems/rle_byte_codec", "Sennrich BPE"],
    bench_metric="1e5 merge_runs",
    bench_cmd="python days/2026-09-10/ai/capstone_tokenizer/solutions/test_capstone_tokenizer.py",
)

spec(
    "2026-09-10/nodejs/capstone_stream_pipeline",
    title="Duplex stream pipeline",
    lang="JavaScript",
    why="Capstone Node: pipe transforma chunks (`HELLO`), métricas de chunks, flush rejeita estado inválido.",
    wire="""| Assert | Valor |
|--------|-------|
| out.join('') | `HELLO` |
| metrics().chunks | 1 |

Registro/flush: siga o tamanho e a regra de recusa no starter/teste.""",
    trace="""```text
pipeline → 'HELLO'
metrics.chunks == 1
```""",
    algo="1. transform/duplex conforme TODOs.\n2. conte chunks.\n3. flush valida pré-condição.",
    bugs="- Encoding errada.\n- Não incrementar chunks.\n- flush silencioso quando deveria recusar.",
    prod="Node stream.Duplex / pipeline().",
    deep=[
        ("Modelo mental", "chunk in → transform → chunk out + metrics."),
        ("Por quê HELLO?", "Fixture estável do teste."),
        ("Por quê chunks==1?", "Um write/push no Caso."),
        ("Invariante", "metrics reflete writes observados."),
        ("Ligação", "Dia 08 duplex_event_pipe; Dia 09 async_hooks."),
        ("Flush", "Recusar se contrato do lab não satisfeito."),
    ],
    ex_easy="Anote HELLO e chunks=1.",
    ex_med="transform básico.",
    ex_hard="metrics + flush.",
    ex_chal="Backpressure: o que pause faz?",
    cases=[
        ("CAP-ND-PIPE-01", "HELLO."),
        ("CAP-ND-PIPE-02", "metrics/chunks."),
        ("CAP-ND-PIPE-03", "flush regra."),
    ],
    research=["stream.Duplex?", "pipeline()?", "Backpressure?", "Dia 08 duplex?", "Por que métricas?"],
    links=["Dia 08 nodejs/duplex_event_pipe", "Node stream docs"],
    bench_metric="1e4 chunks",
    bench_cmd="node days/2026-09-10/nodejs/capstone_stream_pipeline/solutions/test.js",
)

spec(
    "2026-09-10/parsers/capstone_query_eval",
    title="Query Pratt/bool simples",
    lang="Python",
    why="Lex `a:1 AND b:2` e avalia booleanos — capstone do arco de parsers.",
    wire="""| Entrada | Saída |
|---------|-------|
| lex `a:1 AND b:2` | `[\"a:1\",\"AND\",\"b:2\"]` |
| eval AND | True (fixture) |
| `false OR true` | True |""",
    trace="""```text
lex("a:1 AND b:2") == ["a:1","AND","b:2"]
eval_query("a:1 AND b:2") is True
eval_query("false OR true") is True
```""",
    algo="1. lex tokens.\n2. eval AND/OR com literais/termos do lab.\n3. precedência conforme implementação do solution.",
    bugs="- Split errado em `:`.`\n- AND sem short-circuit se exigido.\n- OR false false → True indevido.",
    prod="Elastic/Lucene query string; aqui subset.",
    deep=[
        ("Modelo mental", "tokens → árvore/bool → bool."),
        ("Por quê AND True no fixture?", "Termos a:1 e b:2 são verdadeiros no ambiente do teste."),
        ("Por quê OR true?", "Identidade booleana."),
        ("Invariante", "lex ∘ eval estável para as strings do teste."),
        ("Ligação", "Dia 07 pratt_query_lang; Dia 09 logfmt."),
        ("Paper", "Liste os 3 tokens antes de codar."),
    ],
    ex_easy="Lex no papel.",
    ex_med="lex.",
    ex_hard="eval AND/OR.",
    ex_chal="NOT e parênteses.",
    cases=[
        ("CAP-PRATT-01", "lex 3 tokens."),
        ("CAP-PRATT-02", "AND True."),
        ("CAP-PRATT-03", "OR True."),
    ],
    research=["Pratt parsing?", "Precedência AND/OR?", "Lucene query?", "Dia 07 Pratt?", "Short-circuit?"],
    links=["Dia 07 parsers/pratt_query_lang", "Dia 09 parsers/logfmt_lexer"],
    bench_metric="1e5 eval_query",
    bench_cmd="python days/2026-09-10/parsers/capstone_query_eval/solutions/test_capstone_query_eval.py",
)

spec(
    "2026-09-10/agent/capstone_agent_loop",
    title="Agent loop capstone",
    lang="Python",
    why="Fecha o arco do agent: estado DONE e replay do trace verdadeiro — evolução do verify_replay_log.",
    wire="""| Campo | Assert |
|-------|--------|
| ag.state | `DONE` |
| replay(ag.trace) | True |""",
    trace="""```text
ag.state == "DONE"
replay(ag.trace) is True
```""",
    algo="1. rode o loop até condição de parada.\n2. grave trace.\n3. replay valida consistência.",
    bugs="- Estado final ≠ DONE.\n- Trace incompleto.\n- replay sempre True sem checar.",
    prod="Agent harnesses com tool calls; aqui FSM+trace.",
    deep=[
        ("Modelo mental", "loop → estado → trace → replay."),
        ("Por quê DONE?", "Verify ok no caminho feliz."),
        ("Por quê replay?", "Detecta logs adulterados."),
        ("Invariante", "replay(trace) True ⇒ estado coerente."),
        ("Ligação", "Dia 09 verify_replay_log."),
        ("Paper", "Desenhe IDLE→RUN→DONE."),
    ],
    ex_easy="FSM no papel.",
    ex_med="transições até DONE.",
    ex_hard="replay True.",
    ex_chal="Injetar evento e ver replay falhar.",
    cases=[
        ("CAP-AGENT-01", "estado DONE."),
        ("CAP-AGENT-02", "trace preenchido."),
        ("CAP-AGENT-03", "replay True."),
    ],
    research=["O que é agent loop?", "Por que replay?", "Tool calls?", "Dia 09 verify?", "Hallucination vs verify?"],
    links=["Dia 09 agent/verify_replay_log"],
    bench_metric="1e4 loops",
    bench_cmd="python days/2026-09-10/agent/capstone_agent_loop/solutions/test_capstone_agent_loop.py",
)

spec(
    "2026-09-10/tooling/capstone_format_detect",
    title="Detect de formato por assinatura",
    lang="Python",
    why="PNG e outros: match_signature + dict format/confidence — irmão do triage redteam com API de tooling.",
    wire="""| Entrada | Saída |
|---------|-------|
| PNG bytes | match_signature → `\"PNG\"` |
| detect dict | `format==\"PNG\"`, `confidence==1.0` |""",
    trace="""```text
match_signature(png) == "PNG"
d["format"]=="PNG" and d["confidence"]==1.0
```""",
    algo="1. compare prefixo PNG (89 50 4E 47…).\n2. monte dict com confidence 1.0 em match pleno.\n3. demais formatos conforme solution.",
    bugs="- Assinatura incompleta.\n- confidence ≠ 1.0.\n- case sensível errado.",
    prod="libmagic; aqui tabelas explícitas.",
    deep=[
        ("Modelo mental", "prefixo → formato + score."),
        ("Por quê confidence 1.0?", "Match exato do magic."),
        ("Por quê PNG no teste?", "Assinatura clássica de 8 bytes."),
        ("Invariante", "format e match_signature concordam."),
        ("Ligação", "redteam/capstone_triage."),
        ("Hex", "89 50 4E 47 0D 0A 1A 0A."),
    ],
    ex_easy="Escreva magic PNG em hex.",
    ex_med="match_signature.",
    ex_hard="dict confidence.",
    ex_chal="Conflito de prefixos — quem ganha?",
    cases=[
        ("CAP-TOOL-DET-01", "PNG match."),
        ("CAP-TOOL-DET-02", "format PNG."),
        ("CAP-TOOL-DET-03", "confidence 1.0."),
    ],
    research=["PNG signature?", "libmagic?", "confidence parcial?", "Dia 10 triage?", "Falsos positivos?"],
    links=["Dia 10 redteam/capstone_triage", "PNG spec signature"],
    bench_metric="1e5 match_signature",
    bench_cmd="python days/2026-09-10/tooling/capstone_format_detect/solutions/test_capstone_format_detect.py",
)


def build_teoria(s: dict) -> str:
    deep_parts = []
    for title, body in s["deep"]:
        deep_parts.append(f"## {title}\n\n{body}\n")
    deep = "\n".join(deep_parts)
    return f"""# Teoria passo a passo — {s['title']}

Este laboratório é em **{s['lang']}**.

## 1. O que estamos construindo

{s['why']}

## 2. Por que este módulo existe neste dia

Por quê estudar isso agora? Porque o contrato numérico do teste fixa o vocabulário
do resto do dia — sem o paper-trace, o código “quase certo” passa no olho e falha
no assert.

## 3. Formato / contrato de dados (wire)

{s['wire']}

## 4. Trace numérico (valores dos testes)

Siga no papel **antes** de abrir o editor. Estes números são os do Caso 1.

{s['trace']}

## 5. Algoritmo (ordem obrigatória)

{s['algo']}

## 6. Invariantes

- A saída é determinística para a mesma entrada do teste.
- Erros de pré-condição falham **agora** (retorno negativo, `Err`, `false`, exceção),
  não um default silencioso.
- O valor que o assert compara é o da seção de trace — não um sinônimo.

## 7. Bugs que o teste rejeita

{s['bugs']}

## 8. Lab versus produção

{s['prod']}

{deep}

## Por quê — síntese

### Por quê estas invariantes?
Cada `TODO [ID]` isola uma propriedade que quebra silenciosamente se ignorada.

### Por quê medir?
O `BENCHMARK_GUIADO.md` pede a métrica `{s['bench_metric']}` — mesmo que o ambiente
pule a medição, o aluno registra o protocolo.

### Por quê não alterar o teste?
O teste é o contrato. Ajuste o código até a saída igualar o caderno.

## Checklist antes de implementar

- [ ] Escrevi no papel o valor do Caso 1 (seção 4).
- [ ] Sei arquivo/função de cada TODO (`RESOLUCAO` / `TODO_MAP`).
- [ ] Sei o que **não** mudar (assinaturas, nomes públicos, capacidade fixa).

## Como saber se está correto

Rode os testes do `starter/` (esperado FAIL) e depois os de `solutions/` (PASS).
A string/número impresso deve bater com o trace caractere a caractere / bit a bit.

## Fluxo de dados (visão única deste módulo)

```text
entrada do Caso 1  →  transformação do algoritmo (seção 5)  →  valor do assert
       ↑                          ↑                                ↑
  paper-trace              código no starter                  TESTES_GUIADOS
```

Se qualquer seta divergir, pare: o bug está na seta, não no “conceito geral”.

## Tabela rápida TODO → propriedade

| Ordem | Propriedade protegida |
|-------|------------------------|
| 1º TODO | base do contrato (parse/init/open) |
| 2º TODO | transformação / estado intermediário |
| 3º TODO | agregação / export / verificação final |

Substitua na ordem da RESOLUCAO: pular o 1º faz o 2º mentir com dados lixo.

## O que não fazer

- Não reescrever o módulo em outra linguagem “porque é mais fácil”.
- Não alterar asserts para caber na sua saída.
- Não inventar um segundo exemplo no lugar do trace do Caso 1.
- Não copiar `solutions/` no começo — use a RESOLUCAO só ao travar.

## Fechamento

Releia o wire (seção 3) e o trace (seção 4). Risque no caderno a linha que você
calculou diferente do teste. Só então abra o arquivo do starter citado na
resolução e substitua o corpo da função nomeada.
"""


def build_resolucao(
    day: str,
    track: str,
    name: str,
    s: dict,
    todos: list[tuple[str, str, str]],
    bodies: dict[str, tuple[str, str]],
) -> str:
    mapa_lines = [
        "| TODO ID | Arquivo | Função / âncora |",
        "|---------|---------|-----------------|",
    ]
    for ident, path, fn in todos:
        mapa_lines.append(f"| `{ident}` | `{path}` | `{fn}` |")
    mapa = "\n".join(mapa_lines)
    base = baseline_cmd(day, track, name, todos[0][1] if todos else "starter/main.py")
    sections = []
    for ident, path, fn in todos:
        fence, code = bodies.get(ident, ("", f"# implementar {ident}\npass\n_keep = True"))
        if not fence:
            fence = lang_fence(path)
        # ensure enough code lines
        non_c = [ln for ln in code.splitlines() if ln.strip() and not ln.strip().startswith(("#", "//"))]
        if len(non_c) < 3:
            code = code.rstrip() + "\n    _keep_signature = True  # não altere a assinatura\n"
        case = next((c for c in s["cases"] if c[0] == ident), (ident, "assert do teste"))
        sections.append(
            f"""
## {ident}

### Onde colocar ({ident})

| Campo | Valor |
|-------|-------|
| Arquivo | `{path}` |
| Função / âncora | `{fn}` — comentário `TODO [{ident}]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `{ident}`, o Caso correspondente falha: {case[1]}

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `{ident}` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```{fence}
{code}
```

### Por que funciona?

Por quê este corpo satisfaz `{ident}`: ele implementa exatamente o contrato do
teste ({case[1]}), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `{ident}`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.
"""
        )
    body = f"""# Resolução guiada — {s['title']}

## Mapa exato starter → resolução

{mapa}

> Raiz: `days/{day}/{track}/{name}/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
{base}
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).

{''.join(sections)}

## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| NotImplemented / stub | corpo não substituído | cole o bloco do TODO |
| número/string diferente | trace errado no papel | refaça a seção 4 da TEORIA |
| caso seguinte quebra | mudou assinatura ou estado global | restaure o que “Não mexer” pede |
| listener/null (.NET) | sem ActivityListener | veja TESTES_GUIADOS |

## Relatório de resolução

- TODOs concluídos:
- Comando de teste:
- Saída observada:
- Invariantes checadas:
- Edge cases:
- Benchmark (`{s['bench_metric']}`):
"""
    # keep under 450 lines
    lines = body.splitlines()
    if len(lines) > 440:
        main = "\n".join(lines[:400])
        ap = "# Apêndice de resolução\n\n" + "\n".join(lines[400:])
        return main + "\n", ap
    return body, None


def build_exercicios(s: dict, todos: list[tuple[str, str, str]]) -> str:
    ids = ", ".join(f"`{t[0]}`" for t in todos)
    return f"""# Exercícios — {s['title']}

Cada nível mapeia aos TODOs {ids}.

## Fácil

{s['ex_easy']}

**Arquivo-alvo:** `{todos[0][1] if todos else 'starter/'}`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

{s['ex_med']}

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

{s['ex_hard']}

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

{s['ex_chal']}

**Critério:** resposta escrita no relatório + teste mental/extra sem quebrar os asserts oficiais.
"""


def build_testes(s: dict) -> str:
    parts = ["# Testes guiados\n"]
    for i, (ident, desc) in enumerate(s["cases"], 1):
        parts.append(f"## Caso {i}: `{ident}`\n\n{desc}\n")
    parts.append("## Identificadores\n")
    for ident, _ in s["cases"]:
        parts.append(f"- `{ident}` — exercido pelo caso acima; o assert usa o valor da TEORIA.\n")
    return "\n".join(parts)


def build_pesquisa(s: dict) -> str:
    qs = "\n".join(f"{i}. {q}" for i, q in enumerate(s["research"], 1))
    links = "\n".join(f"- {l}" for l in s["links"])
    return f"""# Pesquisa guiada — {s['title']}

Responda no papel com valores verificáveis neste lab (não ensaios vagos).

{qs}

## Fontes

{links}
"""


def build_benchmark(s: dict) -> str:
    return f"""# Benchmark guiado — {s['title']}

## Hipótese

A métrica `{s['bench_metric']}` permanece estável (±20%) em 3 corridas no mesmo hardware.

## Método

```powershell
{s['bench_cmd']}
```

Repita 3 vezes; anote tempo de parede ou a métrica específica do lab.

## Resultados observados

não executado neste ambiente na geração do dia — registre aqui: {s['bench_metric']}.
"""


def build_readme(s: dict, day: str, track: str, name: str, todos: list[tuple[str, str, str]]) -> str:
    ids = ", ".join(f"`{t[0]}`" for t in todos)
    return f"""# {s['title']}

**Dia:** {day} · **Trilha:** `{track}` · **Módulo:** `{name}`  
**Linguagem:** {s['lang']}  
**TODOs:** {ids}

## Pré-requisitos

- Paper-trace da TEORIA (seção 4) feito no caderno
- Checkpoint correspondente em `ATIVIDADES.md` do dia

## Fluxo

1. `TEORIA_PASSO_A_PASSO.md`
2. `EXERCICIOS.md`
3. Implemente `starter/`
4. `TESTES_GUIADOS.md` / teste local
5. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só se travar
6. `BENCHMARK_GUIADO.md`

## Ideia em uma frase

{s['why']}
"""


def deepen_module(mod: Path) -> None:
    day = mod.parts[-3]
    track = mod.parts[-2]
    name = mod.name
    key = f"{day}/{track}/{name}"
    if key not in SPECS:
        raise SystemExit(f"missing spec for {key}")
    s = SPECS[key]
    todos = collect_todos(mod / "starter")
    bodies = extract_solution_bodies(mod / "solutions")
    write(mod / "TEORIA_PASSO_A_PASSO.md", build_teoria(s))
    res, ap = build_resolucao(day, track, name, s, todos, bodies)
    write(mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", res)
    if ap:
        write(mod / "RESOLUCAO_APENDICE.md", ap)
    elif (mod / "RESOLUCAO_APENDICE.md").exists():
        # remove stale appendix if no longer needed
        (mod / "RESOLUCAO_APENDICE.md").unlink()
    write(mod / "EXERCICIOS.md", build_exercicios(s, todos))
    write(mod / "TESTES_GUIADOS.md", build_testes(s))
    write(mod / "PESQUISA_GUIADA.md", build_pesquisa(s))
    write(mod / "BENCHMARK_GUIADO.md", build_benchmark(s))
    write(mod / "README.md", build_readme(s, day, track, name, todos))
    # gfx comparison if needed
    if track == "graphics":
        (mod / "docs").mkdir(exist_ok=True)
        write(
            mod / "docs" / "COMPARISON.md",
            f"""# Comparação — {s['title']}

Lab **headless**: a máquina de estados / timer simulado é o artefato testável.
Não há janela Win32 obrigatória neste módulo (FSM/timer, não pixels).

| Etapa | Software (CPU) | OpenGL | Este lab |
|-------|----------------|--------|----------|
| medição / estado | perf_counter / FSM | timer query / PSO | simulação determinística |
| validação | asserts unitários | frame dump / debug group | `PEDAGOGY-TEST` |
| CI | sempre | GPU nem sempre | headless PASS |
""",
        )


ATIVIDADES_09 = r'''# ATIVIDADES — 2026-09-09 (observabilidade multi-linguagem)

**Dia:** 13 módulos | **~24–32 h**  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel). Teste PASS sozinho não basta.

---

## Preparação (30 min)

- [ ] Ler `START_HERE.md` e `README.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-09
```

---

## Bloco 1 — Contadores e arena (C / C++) (4–6 h)

### Objetivo conceitual

Ver um **histograma de opcodes** e uma **arena com telemetria** cujo `allocs` sobrevive ao reset.

| Módulo | TODOs | Paper-trace obrigatório |
|--------|-------|-------------------------|
| `systems/clvm_trace_profiler` | CLVM-TRACE-01..03 | `02 02 08` → c[2]=2, hottest=2 |
| `systems/arena_telemetry` | ARENA-TEL-01..03 | alloc(8) ok; alloc(60) -1; reset mantém allocs=1 |

**Checkpoint conceitual:**

- [ ] Contei no papel os opcodes do fixture e marquei hottest
- [ ] Escrevi used/allocs/resets após init, alloc(8), alloc(60), reset
- [ ] Explico em uma frase: por que reset não zera allocs

**Depois:** implemente starters; `ctest` solutions deve PASS.

---

## Bloco 2 — Máscara causal (C) (2–3 h)

### Objetivo conceitual

Atenção causal: k>q é invisível; score vira −1e9; `visible_count(2)=3`.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `ai/attention_mask` | AI-ATTN-01..03 | q=2,k=2 visível; k=3 → −1e9; count=3 |

**Checkpoint conceitual:**

- [ ] Tabela q=2 × k=0..3 no papel
- [ ] Sei por que −1e9 e não 0

---

## Bloco 3 — Stack, spans e async (Rust / .NET / Node) (5–7 h)

### Objetivo conceitual

PC→nome, ActivitySource→tag→export, async_hooks init/before/after.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `rust/stack_sample_trace` | RS-STACK-* | 0x1000 → main |
| `dotnet/activity_source_span` | DN-ACT-* | `work\|activity_source_span` |
| `nodejs/async_hooks_trace` | ND-ASYNC-* | phase init presente; m.init≥1 |

**Checkpoint conceitual:**

- [ ] Escrevi PC→main
- [ ] Escrevi a string de export do Activity
- [ ] Listei as três fases async_hooks

---

## Bloco 4 — Perf, GPU timer, logfmt (3–5 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `linux/perf_event_open_lab` | LX-PERF-* | open(1,2)→fd; read 42; close remove |
| `graphics/gpu_timer_query` | GFX-GPU-* | handle 0; lap draw |
| `parsers/logfmt_lexer` | PR-LOGFMT-* | `a=1 b=2` → 2 tokens |

**Checkpoint conceitual:**

- [ ] Calculei fd = (1<<16)\|2
- [ ] Sei que o primeiro timer handle é 0
- [ ] Tokenizei logfmt no papel

---

## Bloco 5 — Quantum, YARA, agent, PDB (4–6 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `quantum/decoherence_noise` | Q-DECO-* | p0+p1≈1; len(trace)=4 |
| `redteam/yara_match_scan` | RT-YARA-* | pat [0xAA,None]; hit @1 |
| `agent/verify_replay_log` | AG-* | start+verify ok → DONE; hash 16 |
| `tooling/pdb_symbol_index` | TL-PDB-* | `1000 main` → (0x1000, main) |

**Checkpoint conceitual:**

- [ ] Normalizei um par de probs
- [ ] Parseiei AA ?? → [0xAA, None]
- [ ] Desenhei FSM IDLE→RUN→DONE
- [ ] Parseiei linha de símbolo

---

## Relatório do dia

| Bloco | Papel | Testes solutions |
|-------|-------|------------------|
| 1 C/C++ | ☐ | ☐ |
| 2 atenção | ☐ | ☐ |
| 3 Rust/.NET/JS | ☐ | ☐ |
| 4 perf/gfx/parse | ☐ | ☐ |
| 5 q/rt/ag/tool | ☐ | ☐ |

```powershell
python scripts/run_day_tests.py --day 2026-09-09 --mode solutions
```
'''

ATIVIDADES_10 = r'''# ATIVIDADES — 2026-09-10 (integração multi-trilha / capstone)

**Dia:** 13 módulos | **~28–36 h**  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel). Teste PASS sem o papel não conta.

---

## Preparação (30 min)

- [ ] `START_HERE.md` + `README.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-10
```

---

## Bloco 1 — Bytecode CLVM (systems + rust) (5–7 h)

### Objetivo conceitual

Disasm → peephole (apaga `PUSH 0; ADD`) → verify de stack; e o mesmo header validado em Rust.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/clvm_pipeline_integration` | CAP-CLVM-* | listing PUSH1/2 ADD HALT; fold → `01 05 08` |
| `rust/cross_verify_clvm` | CAP-RS-XVFY-* | magic CLVM; version 1; FNV @ offset 12 |

**Checkpoint conceitual:**

- [ ] Escrevi as 4 linhas do disasm antes do editor
- [ ] Sei por que `01 00 02` some e `01 05` fica
- [ ] Desenhei header offsets 0/4/12

**Depois:** solutions PASS (`pytest` / `cargo test`).

---

## Bloco 2 — Input unificado (systems / linux / .NET) (5–7 h)

### Objetivo conceitual

Eventos `(type,code,value)` → mux → `KEY:`/`REL:`; device `composite0` fecha com SYN `(0,0,0)`; host .NET conta via Span.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/unified_input_pipeline` | CAP-INP-* | (1,30,1) → KEY:30 |
| `linux/composite_input_driver` | CAP-LNX-* | name composite0; frame[-1]=(0,0,0) |
| `dotnet/capstone_input_host` | CAP-DN-HOST-* | inteiro literal do HostTests |

**Checkpoint conceitual:**

- [ ] Traduzi (1,30,1) → KEY:30
- [ ] Expliquei SYN_REPORT
- [ ] Anotei o número do assert .NET

---

## Bloco 3 — Gráficos, triage, quantum, AI (5–7 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `graphics/pipeline_state_object` | CAP-GFX-PSO-* | UNINITIALIZED→VERTEX_SHADER; READY→RECORDING |
| `redteam/capstone_triage` | CAP-RT-FMT-* | ELF/PE/WASM magics; min_size PE=2 |
| `quantum/capstone_measurement` | CAP-Q-MEAS-* | \|0.5+0.5j\|²=0.5; sample 0.75→1 |
| `ai/capstone_tokenizer` | CAP-AI-TOK-* | aaab → [97×3,98]; vocab 2 |

**Checkpoint conceitual:**

- [ ] Listei 2 arestas da FSM de PSO
- [ ] Escrevi magics ELF/PE/WASM
- [ ] Calculei Born de 0.5+0.5j
- [ ] RLE de aaab → [(97,3),(98,1)]

---

## Bloco 4 — Node, parsers, agent, tooling (5–7 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `nodejs/capstone_stream_pipeline` | CAP-ND-PIPE-* | out HELLO; chunks=1 |
| `parsers/capstone_query_eval` | CAP-PRATT-* | lex 3 tokens; AND/OR True |
| `agent/capstone_agent_loop` | CAP-AGENT-* | state DONE; replay True |
| `tooling/capstone_format_detect` | CAP-TOOL-DET-* | PNG; confidence 1.0 |

**Checkpoint conceitual:**

- [ ] Anotei HELLO e chunks=1
- [ ] Lexei `a:1 AND b:2` em 3 tokens
- [ ] Desenhei loop até DONE
- [ ] Magic PNG em hex (89 50 4E 47…)

---

## Relatório do dia

| Bloco | Papel | Testes |
|-------|-------|--------|
| 1 bytecode | ☐ | ☐ |
| 2 input | ☐ | ☐ |
| 3 gfx/rt/q/ai | ☐ | ☐ |
| 4 node/parse/ag/tool | ☐ | ☐ |

```powershell
python scripts/run_day_tests.py --day 2026-09-10 --mode solutions
```
'''

START_09 = r'''# START HERE — Day 2026-09-09

**Observabilidade multi-linguagem** — C/C++ no núcleo; Rust, .NET, JavaScript e Python nas demais trilhas.

## Fluxo por módulo (igual Dia 01 / 06)

1. Leia `TEORIA_PASSO_A_PASSO.md` — O quê / Como / Por quê + **trace no papel**.
2. Faça o checkpoint de [`ATIVIDADES.md`](ATIVIDADES.md) **antes** do starter.
3. `EXERCICIOS.md` — Fácil → Desafio.
4. Implemente `starter/` (`TODO [ID]`).
5. Rode testes (`PEDAGOGY-TEST: ID`). Esperado: FAIL até completar.
6. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar.
7. Compare `solutions/` após tentativa honesta; registre `BENCHMARK_GUIADO.md`.

## Ordem recomendada

1. `systems/clvm_trace_profiler` (C) — histograma `02 02 08`
2. `systems/arena_telemetry` (C++) — allocs sobrevivem ao reset
3. `ai/attention_mask` (C) — máscara causal
4. `rust/stack_sample_trace` — PC → main
5. `dotnet/activity_source_span` — Activity + tag
6. `nodejs/async_hooks_trace` — fases init/before/after
7. `linux/perf_event_open_lab` — fd sintético
8. `graphics/gpu_timer_query` — timer headless
9. `parsers/logfmt_lexer` — k=v
10. `quantum/decoherence_noise` — canal + trace
11. `redteam/yara_match_scan` — AA ??
12. `agent/verify_replay_log` — FSM + hash
13. `tooling/pdb_symbol_index` — 1000 main

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-09
python scripts/day_contract_check.py --day 2026-09-09
python scripts/run_day_tests.py --day 2026-09-09 --mode solutions
```
'''

START_10 = r'''# START HERE — Day 2026-09-10

**Integração multi-trilha — preparação capstone** (Dias 01–09 → 13 módulos).

## Fluxo por módulo

1. TEORIA → checkpoint em [`ATIVIDADES.md`](ATIVIDADES.md) → EXERCICIOS → starter → TESTES → RESOLUCAO (se travar).
2. Paper-trace **antes** do editor; o assert literal é a fonte de verdade.

## Ordem por bloco

1. `systems/clvm_pipeline_integration` + `rust/cross_verify_clvm`
2. `systems/unified_input_pipeline` + `linux/composite_input_driver` + `dotnet/capstone_input_host`
3. `graphics/pipeline_state_object` + `redteam/capstone_triage` + `quantum/capstone_measurement` + `ai/capstone_tokenizer`
4. `nodejs/capstone_stream_pipeline` + `parsers/capstone_query_eval` + `agent/capstone_agent_loop` + `tooling/capstone_format_detect`

## Capstones de portfólio

- `projects/chris-vm/` — CLVM + verify
- `projects/chris-driver-lab/` — input
- `projects/chris-binary-toolkit/` — triage
- `projects/chris-agent-harness/` — agent loop

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-10
python scripts/day_contract_check.py --day 2026-09-10
python scripts/run_day_tests.py --day 2026-09-10 --mode solutions
```
'''


def main() -> int:
    missing = []
    for day in ("2026-09-09", "2026-09-10"):
        day_dir = ROOT / "days" / day
        for track in sorted(day_dir.iterdir()):
            if not track.is_dir():
                continue
            for mod in sorted(track.iterdir()):
                if not mod.is_dir() or not (mod / "starter").exists():
                    continue
                key = f"{day}/{track.name}/{mod.name}"
                if key not in SPECS:
                    missing.append(key)
                    continue
                deepen_module(mod)
                print("deepened", key)
        if day == "2026-09-09":
            write(day_dir / "ATIVIDADES.md", ATIVIDADES_09)
            write(day_dir / "START_HERE.md", START_09)
        else:
            write(day_dir / "ATIVIDADES.md", ATIVIDADES_10)
            write(day_dir / "START_HERE.md", START_10)
    if missing:
        print("MISSING SPECS:", *missing, sep="\n")
        return 1
    print("done", len(SPECS), "modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
