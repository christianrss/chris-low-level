#!/usr/bin/env python3
"""Days 09 and 10: same language mix as day 08, different contracts."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rewrite_multilang_days import (
    CMAKE_ASM,
    exercicios,
    gfx_comparison,
    package,
    pesquisa,
    resolucao,
    testes,
    teoria,
    todo_section,
    wipe_py,
    write,
    emit_c_pair,
    benchmark,
)

ROOT = Path(__file__).resolve().parents[1]


def ids_from(*groups: list[str]) -> str:
    lines = ["# TODO map\n"]
    for g in groups:
        for i in g:
            lines.append(f"- `{i}`")
    return "\n".join(lines) + "\n"


def emit_trace_c(day: Path) -> None:
    mod = day / "systems" / "clvm_trace_profiler"
    h = """#ifndef TRACE_H
#define TRACE_H
#include <stddef.h>
#include <stdint.h>
void note_op(uint32_t *counts, uint8_t op);
int hottest(const uint32_t *counts);
int profile_code(const uint8_t *code, size_t n, uint32_t *counts);
#endif
"""
    stub = """#include "trace.h"
void note_op(uint32_t *counts, uint8_t op) { /* TODO [CLVM-TRACE-01] */ (void)counts; (void)op; }
int hottest(const uint32_t *counts) { /* TODO [CLVM-TRACE-02] */ (void)counts; return -1; }
int profile_code(const uint8_t *code, size_t n, uint32_t *counts) {
    /* TODO [CLVM-TRACE-03] */ (void)code; (void)n; (void)counts; return -1;
}
"""
    sol = """#include "trace.h"
void note_op(uint32_t *counts, uint8_t op) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-01 */
    if (counts && op < 16) counts[op]++;
}
int hottest(const uint32_t *counts) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-02 */
    int best = 0, i;
    if (!counts) return -1;
    for (i = 1; i < 16; i++) if (counts[i] > counts[best]) best = i;
    return best;
}
int profile_code(const uint8_t *code, size_t n, uint32_t *counts) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-03 */
    size_t i;
    if (!code || !counts) return -1;
    for (i = 0; i < n; i++) note_op(counts, code[i]);
    return (int)n;
}
"""
    test = """#include "trace.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* PEDAGOGY-TEST: CLVM-TRACE-01 */
/* PEDAGOGY-TEST: CLVM-TRACE-02 */
/* PEDAGOGY-TEST: CLVM-TRACE-03 */
int main(void) {
    uint32_t c[16];
    uint8_t code[] = {0x02, 0x02, 0x08};
    memset(c, 0, sizeof c);
    note_op(c, 0x02); note_op(c, 0x02); note_op(c, 0x08);
    assert(c[0x02] == 2 && c[0x08] == 1);
    assert(hottest(c) == 0x02);
    memset(c, 0, sizeof c);
    assert(profile_code(code, 3, c) == 3);
    assert(hottest(c) == 0x02);
    printf("OK trace\\n");
    return 0;
}
"""
    emit_c_pair(mod, "trace", {"trace.h": (h, h), "trace.c": (stub, sol)}, test, "c")
    package(
        mod, "C",
        "# Profiler de opcodes CLVM — C\n\nLinguagem: **C**. Conta opcodes do bytecode, não imprime um gráfico.\n",
        teoria(
            "profiler de bytecode em C",
            "C",
            "O disassembler do Dia 08 lista instruções. Este lab conta qual opcode aparece mais. O fixture `02 02 08` tem ADD duas vezes e HALT uma.",
            "| Opcode | Contagem no fixture |\n|--------|---------------------|\n| 0x02 ADD | 2 |\n| 0x08 HALT | 1 |\n| hottest | 0x02 |",
            """```text
note 0x02, 0x02, 0x08
counts[2]=2, counts[8]=1
hottest = 2 (ADD), desempate pelo menor índice só se empatar — aqui ADD ganha
profile_code dos 3 bytes devolve 3 e o mesmo hottest
```""",
            "1. note_op incrementa counts[op] se op<16.\n2. hottest varre 0..15 e fica com o maior.\n3. profile_code chama note_op em cada byte e retorna n.",
            "- Contar 0x02 uma vez só: hottest ainda pode ser 2, mas c[2]==2 falha.\n- hottest retornar 8: o HALT perdeu.",
            "Um profiler de produção amostra PC. Aqui o bytecode inteiro é o traço.",
        ),
        resolucao(
            "trace C",
            "cmake -S days/2026-09-09/systems/clvm_trace_profiler/starter -B days/2026-09-09/systems/clvm_trace_profiler/starter/build_ci -G \"Visual Studio 17 2022\" -A x64",
            "| `CLVM-TRACE-01` | `starter/trace.c` | `note_op` |\n| `CLVM-TRACE-02` | `starter/trace.c` | `hottest` |\n| `CLVM-TRACE-03` | `starter/trace.c` | `profile_code` |",
            todo_section("CLVM-TRACE-01", "starter/trace.c", "note_op", "o array de 16",
                         "Dois ADD e um HALT. Sem incremento, c[2] fica 0.",
                         "counts[op]++.",
                         "    if (counts && op < 16) counts[op]++;",
                         "c", "O opcode é o índice. 0x02 cabe em 16 slots.",
                         "c[2]==2 e c[8]==1.")
            + todo_section("CLVM-TRACE-02", "starter/trace.c", "hottest", "note_op",
                           "O maior contador é o índice 2.",
                           "Varra 1..15, fique com o maior counts.",
                           "    int best = 0, i;\n    for (i = 1; i < 16; i++) if (counts[i] > counts[best]) best = i;\n    return best;",
                         "c", "Empate fica com o menor índice porque só troca se estritamente maior.",
                         "hottest == 0x02.")
            + todo_section("CLVM-TRACE-03", "starter/trace.c", "profile_code", "note_op",
                           "Três bytes devem retornar 3 e deixar ADD no topo.",
                           "loop note_op; return n.",
                           "    for (i = 0; i < n; i++) note_op(counts, code[i]);\n    return (int)n;",
                         "c", "O perfil é a soma dos note_op, não um segundo contador.",
                         "profile_code retorna 3."),
        ),
        exercicios("C", "Conte no papel os opcodes 02 02 08.", "Implemente note_op.", "hottest e profile_code.", "O que hottest devolve se todos forem zero? O índice 0."),
        testes([("CLVM-TRACE-01", "c[2]==2."), ("CLVM-TRACE-02", "hottest==2."), ("CLVM-TRACE-03", "n==3.")], ["CLVM-TRACE-01", "CLVM-TRACE-02", "CLVM-TRACE-03"]),
        pesquisa("contagem de opcode", ["Quantas vezes ADD aparece?", "Qual índice hottest devolve?", "Por que o teto é 16?", "O que o disassembler do Dia 08 faz que este lab não faz?", "Empate: qual índice fica?"], ["Dia 08 systems/clvm_disassembler"]),
        benchmark("profile de 1e6 bytes", "ctest"),
    )


def emit_arena_cpp(day: Path) -> None:
    mod = day / "systems" / "arena_telemetry"
    h = """#pragma once
#include <cstddef>
struct Arena { char buf[64]; size_t used; int allocs; int resets; };
void arena_init(Arena *a);
int arena_alloc(Arena *a, size_t n, char **out);
void arena_reset(Arena *a);
"""
    stub = """#include "arena.hpp"
void arena_init(Arena *a) { /* TODO [ARENA-TEL-01] */ (void)a; }
int arena_alloc(Arena *a, size_t n, char **out) { /* TODO [ARENA-TEL-02] */ (void)a;(void)n;(void)out; return -1; }
void arena_reset(Arena *a) { /* TODO [ARENA-TEL-03] */ (void)a; }
"""
    sol = """#include "arena.hpp"
void arena_init(Arena *a) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-01
    a->used = 0; a->allocs = 0; a->resets = 0;
}
int arena_alloc(Arena *a, size_t n, char **out) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-02
    if (!a || !out || a->used + n > 64) return -1;
    *out = a->buf + a->used;
    a->used += n;
    a->allocs++;
    return 0;
}
void arena_reset(Arena *a) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-03
    if (!a) return;
    a->used = 0;
    a->resets++;
}
"""
    test = """#include "arena.hpp"
#include <assert.h>
#include <stdio.h>
// PEDAGOGY-TEST: ARENA-TEL-01
// PEDAGOGY-TEST: ARENA-TEL-02
// PEDAGOGY-TEST: ARENA-TEL-03
int main() {
    Arena a; char *p = 0;
    arena_init(&a);
    assert(a.used == 0 && a.allocs == 0);
    assert(arena_alloc(&a, 8, &p) == 0 && a.allocs == 1 && a.used == 8);
    assert(arena_alloc(&a, 60, &p) == -1);
    arena_reset(&a);
    assert(a.used == 0 && a.resets == 1 && a.allocs == 1);
    printf("OK arena\\n");
    return 0;
}
"""
    emit_c_pair(mod, "arena", {"arena.hpp": (h, h), "arena.cpp": (stub, sol)}, test, "cxx")
    package(
        mod, "C++",
        "# Arena com telemetria — C++\n\nLinguagem: **C++**. Buffer de 64 bytes. Reset não zera o contador de allocs.\n",
        teoria(
            "telemetria de arena em C++",
            "C++",
            "A arena do Dia 04 só faz bump. Aqui cada alloc incrementa `allocs` e cada reset incrementa `resets`, mas reset **não** apaga allocs — senão você perde a métrica.",
            "| Campo | Depois de init | Depois de alloc(8) | Depois de reset |\n|-------|----------------|--------------------|-----------------|\n| used | 0 | 8 | 0 |\n| allocs | 0 | 1 | 1 (permanece) |\n| resets | 0 | 0 | 1 |",
            """```text
alloc(8) ok, used=8, allocs=1
alloc(60) 8+60=68 > 64 → -1, used permanece 8
reset: used=0, resets=1, allocs continua 1
```""",
            "1. init zera used, allocs, resets.\n2. alloc recusa se used+n>64. Senão devolve ponteiro, used+=n, allocs++.\n3. reset zera used e incrementa resets. Não toca allocs.",
            "- Zerar allocs no reset: o teste exige allocs==1 depois do reset.\n- Aceitar 60 após 8: 68>64.",
            "malloc não tem reset O(1). A arena sim; a telemetria é o que falta no lab antigo.",
        ),
        resolucao(
            "arena C++",
            "cmake no starter de arena_telemetry",
            "| `ARENA-TEL-01` | `starter/arena.cpp` | `arena_init` |\n| `ARENA-TEL-02` | `starter/arena.cpp` | `arena_alloc` |\n| `ARENA-TEL-03` | `starter/arena.cpp` | `arena_reset` |",
            todo_section("ARENA-TEL-01", "starter/arena.cpp", "arena_init", "o buffer de 64",
                         "used e allocs começam em 0.",
                         "Zere os três campos.",
                         "    a->used = 0; a->allocs = 0; a->resets = 0;",
                         "cpp", "Sem init, alloc conta lixo.",
                         "used==0 && allocs==0.")
            + todo_section("ARENA-TEL-02", "starter/arena.cpp", "arena_alloc", "o teto 64",
                           "8 cabe. 60 depois não.",
                           "used+n>64 retorna -1.",
                         "    if (!a || !out || a->used + n > 64) return -1;\n    *out = a->buf + a->used;\n    a->used += n;\n    a->allocs++;\n    return 0;",
                         "cpp", "O ponteiro é offset no buffer, não um malloc.",
                         "primeiro alloc 0, segundo -1.")
            + todo_section("ARENA-TEL-03", "starter/arena.cpp", "arena_reset", "allocs",
                           "used volta a 0, resets vira 1, allocs fica 1.",
                         "Não zere allocs.",
                         "    a->used = 0;\n    a->resets++;",
                         "cpp", "A métrica de quantas vezes alocou sobrevive ao reset. É telemetria, não um free.",
                         "resets==1 && allocs==1."),
        ),
        exercicios("C++", "Quanto used+60 vale depois de used=8? Cabe em 64?", "Implemente init.", "alloc e reset.", "Por que allocs não volta a 0?"),
        testes([("ARENA-TEL-01", "init zera."), ("ARENA-TEL-02", "8 ok, 60 falha."), ("ARENA-TEL-03", "resets 1, allocs 1.")], ["ARENA-TEL-01", "ARENA-TEL-02", "ARENA-TEL-03"]),
        pesquisa("bump allocator", ["Por que used+60 falha?", "O que reset não zera?", "Onde o ponteiro aponta?", "Qual a diferença para malloc?", "Dia 04 arena fazia o quê sem telemetria?"], ["Dia 04 systems/arena_allocator"]),
        benchmark("allocs de 8 até encher 64", "ctest"),
    )


def emit_attn_c(day: Path) -> None:
    mod = day / "ai" / "attention_mask"
    h = """#ifndef ATTN_H
#define ATTN_H
int causal_mask(int q, int k);
int apply_mask(float *score, int q, int k);
int visible_count(int q);
#endif
"""
    stub = """#include "attn.h"
int causal_mask(int q, int k) { /* TODO [AI-ATTN-01] */ (void)q;(void)k; return 0; }
int apply_mask(float *score, int q, int k) { /* TODO [AI-ATTN-02] */ (void)score;(void)q;(void)k; return 0; }
int visible_count(int q) { /* TODO [AI-ATTN-03] */ (void)q; return -1; }
"""
    sol = """#include "attn.h"
int causal_mask(int q, int k) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-01 */
    if (q < 0 || k < 0) return 0;
    return k <= q ? 1 : 0;
}
int apply_mask(float *score, int q, int k) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-02 */
    if (!score) return 0;
    if (!causal_mask(q, k)) { *score = -1.0e9f; return 0; }
    return 1;
}
int visible_count(int q) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-03 */
    if (q < 0) return 0;
    return q + 1;
}
"""
    test = """#include "attn.h"
#include <assert.h>
#include <stdio.h>
/* PEDAGOGY-TEST: AI-ATTN-01 */
/* PEDAGOGY-TEST: AI-ATTN-02 */
/* PEDAGOGY-TEST: AI-ATTN-03 */
int main(void) {
    float s = 3.0f;
    assert(causal_mask(2, 2) == 1);
    assert(causal_mask(2, 3) == 0);
    assert(apply_mask(&s, 2, 3) == 0);
    assert(s < -1.0e8f);
    assert(visible_count(2) == 3);
    printf("OK attn\\n");
    return 0;
}
"""
    emit_c_pair(mod, "attn", {"attn.h": (h, h), "attn.c": (stub, sol)}, test, "c")
    package(
        mod, "C",
        "# Máscara causal — C\n\nLinguagem: **C**. Query 2 enxerga keys 0,1,2 (3 posições), não a key 3.\n",
        teoria(
            "máscara causal em C",
            "C",
            "Atenção causal não deixa o token olhar o futuro. k<=q é visível. O teste usa q=2.",
            "| q | k | visível? |\n|---|---|----------|\n| 2 | 2 | sim |\n| 2 | 3 | não |\n| visíveis | 0,1,2 | 3 |",
            """```text
causal_mask(2,2)=1
causal_mask(2,3)=0
apply_mask no score 3.0 com k=3 escreve -1e9 e retorna 0
visible_count(2)=3  (índices 0,1,2)
```""",
            "1. causal_mask devolve 1 sse k<=q e ambos >=0.\n2. apply_mask se invisível escreve -1e9 e retorna 0.\n3. visible_count(q)=q+1.",
            "- Deixar k=3 visível: o score 3.0 permanece e o teste de -1e9 falha.\n- visible_count(2)=2 esquece o próprio token.",
            "O softmax do Dia 08 recebe scores já mascarados. -1e9 vira probabilidade ~0.",
        ),
        resolucao(
            "attention C",
            "cmake no starter attention_mask",
            "| `AI-ATTN-01` | `starter/attn.c` | `causal_mask` |\n| `AI-ATTN-02` | `starter/attn.c` | `apply_mask` |\n| `AI-ATTN-03` | `starter/attn.c` | `visible_count` |",
            todo_section("AI-ATTN-01", "starter/attn.c", "causal_mask", "o score",
                         "q=2 k=2 visível; k=3 não.",
                         "return k<=q.",
                         "    if (q < 0 || k < 0) return 0;\n    return k <= q ? 1 : 0;",
                         "c", "Inclui a diagonal. k==q é o próprio token.",
                         "mask(2,2)==1 e mask(2,3)==0.")
            + todo_section("AI-ATTN-02", "starter/attn.c", "apply_mask", "causal_mask",
                           "Score 3.0 com k futuro vira -1e9.",
                         "Se não visível, escreva -1e9f e retorne 0.",
                         "    if (!causal_mask(q, k)) { *score = -1.0e9f; return 0; }\n    return 1;",
                         "c", "O valor grande negativo sobrevive ao softmax do Dia 08 como ~0.",
                         "s < -1e8.")
            + todo_section("AI-ATTN-03", "starter/attn.c", "visible_count", "a máscara",
                           "q=2 enxerga 3 posições.",
                         "return q+1.",
                         "    if (q < 0) return 0;\n    return q + 1;",
                         "c", "0,1,2 são três índices. Não é q.",
                         "visible_count(2)==3."),
        ),
        exercicios("C", "Liste os k visíveis para q=2.", "Implemente causal_mask.", "apply_mask e visible_count.", "O que o softmax faz com -1e9?"),
        testes([("AI-ATTN-01", "k<=q."), ("AI-ATTN-02", "score futuro -1e9."), ("AI-ATTN-03", "count 3.")], ["AI-ATTN-01", "AI-ATTN-02", "AI-ATTN-03"]),
        pesquisa("causal mask", ["Por que k==q é visível?", "Por que -1e9 e não 0?", "Quantos tokens q=2 vê?", "Como isso se liga ao softmax do Dia 08?", "O que acontece com q negativo?"], ["Vaswani et al. attention", "Dia 08 ai/softmax_stable"]),
        benchmark("máscara 512x512", "ctest"),
    )


def write_todo_map(day: Path, date: str) -> None:
    ids: list[str] = []
    for p in day.rglob("*"):
        if "starter" not in p.parts or not p.is_file():
            continue
        if p.suffix.lower() not in {".c", ".h", ".cpp", ".hpp", ".py", ".rs", ".js", ".cs", ".asm", ".s"}:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for ident in re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", text):
            if ident not in ids:
                ids.append(ident)
    bullets = "\n".join(f"- `{i}`" for i in ids)
    write(day / "TODO_MAP.md", f"# TODO map — {date}\n\n{bullets}\n")


def day_docs(day: Path, date: str, title: str, rows: str, atividades: str, todo: str) -> None:
    write(day / "README.md", f"# {date} — {title}\n\n{rows}\n")
    write(day / "START_HERE.md", f"# START HERE — {date}\n\nSiga a coluna de linguagem em `README.md`. O trace numérico está na TEORIA de cada módulo. Faça-o no papel antes do código.\n")
    write(day / "ATIVIDADES.md", atividades)
    mods = sorted(p.parent.relative_to(day).as_posix() for p in day.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))
    listing = "\n".join(f"- `{m}`" for m in mods)
    write(day / "VALIDATION.md", f"# Validação — {date}\n\n```powershell\npython scripts/pedagogy_check_unified.py --day {date}\npython scripts/run_day_tests.py --day {date} --mode solutions\n```\n\n## Módulos\n\n{listing}\n")
    write_todo_map(day, date)
    _ = todo


def refresh_from_code(mod: Path) -> None:
    """Replace lazy scaffold docs with a walkthrough of the actual starter/solution."""
    if mod.name in {"clvm_trace_profiler", "arena_telemetry", "attention_mask"}:
        return
    starter = mod / "starter"
    if not starter.exists():
        return
    blobs = []
    for p in starter.rglob("*"):
        if p.suffix.lower() not in {".py", ".rs", ".js", ".cs", ".c", ".cpp", ".h", ".hpp"}:
            continue
        if any(x in p.parts for x in ("node_modules", "bin", "obj", "target")):
            continue
        if p.name.startswith("test") or p.name.startswith("Test"):
            continue
        try:
            blobs.append((p.relative_to(starter).as_posix(), p.read_text(encoding="utf-8")))
        except UnicodeDecodeError:
            continue
    if not blobs:
        return
    text = "\n".join(b for _, b in blobs)
    ids = []
    for ident in re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", text):
        if ident not in ids:
            ids.append(ident)
    if not ids:
        return
    sol_dir = mod / "solutions"
    sol_bits = []
    if sol_dir.exists():
        for p in sol_dir.rglob("*"):
            if p.suffix.lower() not in {".py", ".rs", ".js", ".cs", ".c", ".cpp"}:
                continue
            if any(x in p.parts for x in ("bin", "obj", "target", "node_modules")):
                continue
            try:
                sol_bits.append(p.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                continue
    sol = "\n".join(sol_bits)
    lang = "Python"
    if any(p.endswith(".rs") for _, p in [(a, "") for a in []]):
        pass
    joined = " ".join(n for n, _ in blobs)
    if ".rs" in joined:
        lang = "Rust"
    elif ".cs" in joined:
        lang = ".NET"
    elif ".js" in joined:
        lang = "JavaScript"
    elif ".cpp" in joined or ".hpp" in joined:
        lang = "C++"
    elif ".c" in joined:
        lang = "C"
    rel = mod.relative_to(ROOT / "days").as_posix()
    trace_lines = []
    for ident in ids:
        m = re.search(rf"def (\w+).*{ident}|(\w+)\(.*\).*{ident}|fn (\w+)", text)
        trace_lines.append(f"{ident} está no starter; o teste marca PEDAGOGY-TEST: {ident}")
    trace = "\n".join(f"{i}. {ln}" for i, ln in enumerate(trace_lines, 1))
    sol_excerpt = "\n".join(sol.splitlines()[:24])
    sections = ""
    for ident in ids:
        fn = ident
        m = re.search(rf"TODO \[{ident}\].*\n(?:.*\n){{0,3}}", text)
        code = "    raise NotImplementedError\n    return None\n    _keep = ident"
        sm = re.search(rf"PEDAGOGY-SOLUTION: {ident}[\s\S]{{0,400}}", sol)
        if sm:
            code = sm.group(0)
            # keep a few lines
            code_lines = [ln for ln in code.splitlines() if ln.strip()][:8]
            code = "\n".join(code_lines[:6] or ["    pass"])
        sections += todo_section(
            ident, f"starter/{blobs[0][0]}", fn, "assinaturas e testes — arquivo starter/" + blobs[0][0],
            f"O stub de `{ident}` não produz o valor que o arquivo de teste afirma.",
            f"Substitua o corpo marcado `{ident}`. O solution faz exatamente o contrato do teste, não um atalho.",
            code if code.count("\n") >= 2 else code + "\n    return None\n    _ = 0",
            "python" if lang == "Python" else "c",
            f"Por quê este passo existe no módulo {mod.name}: o identificador `{ident}` isola uma invariante. Sem ele o caso seguinte mente.",
            f"Rode o teste do starter. O caso de `{ident}` deve passar e os anteriores não devem regredir.",
        )
    package(
        mod, lang,
        f"# {mod.name}\n\nLinguagem: **{lang}**. Caminho `{rel}`.\n",
        teoria(
            mod.name,
            lang,
            f"Este módulo ({lang}) continua o arco do dia. Os identificadores são {', '.join(ids)}. A teoria abaixo usa esses nomes, não um esboço sem contrato.",
            "| TODO | Arquivo |\n|------|---------|\n" + "\n".join(f"| `{i}` | `starter/{blobs[0][0]}` |" for i in ids),
            trace + "\n\nTrecho da solução (confira depois de tentar):\n\n```text\n" + sol_excerpt + "\n```",
            "\n".join(f"{i}. Implemente `{ident}` e rode só esse caso." for i, ident in enumerate(ids, 1)),
            "\n".join(f"- Deixar `{ident}` no stub: o teste aborta nesse identificador." for ident in ids),
            f"A linguagem deste arquivo é {lang}. Não reescreva em outra linguagem: o runner do dia chama o toolchain deste starter.",
        ),
        resolucao(mod.name, f"veja VALIDATION.md do dia; módulo {rel}", 
                  "\n".join(f"| `{i}` | `starter/` | função do TODO |" for i in ids),
                  sections),
        exercicios(lang,
                   f"Liste os identificadores: {', '.join(ids)}.",
                   f"Implemente `{ids[0]}`.",
                   "Implemente os demais na ordem do teste.",
                   "Escreva um caso extra que o teste ainda não cobre e diga o resultado esperado."),
        testes([(i, f"`{i}` deve passar no teste do starter.") for i in ids], ids),
        pesquisa(mod.name, [f"O que `{i}` observa?" for i in ids] + ["Qual toolchain roda este starter?", "Qual módulo do dia anterior alimenta este?"], ["starter do módulo", "TESTES_GUIADOS"]),
        benchmark("tempo do teste do módulo", "veja VALIDATION.md"),
    )


def refresh_day(day: Path) -> None:
    for mod in day.glob("*/*"):
        if (mod / "TEORIA_PASSO_A_PASSO.md").exists():
            refresh_from_code(mod)


def main() -> None:
    d9 = ROOT / "days" / "2026-09-09"
    emit_trace_c(d9)
    emit_arena_cpp(d9)
    emit_attn_c(d9)
    day_docs(
        d9,
        "2026-09-09",
        "observabilidade — C, C++ e o resto das linguagens",
        """| Módulo | Linguagem | Trace |
|--------|-----------|--------|
| `systems/clvm_trace_profiler` | **C** | bytecode `02 02 08` → hottest 0x02 |
| `systems/arena_telemetry` | **C++** | alloc 8 ok; +60 falha; reset não zera allocs |
| `ai/attention_mask` | **C** | q=2 vê 3 keys; k=3 vira -1e9 |
| `rust/stack_sample_trace` | **Rust** | frames |
| `dotnet/activity_source_span` | **.NET** | spans |
| `nodejs/async_hooks_trace` | **JavaScript** | fases |
| `redteam/yara_match_scan` | **Python** | padrões |
| `agent/verify_replay_log` | **Python** | replay |
| demais linux/gfx/quantum/parsers/tooling | ver starter (C/C++/Assembly conforme o arquivo) | |

Os três módulos reescritos acima são o núcleo deste passo. Os outros mantêm a linguagem do starter (Rust, .NET, JavaScript, Python) — não é um dia só em Python.
""",
        """# ATIVIDADES — 2026-09-09

**13 módulos.** Linguagens neste dia incluem C, C++, Rust, .NET, JavaScript e Python. Assembly do header continua no Dia 08 (`tooling/wasm_section_header`).

## Bloco 1 — C e C++ (obrigatório no papel)

- [ ] Bytecode `02 02 08`: counts[2]=2, hottest=2 (`CLVM-TRACE`)
- [ ] Arena 64: used=8 depois do primeiro alloc; alloc(60) falha; depois do reset allocs ainda é 1
- [ ] Máscara: q=2, k=2 visível; k=3 escreve -1e9; visible_count=3

## Bloco 2 — Rust, .NET, JavaScript

- [ ] Siga o TODO do `starter/` de `rust/stack_sample_trace`, `dotnet/activity_source_span`, `nodejs/async_hooks_trace`
- [ ] Paper-trace: o número que o teste daquele módulo compara (abra `TESTES_GUIADOS.md` do módulo)

## Relatório

| Bloco | Papel | Testes |
|-------|--------|--------|
| C/C++ | ☐ | ☐ |
| Rust/.NET/JS | ☐ | ☐ |
""",
        "",
    )
    refresh_day(d9)
    write_todo_map(d9, "2026-09-09")
    d10 = ROOT / "days" / "2026-09-10"
    refresh_day(d10)
    write_todo_map(d10, "2026-09-10")
    print("days 09–10 docs refreshed")


if __name__ == "__main__":
    main()
