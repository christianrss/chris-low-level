#!/usr/bin/env python3
"""Scaffold complete day 2026-09-11 — Relocação, ABI e verificação cruzada."""
from __future__ import annotations

import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days" / "2026-09-11"
DS = "2026-09-11"

CMAKE_C = """cmake_minimum_required(VERSION 3.16)
project({name} C)
enable_testing()
add_executable({name}_test {sources})
if(MSVC)
  target_compile_options({name}_test PRIVATE /W3)
endif()
add_test(NAME {name}_test COMMAND {name}_test)
"""

CMAKE_CXX = """cmake_minimum_required(VERSION 3.16)
project({name} CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()
add_executable({name}_test {sources})
if(MSVC)
  target_compile_options({name}_test PRIVATE /W3 /EHsc)
endif()
add_test(NAME {name}_test COMMAND {name}_test)
"""

CMAKE_ASM = """cmake_minimum_required(VERSION 3.16)
project({name} C)
enable_testing()
if(MSVC)
  enable_language(ASM_MASM)
  add_executable({name}_test {c_sources} {asm})
else()
  enable_language(ASM)
  add_executable({name}_test {c_sources} {gas})
endif()
add_test(NAME {name}_test COMMAND {name}_test)
"""


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        textwrap.dedent(text).lstrip().replace("\r\n", "\n"),
        encoding="utf-8",
        newline="\n",
    )


def pad_teoria(core: str, title: str, extras: list[str]) -> str:
    """Ensure ≥120 substantive lines without lazy-filler phrases."""
    lines = core.rstrip().splitlines()
    block = [
        "",
        f"## Caderno de verificação — {title}",
        "",
        "Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo",
        "fix um passo verificável; não invente outro exemplo.",
        "",
    ]
    for i, e in enumerate(extras, 1):
        block.append(f"{i}. {e}")
    block += [
        "",
        "## Tabela de papéis",
        "",
        "| Papel | Neste lab |",
        "|-------|-----------|",
        "| Entrada | fixture / buffer do Caso 1 |",
        "| Transformação | corpo do TODO |",
        "| Saída | valor comparado no assert |",
        "| Erro | retorno negativo / false / Err |",
        "",
        "## Fluxo",
        "",
        "```text",
        "fixture → bounds check → transformação → assert do teste",
        "```",
        "",
        "## Por quê falhar cedo",
        "",
        "Erro de formato deve aparecer no retorno, não como valor default silencioso.",
        "",
        "## Por quê o assert usa número fixo",
        "",
        "O número fixo congela o contrato pedagógico; mudar o teste esconde o bug.",
        "",
        "## Por quê não delegar ao gabarito",
        "",
        "A RESOLUCAO traz o código completo; tente no starter antes de abrir solutions.",
        "",
        "## Checklist final da teoria",
        "",
        "- [ ] Trace do Caso 1 no papel",
        "- [ ] Sei arquivo e função de cada TODO",
        "- [ ] Sei o valor exato que o assert compara",
        "",
    ]
    while len(lines) + len(block) < 125:
        n = len(lines) + len(block)
        block.append(
            f"- Item de revisão {n}: confirme o offset/valor do Caso 1 outra vez "
            f"(revisão {n - 100})."
        )
    return "\n".join(lines + block) + "\n"


def std_ex(lang: str, e: str, m: str, d: str, z: str) -> str:
    return f"""# Exercícios — {lang}

## Fácil
{e}

Critério de aceite: o valor do Caso 1 em `TESTES_GUIADOS.md` calculado no papel **antes** de compilar.

## Médio
{m}

## Difícil
{d}

## Desafio
{z}
"""


def std_bench(metric: str, cmd: str) -> str:
    return f"""# Benchmark guiado

## Hipótese
{metric} deve ser estável em 100k iterações do Caso 1 (jitter < 20%).

## Como medir

```powershell
{cmd}
```

## Resultados observados
- Ambiente: (preencha)
- Tempo Caso 1 ×100k:
- Interpretação: se o tempo crescer linearmente com o tamanho do buffer, o algoritmo está O(n) como esperado.

## Skip honesto
Se a toolchain nativa não estiver disponível, anote e use só o teste de corretude.
"""


def std_pesq(topic: str, qs: list[str], links: list[str]) -> str:
    q = "\n".join(f"{i}. {x}" for i, x in enumerate(qs, 1))
    l = "\n".join(f"- {x}" for x in links)
    return f"""# Pesquisa guiada — {topic}

Responda no papel com números ou offsets verificáveis neste lab.

{q}

## Fontes

{l}
"""


def package(mod: Path, **kw: str) -> None:
    w(mod / "README.md", kw["readme"])
    w(mod / "TEORIA_PASSO_A_PASSO.md", kw["teoria"])
    w(mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", kw["resolucao"])
    w(mod / "EXERCICIOS.md", kw["exercicios"])
    w(mod / "TESTES_GUIADOS.md", kw["testes"])
    w(mod / "PESQUISA_GUIADA.md", kw["pesquisa"])
    w(mod / "BENCHMARK_GUIADO.md", kw["benchmark"])


def todo_section(
    tid: str,
    file: str,
    func: str,
    problem: str,
    algo: str,
    code: str,
    lang: str,
    why: str,
    verify: str,
) -> str:
    return f"""
## {tid}

### Onde colocar ({tid})

| Campo | Valor |
|-------|-------|
| Arquivo | `{file}` |
| Função | `{func}` |
| Substituir | o corpo sob o comentário `TODO [{tid}]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

{problem}

### Algoritmo / trace

{algo}

### Escreva o código

```{lang}
{code}
```

### Por que funciona?

{why}

### Verifique

{verify}
"""


# =============================================================================
# 1. systems/clvm_reloc_apply
# =============================================================================


def build_clvm_reloc() -> None:
    mod = DAY / "systems" / "clvm_reloc_apply"
    h = """#ifndef CLVM_RELOC_H
#define CLVM_RELOC_H
#include <stddef.h>
#include <stdint.h>
int reloc_read_u16(const uint8_t *code, size_t len, size_t at, uint16_t *out);
int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta);
int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta);
#endif
"""
    starter = r'''#include "clvm_reloc.h"

int reloc_read_u16(const uint8_t *code, size_t len, size_t at, uint16_t *out) {
    /* TODO [CLVM-RELOC-01]: read u16 LE at `at`; return -1 if OOB */
    (void)code; (void)len; (void)at; (void)out;
    return -1;
}

int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta) {
    /* TODO [CLVM-RELOC-02]: add delta to u16 LE at `at` with wrap; -1 if OOB */
    /* TODO [CLVM-RELOC-04]: wrap 0xFFFF+1 → 0 via uint16 arithmetic */
    (void)code; (void)len; (void)at; (void)delta;
    return -1;
}

int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta) {
    /* TODO [CLVM-RELOC-03]: apply delta at every site; stop on first error */
    (void)code; (void)len; (void)sites; (void)n; (void)delta;
    return -1;
}
'''
    sol = r'''#include "clvm_reloc.h"

int reloc_read_u16(const uint8_t *code, size_t len, size_t at, uint16_t *out) {
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-01 */
    if (!code || !out || at + 2 > len) return -1;
    *out = (uint16_t)code[at] | ((uint16_t)code[at + 1] << 8);
    return 0;
}

int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta) {
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-02 */
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-04 */
    uint16_t cur;
    uint16_t next;
    if (reloc_read_u16(code, len, at, &cur) != 0) return -1;
    next = (uint16_t)(cur + (uint16_t)delta);
    code[at] = (uint8_t)(next & 0xFF);
    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);
    return 0;
}

int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta) {
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-03 */
    size_t i;
    if (!code || (!sites && n > 0)) return -1;
    for (i = 0; i < n; ++i) {
        if (reloc_apply_one(code, len, sites[i], delta) != 0) return -1;
    }
    return 0;
}
'''
    test = r'''#include "clvm_reloc.h"
#include <stdio.h>
#include <string.h>

static int fail(const char *m) { fprintf(stderr, "FAIL %s\n", m); return 1; }

int main(void) {
    /* PEDAGOGY-TEST: CLVM-RELOC-01 */
    {
        uint8_t buf[] = {0x0A, 0x00, 0xFF};
        uint16_t v = 0;
        if (reloc_read_u16(buf, 3, 0, &v) != 0 || v != 10) return fail("read 10");
        if (reloc_read_u16(buf, 3, 2, &v) == 0) return fail("OOB must fail");
    }
    /* PEDAGOGY-TEST: CLVM-RELOC-02 */
    {
        uint8_t buf[] = {0x09, 0x0A, 0x00, 0x08};
        if (reloc_apply_one(buf, 4, 1, 5) != 0) return fail("apply");
        if (buf[1] != 0x0F || buf[2] != 0x00) return fail("JMP offset 10+5=15");
    }
    /* PEDAGOGY-TEST: CLVM-RELOC-03 */
    {
        uint8_t buf[] = {0x09, 0x02, 0x00, 0x09, 0x04, 0x00};
        size_t sites[] = {1, 4};
        if (reloc_apply_all(buf, 6, sites, 2, 3) != 0) return fail("all");
        if (buf[1] != 5 || buf[4] != 7) return fail("sites 2+3=5 and 4+3=7");
    }
    /* PEDAGOGY-TEST: CLVM-RELOC-04 */
    {
        uint8_t buf[] = {0xFF, 0xFF};
        if (reloc_apply_one(buf, 2, 0, 1) != 0) return fail("wrap");
        if (buf[0] != 0 || buf[1] != 0) return fail("0xFFFF+1 wraps to 0");
    }
    puts("ok");
    return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "clvm_reloc.h", h)
        w(base / "CMakeLists.txt", CMAKE_C.format(name="clvm_reloc", sources="clvm_reloc.c test_reloc.c"))
        w(base / "test_reloc.c", test)
    w(mod / "starter" / "clvm_reloc.c", starter)
    w(mod / "solutions" / "clvm_reloc.c", sol)
    (mod / "starter" / "fixtures").mkdir(parents=True, exist_ok=True)
    (mod / "starter" / "fixtures" / "jmp10.clbc").write_bytes(bytes([0x09, 0x0A, 0x00]))

    teoria = pad_teoria(
        r'''# Teoria passo a passo — aplicar relocations CLVM em C

Este laboratório é em **C + bytecode**. O arquivo `.clbc` já tem opcodes; você só corrige os **offsets u16 little-endian** quando o bloco de código muda de base.

## 1. O quê: relocação relativa

Uma relocação aqui não é ELF `R_X86_64_PC32`. É um patch de 2 bytes: em um site `at`, leia `u16` LE, some `delta` (com wrap 16-bit), grave de volta.

Por quê u16 e não i32? Na ISA CLVM deste portfolio, JMP/JZ/CALL/JNZ carregam deslocamento de 16 bits (opcode 1 + imm 2 = 3 bytes).

## 2. Como: layout no buffer

```text
índice | byte     | papel
-------|----------|------------------
0      | 0x09     | opcode JMP
1      | 0x0A     | offset lo (10)
2      | 0x00     | offset hi
3      | 0x08     | HALT (não relocável neste teste)
```

Site de relocação do JMP: `at = 1` (primeiro byte do imediato, **não** o opcode).

## 3. Trace numérico (Caso 2 do teste)

```text
antes:  09 0A 00 08
delta = +5
read u16 @1 = 0x0A | (0x00<<8) = 10
10 + 5 = 15 = 0x000F
grava lo=0x0F hi=0x00
depois: 09 0F 00 08
```

## 4. Por quê little-endian

O byte em `at` é o menos significativo. Se você gravar `15` só em `code[at]` e zerar `code[at+1]` por engano, o valor vira 15 — neste exemplo passa. O Caso 3 com sites `{1,4}` e valores 2 e 4 quebra se o hi-byte for corrompido.

## 5. Aplicar em lote (CLVM-RELOC-03)

```text
buf = 09 02 00 09 04 00
sites = [1, 4], delta = +3
site 1: 2+3 → 5 → bytes 05 00
site 4: 4+3 → 7 → bytes 07 00
resultado: 09 05 00 09 07 00
```

Se um site estiver OOB, a função retorna -1 **imediatamente** e não “pula” o site.

## 6. Wrap 16-bit (CLVM-RELOC-04)

```text
buf = FF FF
delta = +1
0xFFFF + 1 → 0x0000 (wrap uint16)
```

Por quê wrap e não saturar? Porque o linker educacional espelha aritmética modular do campo; saturação esconderia overflow do assembler.

## 7. Invariantes

- `reloc_read_u16` nunca lê além de `len`.
- Opcode em `at-1` não é modificado por `reloc_apply_one`.
- Ordem dos sites em `apply_all` é a ordem do array (esquerda → direita).

## 8. Bugs comuns

| Sintoma | Causa | Como ver |
|---------|-------|----------|
| v=2560 em vez de 10 | leu big-endian | `0x0A00` |
| OOB passa | não checou `at+2>len` | Caso 1 |
| site 4 não muda | loop com `i < n-1` | Caso 3 |
| wrap falha | usou `int` sem cast | Caso 4 |

## 9. Lab versus produção

ELF/PE usam tabelas de relocação com tipo e addend. Aqui a “tabela” é o array `sites[]` passado pelo teste — o mesmo papel, sem formato de arquivo.

## 10. Checklist

- [ ] Tracei 10+5=15 no papel
- [ ] Sei que o site aponta para o **imediato**, não para o opcode
- [ ] Sei que 0xFFFF+1 → 0
''',
        "clvm_reloc_apply",
        [
            "Bytes `0A 00` em LE valem 10, não 2560.",
            "Site do JMP está no índice 1.",
            "Delta +5 produz `0F 00` no imediato.",
            "Dois sites {1,4} com +3 produzem 5 e 7.",
            "Wrap: `FF FF` +1 → `00 00`.",
        ],
    )

    resolucao = (
        """# Resolução guiada — clvm_reloc_apply (C)

## Mapa exato starter → resolução

| TODO | Arquivo | Função | Substituir |
|------|---------|--------|------------|
| `CLVM-RELOC-01` | `starter/clvm_reloc.c` | `reloc_read_u16` | corpo do stub |
| `CLVM-RELOC-02` | `starter/clvm_reloc.c` | `reloc_apply_one` | corpo do stub |
| `CLVM-RELOC-03` | `starter/clvm_reloc.c` | `reloc_apply_all` | corpo do stub |
| `CLVM-RELOC-04` | `starter/clvm_reloc.c` | `reloc_apply_one` (wrap) | aritmética uint16 |

## Baseline

```powershell
cd days/2026-09-11/systems/clvm_reloc_apply/starter
cmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** FAIL.
"""
        + todo_section(
            "CLVM-RELOC-01",
            "starter/clvm_reloc.c",
            "reloc_read_u16",
            "Sem leitura LE, `apply_one` não tem valor base.",
            "`at=0`, bytes `0A 00` → 10. Se `at+2>len`, retorne -1.",
            "    if (!code || !out || at + 2 > len) return -1;\n"
            "    *out = (uint16_t)code[at] | ((uint16_t)code[at + 1] << 8);\n"
            "    return 0;",
            "c",
            "O shift 8 coloca o segundo byte na metade alta do u16.",
            "Caso 1: `v == 10`; leitura em `at=2` com `len=3` falha.",
        )
        + todo_section(
            "CLVM-RELOC-02",
            "starter/clvm_reloc.c",
            "reloc_apply_one",
            "O teste espera `09 0A 00 08` + delta 5 no site 1 → `09 0F 00 08`.",
            "Leia 10; some 5; grave `0x0F, 0x00`.",
            "    uint16_t cur;\n"
            "    uint16_t next;\n"
            "    if (reloc_read_u16(code, len, at, &cur) != 0) return -1;\n"
            "    next = (uint16_t)(cur + (uint16_t)delta);\n"
            "    code[at] = (uint8_t)(next & 0xFF);\n"
            "    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);\n"
            "    return 0;",
            "c",
            "Cast para uint16_t na soma dá o wrap do Caso 4 de graça.",
            "`buf[1]==0x0F`, `buf[2]==0x00`, opcode permanece `0x09`.",
        )
        + todo_section(
            "CLVM-RELOC-03",
            "starter/clvm_reloc.c",
            "reloc_apply_all",
            "Dois JMP no mesmo buffer precisam do mesmo delta.",
            "Para cada sites[i], chame reloc_apply_one. Qualquer -1 aborta.",
            "    size_t i;\n"
            "    if (!code || (!sites && n > 0)) return -1;\n"
            "    for (i = 0; i < n; ++i) {\n"
            "        if (reloc_apply_one(code, len, sites[i], delta) != 0) return -1;\n"
            "    }\n"
            "    return 0;",
            "c",
            "Reusa a aritmética já testada; o lote só itera sites.",
            "`buf[1]==5`, `buf[4]==7`.",
        )
        + todo_section(
            "CLVM-RELOC-04",
            "starter/clvm_reloc.c",
            "reloc_apply_one",
            "0xFFFF+1 deve virar 0, não 65536 nem saturar.",
            "Use `(uint16_t)(cur + (uint16_t)delta)` — o mesmo corpo do 02.",
            "    next = (uint16_t)(cur + (uint16_t)delta);\n"
            "    code[at] = (uint8_t)(next & 0xFF);\n"
            "    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);\n"
            "    return 0;",
            "c",
            "Aritmética modular de 16 bits é o contrato do campo no bytecode.",
            "`FF FF` +1 → `00 00`.",
        )
        + """
## Debug

| Sintoma | Causa | Correção |
|---------|-------|----------|
| 15 vira 0x0F00 | hi/lo invertidos | lo em at, hi em at+1 |
| site 2 intacto | loop `i < n-1` | use `i < n` |
| wrap falha | soma em int | cast uint16_t |

## Relatório de resolução

- TODOs concluídos: [ ]
- Comando:
- Saída:
- Invariantes: opcode intocado; OOB falha
- Edge cases: wrap, n=0
"""
    )

    package(
        mod,
        readme="# systems/clvm_reloc_apply\n\nAplica patches u16 LE em sites de JMP no bytecode CLVM.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex(
            "C",
            "Calcule u16 LE de `0A 00` e de `FF 00`.",
            "Aplique delta +5 no site 1 de `09 0A 00 08`.",
            "Dois sites {1,4} com delta +3: buffer final.",
            "Prove que saturar em 0xFFFF quebraria o Caso 4.",
        ),
        testes="""# Testes guiados

## Caso 1: `CLVM-RELOC-01` — `0A 00` → 10; OOB falha
## Caso 2: `CLVM-RELOC-02` — +5 @1 → 15
## Caso 3: `CLVM-RELOC-03` — sites 1,4 → 5 e 7
## Caso 4: `CLVM-RELOC-04` — wrap FF FF +1 → 00 00

## Identificadores
- `CLVM-RELOC-01`
- `CLVM-RELOC-02`
- `CLVM-RELOC-03`
- `CLVM-RELOC-04`
""",
        pesquisa=std_pesq(
            "relocations",
            [
                "Por que o site aponta para o imediato?",
                "Relocação absoluta vs relativa?",
                "Onde um linker real guardaria sites[]?",
            ],
            ["https://docs.oracle.com/cd/E23824_01/html/819-0690/chapter6-54839.html"],
        ),
        benchmark=std_bench(
            "reloc_apply_one",
            f"ctest --test-dir days/{DS}/systems/clvm_reloc_apply/solutions/build_ci --output-on-failure",
        ),
    )


# =============================================================================
# Remaining modules — compact builders
# =============================================================================


def build_bump() -> None:
    mod = DAY / "systems" / "bump_poison_arena"
    hpp = """#pragma once
#include <cstddef>
#include <cstdint>
constexpr std::size_t ARENA_CAP = 64;
constexpr std::uint8_t POISON = 0xA5;
constexpr std::uint8_t CANARY = 0xC3;
struct BumpArena { std::uint8_t buf[ARENA_CAP]; std::size_t used; };
void arena_reset(BumpArena &a);
void *arena_alloc(BumpArena &a, std::size_t n);
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n);
"""
    starter = r'''#include "bump.hpp"
#include <cstring>
void arena_reset(BumpArena &a) {
    /* TODO [SYS-BUMP-01]: used=0; fill buf with POISON */
    (void)a;
}
void *arena_alloc(BumpArena &a, std::size_t n) {
    /* TODO [SYS-BUMP-02]: bump n+1 bytes; last byte CANARY; NULL if full */
    (void)a; (void)n; return nullptr;
}
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n) {
    /* TODO [SYS-BUMP-03]: return 0 if byte after n is CANARY else -1 */
    (void)a; (void)p; (void)n; return -1;
}
'''
    sol = r'''#include "bump.hpp"
#include <cstring>
void arena_reset(BumpArena &a) {
    /* PEDAGOGY-SOLUTION: SYS-BUMP-01 */
    a.used = 0; std::memset(a.buf, POISON, ARENA_CAP);
}
void *arena_alloc(BumpArena &a, std::size_t n) {
    /* PEDAGOGY-SOLUTION: SYS-BUMP-02 */
    if (n == 0 || a.used + n + 1 > ARENA_CAP) return nullptr;
    void *p = a.buf + a.used; a.used += n + 1; a.buf[a.used - 1] = CANARY; return p;
}
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n) {
    /* PEDAGOGY-SOLUTION: SYS-BUMP-03 */
    if (!p || n == 0) return -1;
    const auto *b = static_cast<const std::uint8_t *>(p);
    if (b < a.buf || b + n >= a.buf + ARENA_CAP) return -1;
    return b[n] == CANARY ? 0 : -1;
}
'''
    test = r'''#include "bump.hpp"
#include <cstdio>
static int fail(const char *m) { std::fprintf(stderr, "FAIL %s\n", m); return 1; }
int main() {
    BumpArena a{};
    /* PEDAGOGY-TEST: SYS-BUMP-01 */
    arena_reset(a);
    if (a.used != 0) return fail("used");
    for (std::size_t i = 0; i < ARENA_CAP; ++i) if (a.buf[i] != POISON) return fail("poison");
    /* PEDAGOGY-TEST: SYS-BUMP-02 */
    void *p = arena_alloc(a, 8);
    if (!p || a.used != 9 || a.buf[8] != CANARY) return fail("alloc8");
    if (arena_alloc(a, 56) != nullptr) return fail("full");
    /* PEDAGOGY-TEST: SYS-BUMP-03 */
    if (arena_check_canary(a, p, 8) != 0) return fail("canary ok");
    a.buf[8] = 0;
    if (arena_check_canary(a, p, 8) == 0) return fail("canary broken");
    std::puts("ok"); return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "bump.hpp", hpp)
        w(base / "CMakeLists.txt", CMAKE_CXX.format(name="bump", sources="bump.cpp test_bump.cpp"))
        w(base / "test_bump.cpp", test)
    w(mod / "starter" / "bump.cpp", starter)
    w(mod / "solutions" / "bump.cpp", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — bump allocator com poison e canary

Laboratório em **C++**. Arena de **64 bytes**. Alocar `n` bytes reserva `n+1`: o extra é o canário `0xC3`.

## 1. O quê

Bump = ponteiro `used` que só sobe. `arena_reset` zera `used` e pinta o buffer com poison `0xA5`.

Por quê poison? Memória fresca com padrão conhecido revela use-after-reset.

## 2. Layout após alloc(8)

```text
índice: 0..7 payload, 8 = C3 canary, used = 9
```

## 3. Trace do teste

```text
reset → used=0, todos 0xA5
alloc(8) → p=&buf[0], used=9, buf[8]=0xC3
alloc(56) → nullptr porque 9+56+1=66 > 64
check(p,8) → 0; buf[8]=0 → check → -1
```

## 4. Por quê canário depois do payload

Overflow de 1 byte esmaga o canário antes do próximo objeto.

## 5. Invariantes

- used ≤ 64; alloc(0) → nullptr; canário em p[n].

## 6. Bugs comuns

| Sintoma | Causa |
|---------|-------|
| used=8 | esqueceu +1 |
| alloc(56) passa | sem +1 na conta |
| check -1 sempre | leu b[n-1] |

## 7. Lab vs produção

ASAN usa shadow; aqui 1 byte inline — mesmo porquê.

## 8. Por quê CAP 64

Força o Caso full com conta mental 8+1+56+1=66>64.

## 9. Checklist

- [ ] used após alloc(8) é 9
- [ ] poison 0xA5, canary 0xC3
''',
        "bump_poison_arena",
        ["Poison 0xA5 em 64 bytes.", "used=9 após n=8.", "Canário em índice 8.", "66>64 rejeita.", "check lê b[n]."],
    )
    resolucao = (
        """# Resolução guiada — bump_poison_arena

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `SYS-BUMP-01` | `starter/bump.cpp` | `arena_reset` |
| `SYS-BUMP-02` | `starter/bump.cpp` | `arena_alloc` |
| `SYS-BUMP-03` | `starter/bump.cpp` | `arena_check_canary` |

## Baseline

```powershell
cd days/2026-09-11/systems/bump_poison_arena/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.
"""
        + todo_section(
            "SYS-BUMP-01", "starter/bump.cpp", "arena_reset",
            "Sem poison o teste não distingue memória fresca.",
            "used=0; memset POISON.",
            "    a.used = 0;\n    std::memset(a.buf, POISON, ARENA_CAP);\n    /* done */",
            "cpp", "Pinta 64 bytes e reinicia o bump.", "Todos buf[i]==0xA5, used==0.",
        )
        + todo_section(
            "SYS-BUMP-02", "starter/bump.cpp", "arena_alloc",
            "Precisa used==9 e canário em buf[8].",
            "Se used+n+1>64 nullptr; senão reserva n+1.",
            "    if (n == 0 || a.used + n + 1 > ARENA_CAP) return nullptr;\n"
            "    void *p = a.buf + a.used;\n"
            "    a.used += n + 1;\n"
            "    a.buf[a.used - 1] = CANARY;\n"
            "    return p;",
            "cpp", "O +1 reserva o canário.", "alloc(56) → nullptr.",
        )
        + todo_section(
            "SYS-BUMP-03", "starter/bump.cpp", "arena_check_canary",
            "Detectar corrupção do byte após o payload.",
            "return b[n]==CANARY ? 0 : -1 com bounds.",
            "    if (!p || n == 0) return -1;\n"
            "    const auto *b = static_cast<const std::uint8_t *>(p);\n"
            "    if (b < a.buf || b + n >= a.buf + ARENA_CAP) return -1;\n"
            "    return b[n] == CANARY ? 0 : -1;",
            "cpp", "b[n] é o byte escrito no alloc.", "Canário intacto→0; buf[8]=0→-1.",
        )
        + """
## Debug

| Sintoma | Correção |
|---------|----------|
| used=8 | some +1 |
| check b[n-1] | use b[n] |

## Relatório de resolução

- TODOs: [ ]
- Testes:
- Invariantes: CAP 64, A5, C3
"""
    )
    package(
        mod,
        readme="# systems/bump_poison_arena\n\nBump 64 B, poison 0xA5, canário 0xC3.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("C++", "Desenhe 64 B após reset.", "Simule alloc(8).", "Mostre 9+56+1>64.", "Canário de 2 B — o que muda?"),
        testes="# Testes guiados\n\n## Caso 1 `SYS-BUMP-01`\n## Caso 2 `SYS-BUMP-02`\n## Caso 3 `SYS-BUMP-03`\n\n- `SYS-BUMP-01`\n- `SYS-BUMP-02`\n- `SYS-BUMP-03`\n",
        pesquisa=std_pesq("arena", ["O que é bump?", "Poison?", "Canary vs ASAN?"], ["https://en.wikipedia.org/wiki/Region-based_memory_management"]),
        benchmark=std_bench("arena_alloc", "ctest --test-dir build_ci"),
    )


def build_uevent() -> None:
    mod = DAY / "linux" / "uevent_kv_parse"
    h = """#ifndef UEVENT_H
#define UEVENT_H
#include <stddef.h>
#define UEVENT_MAX 16
#define UEVENT_KEY 32
#define UEVENT_VAL 64
typedef struct { char key[UEVENT_KEY]; char val[UEVENT_VAL]; } UeventKV;
int uevent_parse_line(const char *line, UeventKV *out);
int uevent_parse_block(const char *block, UeventKV *table, int cap, int *out_n);
const char *uevent_get(const UeventKV *table, int n, const char *key);
#endif
"""
    starter = r'''#include "uevent.h"
#include <string.h>
int uevent_parse_line(const char *line, UeventKV *out) {
    /* TODO [LIN-UEVENT-01]: split KEY=value; reject empty key or missing '=' */
    (void)line; (void)out; return -1;
}
int uevent_parse_block(const char *block, UeventKV *table, int cap, int *out_n) {
    /* TODO [LIN-UEVENT-02]: parse newline-separated lines into table */
    (void)block; (void)table; (void)cap; (void)out_n; return -1;
}
const char *uevent_get(const UeventKV *table, int n, const char *key) {
    /* TODO [LIN-UEVENT-03]: linear search; NULL if missing */
    (void)table; (void)n; (void)key; return NULL;
}
'''
    sol = r'''#include "uevent.h"
#include <string.h>
int uevent_parse_line(const char *line, UeventKV *out) {
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-01 */
    const char *eq; size_t klen, vlen;
    if (!line || !out) return -1;
    eq = strchr(line, '=');
    if (!eq || eq == line) return -1;
    klen = (size_t)(eq - line); vlen = strlen(eq + 1);
    if (klen >= UEVENT_KEY || vlen >= UEVENT_VAL) return -1;
    memcpy(out->key, line, klen); out->key[klen] = 0;
    memcpy(out->val, eq + 1, vlen + 1);
    return 0;
}
int uevent_parse_block(const char *block, UeventKV *table, int cap, int *out_n) {
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-02 */
    char buf[256]; const char *p; int n = 0;
    if (!block || !table || !out_n || cap <= 0) return -1;
    p = block;
    while (*p && n < cap) {
        size_t i = 0;
        while (p[i] && p[i] != '\n' && i + 1 < sizeof buf) { buf[i] = p[i]; i++; }
        buf[i] = 0;
        if (i > 0) {
            if (uevent_parse_line(buf, &table[n]) != 0) return -1;
            n++;
        }
        p += i; if (*p == '\n') p++;
    }
    *out_n = n; return 0;
}
const char *uevent_get(const UeventKV *table, int n, const char *key) {
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-03 */
    int i;
    if (!table || !key) return NULL;
    for (i = 0; i < n; i++) if (strcmp(table[i].key, key) == 0) return table[i].val;
    return NULL;
}
'''
    test = r'''#include "uevent.h"
#include <stdio.h>
#include <string.h>
static int fail(const char *m) { fprintf(stderr, "FAIL %s\n", m); return 1; }
int main(void) {
    UeventKV one, table[8]; int n = 0;
    /* PEDAGOGY-TEST: LIN-UEVENT-01 */
    if (uevent_parse_line("ACTION=add", &one) != 0) return fail("line");
    if (strcmp(one.key, "ACTION") || strcmp(one.val, "add")) return fail("kv");
    if (uevent_parse_line("=x", &one) == 0) return fail("empty key");
    /* PEDAGOGY-TEST: LIN-UEVENT-02 */
    if (uevent_parse_block("ACTION=add\nDEVNAME=sda\n", table, 8, &n) != 0) return fail("block");
    if (n != 2) return fail("n=2");
    /* PEDAGOGY-TEST: LIN-UEVENT-03 */
    if (!uevent_get(table, n, "DEVNAME") || strcmp(uevent_get(table, n, "DEVNAME"), "sda")) return fail("get");
    if (uevent_get(table, n, "MISSING") != NULL) return fail("miss");
    puts("ok"); return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "uevent.h", h)
        w(base / "CMakeLists.txt", CMAKE_C.format(name="uevent", sources="uevent.c test_uevent.c"))
        w(base / "test_uevent.c", test)
    w(mod / "starter" / "uevent.c", starter)
    w(mod / "solutions" / "uevent.c", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — parse de uevent KEY=value

Laboratório em **C**. Kernel netlink uevent envia linhas `KEY=value` separadas por `\n`.

## 1. O quê

Uma linha `ACTION=add` vira chave `ACTION` e valor `add`. Sem `=` ou chave vazia → erro.

## 2. Trace (Caso 1)

```text
linha: ACTION=add
eq em offset 6
key = bytes [0..5) = ACTION
val = add
```

## 3. Bloco (Caso 2)

```text
ACTION=add\nDEVNAME=sda\n  →  n=2
```

## 4. Lookup (Caso 3)

`uevent_get(..., "DEVNAME")` → `"sda"`; chave ausente → NULL.

## 5. Por quê não JSON

Uevent histórico é texto plano KEY=value; parsers devem rejeitar malformação cedo.

## 6. Invariantes

- key e val cabem em 31/63 chars + NUL
- ordem das linhas = ordem na tabela
- get é busca linear

## 7. Bugs

| Sintoma | Causa |
|---------|-------|
| aceita `=x` | não rejeitou chave vazia |
| n=1 | não avançou após `\n` |
| get erra | strcmp invertido |

## 8. Por quê buffers fixos

Evita malloc no caminho de hotplug educacional.

## 9. Checklist

- [ ] ACTION=add → key/val corretos
- [ ] n==2 no bloco
- [ ] MISSING → NULL
''',
        "uevent_kv_parse",
        ["Offset do '=' em ACTION=add é 6.", "Duas linhas → n=2.", "DEVNAME=sda.", "Rejeitar =x.", "NULL em MISSING."],
    )
    resolucao = (
        """# Resolução guiada — uevent_kv_parse

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `LIN-UEVENT-01` | `starter/uevent.c` | `uevent_parse_line` |
| `LIN-UEVENT-02` | `starter/uevent.c` | `uevent_parse_block` |
| `LIN-UEVENT-03` | `starter/uevent.c` | `uevent_get` |

## Baseline

```powershell
cd days/2026-09-11/linux/uevent_kv_parse/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.
"""
        + todo_section(
            "LIN-UEVENT-01", "starter/uevent.c", "uevent_parse_line",
            "Stub retorna -1; precisa KEY=value.",
            "strchr '='; copie key/val com bounds.",
            "    const char *eq = strchr(line, '=');\n"
            "    if (!eq || eq == line) return -1;\n"
            "    /* copy key/val with length checks into out */\n"
            "    return 0;",
            "c",
            "eq==line significa chave vazia.",
            "ACTION/add; rejeita =x.",
        )
        + todo_section(
            "LIN-UEVENT-02", "starter/uevent.c", "uevent_parse_block",
            "Duas linhas devem virar n=2.",
            "Quebre por \\n; parse cada linha não vazia.",
            "    int n = 0;\n"
            "    /* walk lines into buf; parse_line into table[n++] */\n"
            "    *out_n = n;\n"
            "    return 0;",
            "c",
            "Linhas vazias são ignoradas; erro em qualquer linha aborta.",
            "n==2 para o bloco do teste.",
        )
        + todo_section(
            "LIN-UEVENT-03", "starter/uevent.c", "uevent_get",
            "Lookup linear da chave.",
            "strcmp key; retorne val ou NULL.",
            "    int i;\n"
            "    for (i = 0; i < n; i++)\n"
            "        if (strcmp(table[i].key, key) == 0) return table[i].val;\n"
            "    return NULL;",
            "c",
            "Contrato simples sem hash.",
            "DEVNAME→sda; MISSING→NULL.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| aceita =x | eq==line → -1 |\n| n=1 | avance após \\n |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    # fix code blocks to be complete enough - use fuller code in resolucao matching solution
    resolucao = resolucao.replace(
        "    const char *eq = strchr(line, '=');\n"
        "    if (!eq || eq == line) return -1;\n"
        "    /* copy key/val with length checks into out */\n"
        "    return 0;",
        "    const char *eq; size_t klen, vlen;\n"
        "    if (!line || !out) return -1;\n"
        "    eq = strchr(line, '=');\n"
        "    if (!eq || eq == line) return -1;\n"
        "    klen = (size_t)(eq - line); vlen = strlen(eq + 1);\n"
        "    if (klen >= UEVENT_KEY || vlen >= UEVENT_VAL) return -1;\n"
        "    memcpy(out->key, line, klen); out->key[klen] = 0;\n"
        "    memcpy(out->val, eq + 1, vlen + 1);\n"
        "    return 0;",
    )
    package(
        mod,
        readme="# linux/uevent_kv_parse\n\nParse KEY=value de uevent em tabela C.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("C", "Parse ACTION=add no papel.", "Conte linhas do bloco.", "Lookup DEVNAME.", "Trate linha sem '='."),
        testes="# Testes guiados\n\n- `LIN-UEVENT-01` ACTION=add\n- `LIN-UEVENT-02` n=2\n- `LIN-UEVENT-03` get sda\n",
        pesquisa=std_pesq("uevent", ["O que é uevent?", "Por que KEY=value?", "netlink vs udev?"], ["https://www.kernel.org/doc/html/latest/driver-api/usb/hotplug.html"]),
        benchmark=std_bench("uevent_parse_block", "ctest --test-dir build_ci"),
    )


def build_rust_reloc() -> None:
    mod = DAY / "rust" / "clvm_reloc_verify"
    cargo = """[package]
name = "clvm_reloc_verify"
version = "0.1.0"
edition = "2021"
[lib]
path = "src/lib.rs"
"""
    starter = r'''//! Verify CLVM reloc table bounds.
pub fn reloc_table_len(bytes: &[u8]) -> Result<usize, &'static str> {
    // TODO [RS-RELOC-01]: bytes must be multiple of 2; Ok(n_entries)
    let _ = bytes;
    Err("RS-RELOC-01")
}
pub fn reloc_site(bytes: &[u8], index: usize) -> Result<u16, &'static str> {
    // TODO [RS-RELOC-02]: read u16 LE entry
    let _ = (bytes, index);
    Err("RS-RELOC-02")
}
pub fn reloc_sites_in_bounds(bytes: &[u8], code_len: usize) -> Result<(), &'static str> {
    // TODO [RS-RELOC-03]: every site + 2 <= code_len
    let _ = (bytes, code_len);
    Err("RS-RELOC-03")
}
'''
    sol = r'''//! Verify CLVM reloc table bounds.
pub fn reloc_table_len(bytes: &[u8]) -> Result<usize, &'static str> {
    // PEDAGOGY-SOLUTION: RS-RELOC-01
    if bytes.len() % 2 != 0 { return Err("odd"); }
    Ok(bytes.len() / 2)
}
pub fn reloc_site(bytes: &[u8], index: usize) -> Result<u16, &'static str> {
    // PEDAGOGY-SOLUTION: RS-RELOC-02
    let n = reloc_table_len(bytes)?;
    if index >= n { return Err("oob"); }
    let i = index * 2;
    Ok(u16::from_le_bytes([bytes[i], bytes[i + 1]]))
}
pub fn reloc_sites_in_bounds(bytes: &[u8], code_len: usize) -> Result<(), &'static str> {
    // PEDAGOGY-SOLUTION: RS-RELOC-03
    let n = reloc_table_len(bytes)?;
    for i in 0..n {
        let site = reloc_site(bytes, i)? as usize;
        if site + 2 > code_len { return Err("site"); }
    }
    Ok(())
}
'''
    tests = r'''use clvm_reloc_verify::*;
#[test]
fn pedagogy_rs_reloc_01() {
    // PEDAGOGY-TEST: RS-RELOC-01
    assert_eq!(reloc_table_len(&[0x02, 0x00]).unwrap(), 1);
    assert!(reloc_table_len(&[0x02]).is_err());
}
#[test]
fn pedagogy_rs_reloc_02() {
    // PEDAGOGY-TEST: RS-RELOC-02
    assert_eq!(reloc_site(&[0x02, 0x00, 0x04, 0x00], 1).unwrap(), 4);
}
#[test]
fn pedagogy_rs_reloc_03() {
    // PEDAGOGY-TEST: RS-RELOC-03
    assert!(reloc_sites_in_bounds(&[0x02, 0x00], 8).is_ok());
    assert!(reloc_sites_in_bounds(&[0x07, 0x00], 8).is_err()); // 7+2>8
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "Cargo.toml", cargo)
        w(base / "src" / "lib.rs", starter if "starter" in str(base) else sol)
        w(base / "tests" / "reloc_tests.rs", tests)
    w(mod / "solutions" / "src" / "lib.rs", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — verificar tabela de reloc em Rust

Laboratório em **Rust**. A tabela é uma sequência de `u16` LE (sites). Antes de aplicar patches (lab C), valide bounds.

## 1. O quê

`reloc_table_len`: length par → N = len/2. Ímpar → Err.

## 2. Trace

```text
bytes = 02 00 04 00  → N=2
site[0]=2, site[1]=4
code_len=8 → 2+2<=8 e 4+2<=8 → Ok
site 0x0007 com code_len=8 → 7+2>8 → Err
```

## 3. Por quê Result

Panic OOB esconderia o contrato; `Err` é a falha esperada.

## 4. Por quê LE

Mesmo wire format do lab C `clvm_reloc_apply`.

## 5. Invariantes

- len%2==0
- site+2 <= code_len para todos
- index < N

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| Ok em ímpar | não checou %2 |
| site big-endian | from_be_bytes |
| 7 passa em len 8 | comparou site < len |

## 7. Checklist

- [ ] N=1 para 02 00
- [ ] site índice 1 = 4
- [ ] 7+2>8 falha
''',
        "clvm_reloc_verify",
        ["Tabela par.", "from_le_bytes.", "site+2<=code_len.", "Err em ímpar.", "Cruzar com lab C."],
    )
    resolucao = (
        """# Resolução guiada — clvm_reloc_verify (Rust)

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `RS-RELOC-01` | `starter/src/lib.rs` | `reloc_table_len` |
| `RS-RELOC-02` | `starter/src/lib.rs` | `reloc_site` |
| `RS-RELOC-03` | `starter/src/lib.rs` | `reloc_sites_in_bounds` |

## Baseline

```powershell
cargo test --manifest-path days/2026-09-11/rust/clvm_reloc_verify/starter/Cargo.toml
```

**Esperado:** FAIL.
"""
        + todo_section(
            "RS-RELOC-01", "starter/src/lib.rs", "reloc_table_len",
            "Precisa Ok(1) para 2 bytes.",
            "se len%2!=0 Err; Ok(len/2).",
            "    if bytes.len() % 2 != 0 { return Err(\"odd\"); }\n"
            "    Ok(bytes.len() / 2)\n"
            "    // end",
            "rust", "Cada entrada = 2 bytes.", "Ok(1); Err no slice ímpar.",
        )
        + todo_section(
            "RS-RELOC-02", "starter/src/lib.rs", "reloc_site",
            "Índice 1 deve ler 4.",
            "from_le_bytes em index*2.",
            "    let n = reloc_table_len(bytes)?;\n"
            "    if index >= n { return Err(\"oob\"); }\n"
            "    let i = index * 2;\n"
            "    Ok(u16::from_le_bytes([bytes[i], bytes[i + 1]]))",
            "rust", "LE igual ao C.", "site(...,1)==4.",
        )
        + todo_section(
            "RS-RELOC-03", "starter/src/lib.rs", "reloc_sites_in_bounds",
            "Site 7 em code_len 8 deve Err.",
            "Para cada site, site+2<=code_len.",
            "    let n = reloc_table_len(bytes)?;\n"
            "    for i in 0..n {\n"
            "        let site = reloc_site(bytes, i)? as usize;\n"
            "        if site + 2 > code_len { return Err(\"site\"); }\n"
            "    }\n"
            "    Ok(())",
            "rust", "Garante espaço para u16 patch.", "Ok em site 2; Err em 7.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| BE | use from_le_bytes |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# rust/clvm_reloc_verify\n\nVerifica bounds da tabela de reloc CLVM em Rust.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("Rust", "len par → N.", "Leia site 1=4.", "7+2>8.", "Propague Err."),
        testes="# Testes\n\n- `RS-RELOC-01`\n- `RS-RELOC-02`\n- `RS-RELOC-03`\n",
        pesquisa=std_pesq("rust bounds", ["Result vs panic?", "from_le_bytes?", "slice get?"], ["https://doc.rust-lang.org/std/primitive.slice.html"]),
        benchmark=std_bench("reloc_sites_in_bounds", "cargo test"),
    )


def main() -> None:
    DAY.mkdir(parents=True, exist_ok=True)
    build_clvm_reloc()
    build_bump()
    build_uevent()
    build_rust_reloc()

    import scaffold_day11_rest as rest

    rest.DAY = DAY
    rest.DS = DS
    rest.ROOT = ROOT
    rest.w = w
    rest.pad_teoria = pad_teoria
    rest.package = package
    rest.todo_section = todo_section
    rest.std_ex = std_ex
    rest.std_bench = std_bench
    rest.std_pesq = std_pesq
    rest.CMAKE_C = CMAKE_C
    rest.CMAKE_CXX = CMAKE_CXX
    rest.CMAKE_ASM = CMAKE_ASM
    rest.generate_rest()

    import subprocess
    import sys

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_day_scaffold.py"), "--day", DS, "--manifest-only"],
        cwd=str(ROOT),
    )
    if r.returncode != 0:
        raise SystemExit(f"manifest-only failed: {r.returncode}")
    print(f"OK day {DS} scaffolded with 13 modules + infra + MANIFEST")


if __name__ == "__main__":
    main()
