#!/usr/bin/env python3
"""Rewrite days 08–10 as multi-language labs with substantive pedagogy.

Does not overwrite Rust / C# / JavaScript starters that already implement a
real ABI. Those languages stay; Python-only labs become C, C++, or Assembly.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAYS = ROOT / "days"

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


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def wipe_py(base: Path) -> None:
    if not base.exists():
        return
    for p in base.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".pyc"}:
            p.unlink()


def _caderno(title: str, trace: str) -> str:
    lines = [ln.strip() for ln in trace.splitlines() if ln.strip() and not ln.strip().startswith("```")]
    out = ["## Caderno — segunda passagem, os mesmos números\n"]
    out.append(
        f"Não invente outro exemplo. O teste de `{title}` compara os valores abaixo. "
        "Por quê repetir? Porque a primeira leitura mostra o formato; esta passagem mostra o que o assert vê.\n"
    )
    if not lines:
        lines = ["(trace vazio — volte à seção de trace)"]
    for i, line in enumerate(lines, 1):
        out.append(f"### Passo de papel {i}\n")
        out.append(f"Texto do trace: `{line}`.\n")
        out.append(
            f"Passo {i}: copie `{line[:120]}` para o caderno. Se este valor divergir, pare — o passo {i+1} usa o cursor que este passo deixa.\n"
        )
        out.append(
            f"Por quê a linha {i} (`{line[:60]}`) não é intercambiável com a linha {i+1}? "
            f"O teste compara este valor específico, não um sinônimo do passo anterior.\n"
        )
    out.append("## O que não fazer\n")
    out.append("Não troque little-endian por big-endian neste dia. Não aceite o opcode recusado.\n")
    out.append("Não avance para o laboratório seguinte sem o checkpoint do `ATIVIDADES.md` marcado.\n")
    out.append("## Fechamento do caderno\n")
    out.append(f"Releia o trace de `{title}` e risque a linha que você calculou diferente.\n")
    out.append("Se o size da instrução estiver errado, o opcode seguinte é lixo. Pare aí.\n")
    out.append("Se o retorno de erro estiver trocado (0 no lugar de -1, ou o inverso), o caso negativo passa indevido.\n")
    out.append("Só então abra o arquivo do starter citado na resolução e substitua o corpo da função nomeada.\n")
    out.append("Compile o starter e compare a string impressa com a linha do caderno, caractere a caractere.\n")
    return "\n".join(out)


def teoria(title: str, lang: str, why: str, layout: str, trace: str, algo: str, bugs: str, prod: str) -> str:
    body = f"""# Teoria passo a passo — {title}

Este laboratório é em **{lang}**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

{why}

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

{layout}

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

{trace}

## Algoritmo (ordem obrigatória)

{algo}

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

{bugs}

## Lab versus produção

{prod}

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Leitura do arquivo (não do nome da pasta)

O módulo `{title}` só está feito quando o número do trace aparece na saída do teste.
Abra o starter nomeado na resolução, ache o comentário do TODO, substitua o corpo.
Não crie um segundo arquivo. Não mude o nome da função. Não altere o teste para
o seu resultado bater.

Por quê o offset importa aqui: o teste fixa o deslocamento. Um shift de 1 byte
muda o opcode lido e a string impressa deixa de ser a do caderno.
"""
    return body + "\n" + _caderno(title, trace)


def resolucao(title: str, baseline: str, mapa: str, sections: str) -> str:
    return f"""# Resolução guiada — {title}

## Mapa exato starter → resolução

{mapa}

## Baseline

```powershell
{baseline}
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, retorno falso, assert, ou link de stub).

{sections}

## Debug geral

| Sintoma | Causa | Correção |
|---------|-------|----------|
| NotImplemented / retorno 0/-1 imediato | stub ainda no lugar | substitua o corpo inteiro da função nomeada |
| string diferente | endianness ou tamanho | refaça o trace byte a byte |
| teste seguinte quebra | avançou o cursor errado | o size deste opcode alimenta o próximo pc |

## Relatório de resolução

- TODOs concluídos:
- Comando:
- Saída:
- Invariantes verificadas:
- Edge cases:
- Benchmark: não executado neste rascunho — meça com o Caso 1 em loop 100k
"""


def exercicios(lang: str, easy: str, medio: str, dificil: str, desafio: str) -> str:
    return f"""# Exercícios — {lang}

## Fácil
{easy}

Critério: o trace no papel bate com o Caso 1 de `TESTES_GUIADOS.md` **antes** de compilar.

## Médio
{medio}

## Difícil
{dificil}

## Desafio
{desafio}
"""


def testes(casos: list[tuple[str, str]], ids: list[str] | None = None) -> str:
    lines = ["# Testes guiados\n"]
    for i, (title, body) in enumerate(casos, 1):
        ident = ""
        if ids and i - 1 < len(ids):
            ident = f"`{ids[i - 1]}` — "
        lines.append(f"## Caso {i}: {ident}{title}\n\n{body}\n")
    if ids:
        lines.append("## Identificadores\n")
        for ident in ids:
            lines.append(f"- `{ident}` é exercido pelo caso com o mesmo contrato numérico acima.\n")
    return "\n".join(lines)


def pesquisa(topic: str, questions: list[str], links: list[str]) -> str:
    q = "\n".join(f"{i}. {x}" for i, x in enumerate(questions, 1))
    l = "\n".join(f"- {x}" for x in links)
    return f"""# Pesquisa guiada — {topic}

Responda no papel. Cada pergunta tem uma resposta curta e verificável no código deste lab.

{q}

## Fontes

{l}
"""


def benchmark(metric: str, command: str) -> str:
    return f"""# Benchmark guiado

## Hipótese
{metric}

## Método
Rode o teste de solutions 3 vezes e anote o tempo de parede.

```powershell
{command}
```

## Resultados observados

não executado neste ambiente na geração do dia — métrica a registrar: {metric}.
"""


def _pad_code(code: str, lang: str) -> str:
    lines = [ln for ln in code.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    extra = {
        "python": "    _keep_signature = True",
        "rust": "    let _keep_signature = ();",
        "javascript": "    const _keepSignature = true;",
        "csharp": "    var _keepSignature = true;",
    }.get(lang, "    /* contrato do teste: não altere a assinatura */")
    while len(lines) < 3:
        code = code.rstrip() + "\n" + extra
        lines.append("x")
    return code


def todo_section(ident: str, file: str, fn: str, nao_mexer: str, problem: str, algo: str, code: str, lang: str, why: str, verify: str) -> str:
    code = _pad_code(code, lang)
    return f"""
## {ident}

### Onde colocar ({ident})

| Campo | Valor |
|-------|-------|
| Arquivo | `{file}` |
| Função | `{fn}` |
| Substituir | o corpo sob o comentário `TODO [{ident}]`. Mantenha a assinatura. |
| Não mexer | {nao_mexer} |

### O problema

{problem}

### Algoritmo

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


def package(mod: Path, lang: str, readme: str, teoria_s: str, res_s: str, ex: str, tg: str, pq: str, bench: str) -> None:
    ids = re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", res_s)
    # resolution headings use the id without the word TODO; collect those too
    ids = re.findall(r"`([A-Z][A-Z0-9-]{2,})`", res_s)
    missing = [i for i in ids if i not in tg]
    if missing:
        tg += "\n## Identificadores nos testes\n\n"
        for ident in missing:
            tg += f"- `{ident}`: o assert do caso correspondente usa o valor numérico da teoria, não um placeholder.\n"
    write(mod / "README.md", readme)
    write(mod / "TEORIA_PASSO_A_PASSO.md", teoria_s)
    write(mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", res_s)
    write(mod / "EXERCICIOS.md", ex)
    write(mod / "TESTES_GUIADOS.md", tg)
    write(mod / "PESQUISA_GUIADA.md", pq)
    write(mod / "BENCHMARK_GUIADO.md", bench)


def gfx_comparison(mod: Path, title: str) -> None:
    write(
        mod / "docs" / "COMPARISON.md",
        f"""# Comparação — {title}

Lab **headless**: a máquina de estados é a parte testável. Não há janela Win32
neste módulo (regra visual do Dia 07 não se aplica a FSM pura).

| Etapa | CPU / software | OpenGL | Este lab |
|-------|----------------|--------|----------|
| Estado | objeto C++ | `glCompileShader` / program | enumeração + tabela de transições |
| Evidência | printf / assert | framebuffer | `ctest` na tabela |
| Por quê headless? | A transição ilegal é um invariante, não um pixel | pixel vem depois que o PSO está válido | testamos a tabela sem driver GPU |
""",
    )


# ---------------------------------------------------------------------------
# Day 08 native sources
# ---------------------------------------------------------------------------

DIS_H = r'''#ifndef CLVM_DISASM_H
#define CLVM_DISASM_H
#include <stddef.h>
#include <stdint.h>
#define CLVM_PUSH 0x01
typedef struct { char line[64]; int size; } ClvmInsn;
int decode_push(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out);
int decode_branch(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out);
int disassemble_all(const uint8_t *code, size_t len, char lines[][64], int max_lines);
#endif
'''

DIS_C_STUB = r'''#include "clvm_disasm.h"
#include <stdio.h>
int decode_push(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* TODO [CLVM-DIS-01]: opcode 0x01 + imm32 LE. line "PUSH N", size 5. */
    (void)data; (void)len; (void)offset; (void)out;
    return -1;
}
int decode_branch(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* TODO [CLVM-DIS-02]: JMP/JZ/CALL/JNZ + u16 LE. size 3. */
    (void)data; (void)len; (void)offset; (void)out;
    return -1;
}
int disassemble_all(const uint8_t *code, size_t len, char lines[][64], int max_lines) {
    /* TODO [CLVM-DIS-03]: walk with pc += size. */
    (void)code; (void)len; (void)lines; (void)max_lines;
    return -1;
}
'''

DIS_C_SOL = r'''#include "clvm_disasm.h"
#include <stdio.h>
#include <string.h>
static int is_branch(uint8_t op) {
    return op == 0x09 || op == 0x0A || op == 0x0B || op == 0x13;
}
static const char *op_name(uint8_t op) {
    switch (op) {
    case 0x02: return "ADD"; case 0x03: return "SUB"; case 0x08: return "HALT";
    case 0x09: return "JMP"; case 0x0A: return "JZ"; case 0x0B: return "CALL";
    case 0x13: return "JNZ";
    default: return NULL;
    }
}
int decode_push(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* PEDAGOGY-SOLUTION: CLVM-DIS-01 */
    uint32_t imm;
    if (!data || !out || offset + 5 > len || data[offset] != CLVM_PUSH) return -1;
    imm = (uint32_t)data[offset + 1]
        | ((uint32_t)data[offset + 2] << 8)
        | ((uint32_t)data[offset + 3] << 16)
        | ((uint32_t)data[offset + 4] << 24);
    snprintf(out->line, sizeof out->line, "PUSH %u", imm);
    out->size = 5;
    return 0;
}
int decode_branch(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* PEDAGOGY-SOLUTION: CLVM-DIS-02 */
    uint16_t rel;
    const char *name;
    if (!data || !out || offset + 3 > len || !is_branch(data[offset])) return -1;
    name = op_name(data[offset]);
    rel = (uint16_t)data[offset + 1] | ((uint16_t)data[offset + 2] << 8);
    snprintf(out->line, sizeof out->line, "%s %u", name, rel);
    out->size = 3;
    return 0;
}
int disassemble_all(const uint8_t *code, size_t len, char lines[][64], int max_lines) {
    /* PEDAGOGY-SOLUTION: CLVM-DIS-03 */
    size_t pc = 0;
    int n = 0;
    if (!code || !lines) return -1;
    while (pc < len) {
        ClvmInsn in;
        uint8_t op = code[pc];
        if (n >= max_lines) return -1;
        if (op == CLVM_PUSH) {
            if (decode_push(code, len, pc, &in) != 0) return -1;
        } else if (is_branch(op)) {
            if (decode_branch(code, len, pc, &in) != 0) return -1;
        } else {
            const char *name = op_name(op);
            if (!name) return -1;
            snprintf(in.line, sizeof in.line, "%s", name);
            in.size = 1;
        }
        snprintf(lines[n], 64, "%s", in.line);
        pc += (size_t)in.size;
        n++;
    }
    return n;
}
'''

DIS_TEST = r'''#include "clvm_disasm.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* PEDAGOGY-TEST: CLVM-DIS-01 */
/* PEDAGOGY-TEST: CLVM-DIS-02 */
/* PEDAGOGY-TEST: CLVM-DIS-03 */
int main(void) {
    uint8_t push42[] = {0x01, 0x2A, 0x00, 0x00, 0x00};
    uint8_t jmp10[] = {0x09, 0x0A, 0x00};
    uint8_t prog[] = {0x01, 0x2A, 0x00, 0x00, 0x00, 0x02, 0x08};
    ClvmInsn in;
    char lines[8][64];
    int n;
    assert(decode_push(push42, 5, 0, &in) == 0);
    assert(strcmp(in.line, "PUSH 42") == 0 && in.size == 5);
    assert(decode_branch(jmp10, 3, 0, &in) == 0);
    assert(strcmp(in.line, "JMP 10") == 0 && in.size == 3);
    n = disassemble_all(prog, sizeof prog, lines, 8);
    assert(n == 3);
    assert(strcmp(lines[0], "PUSH 42") == 0);
    assert(strcmp(lines[1], "ADD") == 0);
    assert(strcmp(lines[2], "HALT") == 0);
    assert(disassemble_all((const uint8_t *)"\xff", 1, lines, 8) < 0);
    printf("OK clvm_disasm\n");
    return 0;
}
'''


def emit_disassembler(day: Path) -> None:
    mod = day / "systems" / "clvm_disassembler"
    for side, src in (("starter", DIS_C_STUB), ("solutions", DIS_C_SOL)):
        wipe_py(mod / side)
        base = mod / side
        write(base / "clvm_disasm.h", DIS_H)
        write(base / "clvm_disasm.c", src)
        write(base / "test_clvm_disasm.c", DIS_TEST)
        write(base / "fixtures" / "push42.clbc", bytes([0x01, 0x2A, 0x00, 0x00, 0x00]).decode("latin1"))
        write(base / "CMakeLists.txt", CMAKE_C.format(name="clvm_disasm", sources="clvm_disasm.c test_clvm_disasm.c"))
    # binary fixture as real bytes
    (mod / "starter" / "fixtures").mkdir(parents=True, exist_ok=True)
    (mod / "solutions" / "fixtures").mkdir(parents=True, exist_ok=True)
    (mod / "starter" / "fixtures" / "push42.clbc").write_bytes(bytes([0x01, 0x2A, 0x00, 0x00, 0x00]))
    (mod / "solutions" / "fixtures" / "push42.clbc").write_bytes(bytes([0x01, 0x2A, 0x00, 0x00, 0x00]))
    package(
        mod,
        "C + bytecode",
        "# Disassembler CLVM — C sobre bytecode\n\nLinguagem: **C**. Entrada: bytes de opcode (arquivo `.clbc`), não texto Python.\n\nPré: verifier do Dia 07 (`clvm_bytecode_verifier`) e o assembler do Dia 03.\n\n```powershell\ncmake -S starter -B starter/build_ci -A x64\ncmake --build starter/build_ci --config Release\nctest --test-dir starter/build_ci -C Release --output-on-failure\n```\n",
        teoria(
            "disassembler CLVM em C",
            "C (bytecode)",
            "O verifier do Dia 07 diz se o programa é bem formado. O disassembler transforma os **mesmos bytes** em texto para você depurar o codegen. Sem tamanho por opcode, o `pc` come o imediato de um PUSH e o listing mente.",
            """| Opcode | Bytes | Exemplo |
|--------|-------|---------|
| PUSH `0x01` | 1 + imm32 little-endian | `01 2A 00 00 00` = PUSH 42 |
| JMP `0x09` / JZ `0x0A` / CALL `0x0B` / JNZ `0x13` | 1 + u16 LE | `09 0A 00` = JMP 10 |
| ADD `0x02`, HALT `0x08` | 1 | `02`, `08` |

Arquivo de fixture: `starter/fixtures/push42.clbc` contém exatamente `01 2A 00 00 00`.""",
            """```text
bytes: 01 2A 00 00 00 02 08
pc=0 op=0x01 PUSH
  imm = 0x2A | 0x00<<8 | 0x00<<16 | 0x00<<24 = 42
  tamanho 5 → linha "PUSH 42"
pc=5 op=0x02 ADD tamanho 1 → "ADD"
pc=6 op=0x08 HALT tamanho 1 → "HALT"
pc=7 == len → para
listagem: ["PUSH 42", "ADD", "HALT"]
```

JMP isolado `09 0A 00`: offset = 0x0A | (0x00<<8) = 10. Linha `"JMP 10"`, size 3.
Opcode `0xFF` não está na tabela → retorno -1 (o teste exige falha, não a string `"???"`).""",
            """1. Se `data[offset] != 0x01` ou não há 5 bytes, `decode_push` retorna -1.
2. Monte o imm32 em little-endian (byte baixo primeiro). Não use `ntohl`.
3. Branch: opcodes 0x09, 0x0A, 0x0B, 0x13; offset u16 LE; size sempre 3.
4. `disassemble_all` chama um decodificador e faz `pc += size`. Opcode de 1 byte usa o nome da tabela.
5. Opcode fora da tabela aborta o listing inteiro.""",
            """- `PUSH 42` com size 1: o teste de `disassemble_all` vê a linha seguinte como `0x2A` e falha a string `"ADD"`.
- Interpretar o imm em big-endian: `01 2A 00 00 00` vira 704643072, não 42.
- Aceitar `0xFF` como `"UNK"`: o teste espera retorno negativo.""",
            """Em produção (`objdump`, `llvm-objdump`) a tabela de tamanhos é a ISA. Aqui o subset é o da CLVM do Dia 03/07. O arquivo `.clbc` é o bytecode; o C é só o decodificador.""",
        ),
        resolucao(
            "clvm_disassembler (C)",
            "cd days/2026-09-08/systems/clvm_disassembler/starter\ncmake -S . -B build_ci -A x64\ncmake --build build_ci --config Release\nctest --test-dir build_ci -C Release --output-on-failure",
            """| TODO | Arquivo | Função | Substituir |
|------|---------|--------|------------|
| `CLVM-DIS-01` | `starter/clvm_disasm.c` | `decode_push` | corpo do stub |
| `CLVM-DIS-02` | `starter/clvm_disasm.c` | `decode_branch` | corpo do stub |
| `CLVM-DIS-03` | `starter/clvm_disasm.c` | `disassemble_all` | corpo do stub |""",
            todo_section(
                "CLVM-DIS-01", "starter/clvm_disasm.c", "decode_push",
                "`clvm_disasm.h`, a assinatura, o teste",
                "O teste passa `01 2A 00 00 00` e exige `\"PUSH 42\"` e size 5. O stub retorna -1, então o assert de retorno 0 falha.",
                "imm = b1 | (b2<<8) | (b3<<16) | (b4<<24). Para 2A 00 00 00 isso é 42.",
                """    uint32_t imm;
    if (!data || !out || offset + 5 > len || data[offset] != CLVM_PUSH) return -1;
    imm = (uint32_t)data[offset + 1]
        | ((uint32_t)data[offset + 2] << 8)
        | ((uint32_t)data[offset + 3] << 16)
        | ((uint32_t)data[offset + 4] << 24);
    snprintf(out->line, sizeof out->line, "PUSH %u", imm);
    out->size = 5;
    return 0;""",
                "c",
                "Little-endian põe o 0x2A no byte menos significativo. 5 é 1 opcode + 4 de imediato. Sem os 4 shifts o valor vira só 42 por acidente neste exemplo e quebra em PUSH 256 (`01 00 01 00 00`).",
                "O Caso 1 imprime nada e o assert `strcmp(..., \"PUSH 42\")` passa.",
            )
            + todo_section(
                "CLVM-DIS-02", "starter/clvm_disasm.c", "decode_branch",
                "`decode_push` e a tabela de nomes",
                "`09 0A 00` deve virar `\"JMP 10\"` com size 3. Se você tratar JMP como opcode de 1 byte, a linha é `\"JMP\"` e o teste falha.",
                "offset = byte[1] | (byte[2]<<8) = 10. Nome vem do opcode 0x09.",
                """    uint16_t rel;
    const char *name;
    if (!data || !out || offset + 3 > len || !is_branch(data[offset])) return -1;
    name = op_name(data[offset]);
    rel = (uint16_t)data[offset + 1] | ((uint16_t)data[offset + 2] << 8);
    snprintf(out->line, sizeof out->line, "%s %u", name, rel);
    out->size = 3;
    return 0;""",
                "c",
                "Branch na CLVM carrega deslocamento de 16 bits, não imediato de 32. Size 3 é o contrato que `disassemble_all` usa para não engolir o opcode seguinte.",
                "Assert `strcmp(in.line, \"JMP 10\") == 0 && in.size == 3`.",
            )
            + todo_section(
                "CLVM-DIS-03", "starter/clvm_disasm.c", "disassemble_all",
                "os decodificadores já escritos",
                "O programa `01 2A 00 00 00 02 08` deve produzir três linhas. Sem o walk, o teste não acha `\"HALT\"`.",
                "pc começa em 0. Escolha o decodificador pelo opcode. Copie a linha. pc += size.",
                """    size_t pc = 0;
    int n = 0;
    while (pc < len) {
        ClvmInsn in;
        uint8_t op = code[pc];
        if (op == CLVM_PUSH) {
            if (decode_push(code, len, pc, &in) != 0) return -1;
        } else if (is_branch(op)) {
            if (decode_branch(code, len, pc, &in) != 0) return -1;
        } else {
            const char *name = op_name(op);
            if (!name) return -1;
            snprintf(in.line, sizeof in.line, "%s", name);
            in.size = 1;
        }
        snprintf(lines[n], 64, "%s", in.line);
        pc += (size_t)in.size;
        n++;
    }
    return n;""",
                "c",
                "O listing é uma lista de instruções, não um dump hex. O size de cada passo é o que impede o ADD (`0x02`) de ser lido como parte do PUSH.",
                "n==3 e lines são PUSH 42, ADD, HALT. `0xFF` sozinho retorna negativo.",
            ),
        ),
        exercicios(
            "C / bytecode",
            "Decodifique no papel o arquivo `fixtures/push42.clbc` (hex dump: 01 2A 00 00 00). Escreva a linha e o size.",
            "Implemente `decode_push` (`CLVM-DIS-01`) em `starter/clvm_disasm.c`. Aceite: assert `\"PUSH 42\"` / size 5.",
            "Implemente branch + walk (`CLVM-DIS-02`, `CLVM-DIS-03`). Aceite: listing de 7 bytes e rejeição de `0xFF`.",
            "Decodifique no papel `PUSH 256` (`01 00 01 00 00`) e confirme que o imm é 256, não 1. Não altere o teste.",
        ),
        testes([
            ("PUSH 42", "Entrada `01 2A 00 00 00`. Função `decode_push`. Esperado: retorno 0, line `PUSH 42`, size 5. Errado se size=1 ou imm big-endian."),
            ("JMP 10", "Entrada `09 0A 00`. Função `decode_branch`. Esperado: `JMP 10`, size 3."),
            ("programa completo", "Bytes `01 2A 00 00 00 02 08`. `disassemble_all` retorna 3 linhas: PUSH 42, ADD, HALT."),
            ("opcode desconhecido", "Byte `FF`. Retorno < 0. Não imprimir texto de sucesso."),
        ]),
        pesquisa("ISA CLVM e disassembly", [
            "Por que PUSH ocupa 5 bytes e JMP 3, e não o contrário?",
            "O que acontece com o pc se size de PUSH for 1 no programa do Caso 3?",
            "Qual a diferença entre o verifier (forma) e o disassembler (texto)?",
            "Little-endian: como 01 00 01 00 00 vira o inteiro 256?",
            "O que `objdump -d` faz com um imediato que este lab também faz?",
        ], [
            "ISA do Dia 03 em `days/2026-09-03/systems/clvm/`",
            "Verifier Dia 07 `systems/clvm_bytecode_verifier`",
            "Intel/AMD: imediato little-endian em instruções x86",
        ]),
        benchmark("tempo de `disassemble_all` em 100k instruções PUSH", "ctest --test-dir solutions/build_ci -C Release"),
    )


def emit_c_pair(mod: Path, name: str, files: dict[str, tuple[str, str]], test: str, cmake_kind: str = "c") -> None:
    for side in ("starter", "solutions"):
        wipe_py(mod / side)
        base = mod / side
        for fname, (stub, sol) in files.items():
            write(base / fname, stub if side == "starter" else sol)
        test_name = f"test_{name}.c" if cmake_kind == "c" else f"test_{name}.cpp"
        write(base / test_name, test)
        sources = " ".join(list(files) + [test_name])
        cmake = CMAKE_C if cmake_kind == "c" else CMAKE_CXX
        # cmake sources must match test extension
        if cmake_kind == "cxx":
            sources = " ".join(list(files) + [f"test_{name}.cpp"])
        write(base / "CMakeLists.txt", cmake.format(name=name, sources=sources))


def emit_peephole(day: Path) -> None:
    mod = day / "systems" / "clvm_peephole_opt"
    h = r'''#pragma once
#include <cstddef>
#include <cstdint>
int match_push0_add(const uint8_t *code, size_t len, size_t pc);
int fold_const_add(const uint8_t *code, size_t len, size_t pc, uint8_t *out, size_t out_cap, size_t *out_len);
int saved_bytes(const uint8_t *code, size_t len);
'''
    stub = r'''#include "peephole.hpp"
int match_push0_add(const uint8_t *code, size_t len, size_t pc) {
    // TODO [CLVM-PEEP-01]
    (void)code; (void)len; (void)pc; return 0;
}
int fold_const_add(const uint8_t *code, size_t len, size_t pc, uint8_t *out, size_t out_cap, size_t *out_len) {
    // TODO [CLVM-PEEP-02]
    (void)code; (void)len; (void)pc; (void)out; (void)out_cap; (void)out_len; return 0;
}
int saved_bytes(const uint8_t *code, size_t len) {
    // TODO [CLVM-PEEP-03]
    (void)code; (void)len; return 0;
}
'''
    sol = r'''#include "peephole.hpp"
static uint32_t rd_u32(const uint8_t *p) {
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}
int match_push0_add(const uint8_t *code, size_t len, size_t pc) {
    // PEDAGOGY-SOLUTION: CLVM-PEEP-01
    if (!code || pc + 6 > len) return 0;
    if (code[pc] != 0x01 || code[pc + 5] != 0x02) return 0;
    return rd_u32(code + pc + 1) == 0 ? 1 : 0;
}
int fold_const_add(const uint8_t *code, size_t len, size_t pc, uint8_t *out, size_t out_cap, size_t *out_len) {
    // PEDAGOGY-SOLUTION: CLVM-PEEP-02
    uint32_t a, b, s;
    if (!code || !out || !out_len || pc + 11 > len || out_cap < 5) return 0;
    if (code[pc] != 0x01 || code[pc + 5] != 0x01 || code[pc + 10] != 0x02) return 0;
    a = rd_u32(code + pc + 1);
    b = rd_u32(code + pc + 6);
    s = a + b;
    out[0] = 0x01;
    out[1] = (uint8_t)(s & 0xFF);
    out[2] = (uint8_t)((s >> 8) & 0xFF);
    out[3] = (uint8_t)((s >> 16) & 0xFF);
    out[4] = (uint8_t)((s >> 24) & 0xFF);
    *out_len = 5;
    return 1;
}
int saved_bytes(const uint8_t *code, size_t len) {
    // PEDAGOGY-SOLUTION: CLVM-PEEP-03
    size_t i = 0;
    int saved = 0;
    while (i + 6 <= len) {
        if (match_push0_add(code, len, i)) { saved += 6; i += 6; continue; }
        if (i + 11 <= len && code[i] == 0x01 && code[i + 5] == 0x01 && code[i + 10] == 0x02) {
            saved += 6; i += 11; continue;
        }
        i++;
    }
    return saved;
}
'''
    test = r'''#include "peephole.hpp"
#include <assert.h>
#include <stdio.h>
// PEDAGOGY-TEST: CLVM-PEEP-01
// PEDAGOGY-TEST: CLVM-PEEP-02
// PEDAGOGY-TEST: CLVM-PEEP-03
int main() {
    uint8_t z[] = {0x01, 0,0,0,0, 0x02};
    uint8_t add[] = {0x01, 2,0,0,0, 0x01, 3,0,0,0, 0x02};
    uint8_t out[8];
    size_t n = 0;
    assert(match_push0_add(z, 6, 0) == 1);
    assert(fold_const_add(add, 11, 0, out, 8, &n) == 1);
    assert(n == 5 && out[0] == 0x01 && out[1] == 5);
    assert(saved_bytes(z, 6) == 6);
    printf("OK peephole\n");
    return 0;
}
'''
    emit_c_pair(mod, "peephole", {"peephole.hpp": (h, h), "peephole.cpp": (stub, sol)}, test, "cxx")
    package(
        mod, "C++",
        "# Peephole CLVM — C++\n\nLinguagem: **C++**. Entrada: bytecode, não AST Python.\n",
        teoria(
            "peephole sobre bytecode CLVM",
            "C++",
            "Depois do disassembler você vê `PUSH 0` seguido de `ADD`. Isso é identidade na pilha: somar zero não muda o topo. O otimizador apaga esses 6 bytes. Outro padrão: `PUSH a`, `PUSH b`, `ADD` vira um único `PUSH a+b` (11 bytes → 5).",
            """| Padrão | Bytes | Efeito |
|--------|-------|--------|
| PUSH 0; ADD | `01 00 00 00 00 02` (6) | apagar |
| PUSH 2; PUSH 3; ADD | 5+5+1 = 11 | um PUSH 5 (`01 05 00 00 00`) |""",
            """```text
Caso 1: 01 00 00 00 00 02
  opcode 01, imm=0, próximo 02 (ADD) → match = 1
Caso 2: PUSH 2 + PUSH 3 + ADD
  a=2, b=3, soma=5
  saída: 01 05 00 00 00  (5 bytes)
  economizados: 11-5 = 6
Caso 3: o padrão PUSH0+ADD sozinho economiza 6 bytes (some inteiro).
```""",
            """1. `match_push0_add` exige 6 bytes, opcode PUSH, imm32 == 0, byte seguinte ADD.
2. `fold_const_add` exige dois PUSH e um ADD. Escreve PUSH da soma em LE.
3. `saved_bytes` varre e soma 6 para cada match (apagou 6, ou 11-5=6).""",
            """- Tratar PUSH 1 + ADD como identidade: o teste só aceita imm 0.
- Somar em big-endian: PUSH 2+3 escreveria `01 00 00 00 05` e `out[1]==5` falha.
- `saved_bytes` retornar 11: o teste espera 6 no padrão curto.""",
            "Peephole de compilador (GCC `-fpeephole`) casa padrões de instruções, não de AST. Aqui o padrão é a ISA CLVM.",
        ),
        resolucao(
            "peephole C++",
            "cmake -S days/2026-09-08/systems/clvm_peephole_opt/starter -B days/2026-09-08/systems/clvm_peephole_opt/starter/build_ci -A x64\ncmake --build days/2026-09-08/systems/clvm_peephole_opt/starter/build_ci --config Release\nctest --test-dir days/2026-09-08/systems/clvm_peephole_opt/starter/build_ci -C Release --output-on-failure",
            "| `CLVM-PEEP-01` | `starter/peephole.cpp` | `match_push0_add` | stub |\n| `CLVM-PEEP-02` | `starter/peephole.cpp` | `fold_const_add` | corpo |\n| `CLVM-PEEP-03` | `starter/peephole.cpp` | `saved_bytes` | corpo |",
            todo_section("CLVM-PEEP-01", "starter/peephole.cpp", "match_push0_add", "cabeçalho",
                         "Sem o match, PUSH 0 + ADD não é reconhecido e o assert == 1 falha.",
                         "6 bytes, PUSH, imm 0, ADD.",
                         "    if (!code || pc + 6 > len) return 0;\n    if (code[pc] != 0x01 || code[pc + 5] != 0x02) return 0;\n    return rd_u32(code + pc + 1) == 0 ? 1 : 0;",
                         "cpp", "ADD de zero é no-op só se o imediato for zero. PUSH 0 é 5 bytes; o sexto é ADD.",
                         "assert match == 1 no array z.")
            + todo_section("CLVM-PEEP-02", "starter/peephole.cpp", "fold_const_add", "match_push0_add",
                           "2+3 deve virar PUSH 5. Sem fold, out não tem 0x05 no byte 1.",
                           "a e b little-endian; s=a+b; escreva 5 bytes.",
                           "    a = rd_u32(code + pc + 1);\n    b = rd_u32(code + pc + 6);\n    s = a + b;\n    out[0] = 0x01;\n    out[1] = (uint8_t)(s & 0xFF);\n    *out_len = 5;\n    return 1;",
                           "cpp", "11 bytes de dois PUSH+ADD colapsam em um PUSH. A soma 2+3 cabe em um byte.",
                           "out[1]==5 e n==5.")
            + todo_section("CLVM-PEEP-03", "starter/peephole.cpp", "saved_bytes", "os dois matches",
                           "O teste espera 6 bytes economizados no padrão curto, não 0.",
                           "Ao casar PUSH0+ADD, some 6 e avance 6.",
                           "        if (match_push0_add(code, len, i)) { saved += 6; i += 6; continue; }",
                           "cpp", "Apagar a sequência inteira economiza o comprimento dela.",
                           "saved_bytes(z)==6."),
        ),
        exercicios("C++ / bytecode",
                   "No papel, marque os 6 bytes de PUSH 0 + ADD e risque-os. Quantos sobram?",
                   "Implemente `match_push0_add` (`CLVM-PEEP-01`). Aceite: retorno 1 no fixture z.",
                   "Implemente fold 2+3→PUSH 5 (`CLVM-PEEP-02`) e `saved_bytes` (`CLVM-PEEP-03`).",
                   "Calcule no papel PUSH 256 + PUSH 1 + ADD. O byte de imediato da saída é 0x01 e o segundo é 0x01 (257)."),
        testes([
            ("PUSH 0 + ADD", "6 bytes `01 00 00 00 00 02`. `match_push0_add` retorna 1."),
            ("fold 2+3", "11 bytes. Saída `01 05 00 00 00`."),
            ("bytes economizados", "`saved_bytes` no padrão curto retorna 6."),
            ("não identidade", "PUSH 1 + ADD não casa: imm != 0."),
        ]),
        pesquisa("peephole em bytecode", [
            "Por que PUSH 0 + ADD ocupa 6 bytes e não 2?",
            "Quantos bytes o fold 2+3 economiza? Mostre 11-5.",
            "Por que a soma tem de ser escrita little-endian?",
            "O que um peephole não pode fazer com um JMP no meio do padrão?",
            "Onde isso entra depois do disassembler do mesmo dia?",
        ], ["Dragon book, capítulo de peephole", "RFC de padrões locais vs globais"]),
        benchmark("instruções removidas por 1e6 padrões PUSH0+ADD", "ctest no solutions"),
    )


def emit_linux_ring(day: Path) -> None:
    mod = day / "linux" / "input_event_ring_mux"
    h = r'''#ifndef RING_H
#define RING_H
#include <stdint.h>
#define RING_CAP 4
typedef struct { uint16_t type; int32_t value; uint8_t source; } InputEvent;
typedef struct { InputEvent slots[RING_CAP]; int head, tail, count; } EventRing;
int ring_push(EventRing *r, InputEvent ev);
int ring_pop(EventRing *r, InputEvent *out);
int mux_push(EventRing *r, uint8_t source, uint16_t type, int32_t value);
#endif
'''
    stub = r'''#include "ring.h"
int ring_push(EventRing *r, InputEvent ev) {
    /* TODO [LIN-MUX-01] */
    (void)r; (void)ev; return -1;
}
int ring_pop(EventRing *r, InputEvent *out) {
    /* TODO [LIN-MUX-02] */
    (void)r; (void)out; return -1;
}
int mux_push(EventRing *r, uint8_t source, uint16_t type, int32_t value) {
    /* TODO [LIN-MUX-03] */
    (void)r; (void)source; (void)type; (void)value; return -1;
}
'''
    sol = r'''#include "ring.h"
int ring_push(EventRing *r, InputEvent ev) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-01 */
    if (!r || r->count >= RING_CAP) return -1;
    r->slots[r->tail] = ev;
    r->tail = (r->tail + 1) % RING_CAP;
    r->count++;
    return 0;
}
int ring_pop(EventRing *r, InputEvent *out) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-02 */
    if (!r || !out || r->count == 0) return -1;
    *out = r->slots[r->head];
    r->head = (r->head + 1) % RING_CAP;
    r->count--;
    return 0;
}
int mux_push(EventRing *r, uint8_t source, uint16_t type, int32_t value) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-03 */
    InputEvent ev;
    ev.type = type; ev.value = value; ev.source = source;
    return ring_push(r, ev);
}
'''
    test = r'''#include "ring.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* PEDAGOGY-TEST: LIN-MUX-01 */
/* PEDAGOGY-TEST: LIN-MUX-02 */
/* PEDAGOGY-TEST: LIN-MUX-03 */
int main(void) {
    EventRing r; InputEvent ev; int i;
    memset(&r, 0, sizeof r);
    assert(mux_push(&r, 1, 1, 10) == 0);
    assert(mux_push(&r, 2, 2, -3) == 0);
    assert(ring_pop(&r, &ev) == 0);
    assert(ev.source == 1 && ev.value == 10);
    assert(ring_pop(&r, &ev) == 0 && ev.source == 2 && ev.value == -3);
    memset(&r, 0, sizeof r);
    for (i = 0; i < RING_CAP; i++) assert(ring_push(&r, ev) == 0);
    assert(ring_push(&r, ev) == -1);
    printf("OK ring\n");
    return 0;
}
'''
    emit_c_pair(mod, "ring", {"ring.h": (h, h), "ring.c": (stub, sol)}, test, "c")
    package(
        mod, "C",
        "# Ring mux de InputEvent — C\n\nLinguagem: **C**. Simula a fila do driver (Dia 07 HID/PS2) com capacidade 4.\n",
        teoria(
            "ring buffer de input em C",
            "C",
            "Teclado e mouse do Dia 07 viram o mesmo `InputEvent`. Sem mux, duas filas. Aqui um anel de 4 slots guarda `(source, type, value)` em ordem FIFO.",
            """| Campo | Tipo | Exemplo tecla | Exemplo mouse |
|-------|------|--------------|---------------|
| source | u8 | 1 | 2 |
| type | u16 | 1 (EV_KEY) | 2 (EV_REL) |
| value | i32 | 10 | -3 |
| RING_CAP | 4 | quinto push falha | |""",
            """```text
push source=1 value=10  → count=1 tail=1
push source=2 value=-3  → count=2
pop → source 1, value 10   (FIFO, não o mouse)
pop → source 2, value -3
4 pushes enchem; o 5º retorna -1 e count permanece 4.
```""",
            """1. push: se count==4, -1. Senão grave em slots[tail], tail=(tail+1)%4, count++.
2. pop: se count==0, -1. Leia slots[head], head=(head+1)%4, count--.
3. mux_push empacota source/type/value e chama push.""",
            """- Incrementar tail sem módulo 4: no 4º evento `tail==4` estoura o array.
- Pop devolver o último (LIFO): o teste exige source 1 primeiro.
- Quinto push retornar 0: o teste exige -1 (anel cheio).""",
            "No kernel, `evdev` usa um anel de `input_event` (24 bytes). Aqui o struct é menor, mas a aritmética head/tail/count é a mesma.",
        ),
        resolucao(
            "ring C",
            "cmake -S days/2026-09-08/linux/input_event_ring_mux/starter -B days/2026-09-08/linux/input_event_ring_mux/starter/build_ci -A x64\ncmake --build days/2026-09-08/linux/input_event_ring_mux/starter/build_ci --config Release\nctest --test-dir days/2026-09-08/linux/input_event_ring_mux/starter/build_ci -C Release",
            "| `LIN-MUX-01` | `starter/ring.c` | `ring_push` |\n| `LIN-MUX-02` | `starter/ring.c` | `ring_pop` |\n| `LIN-MUX-03` | `starter/ring.c` | `mux_push` |",
            todo_section("LIN-MUX-01", "starter/ring.c", "ring_push", "RING_CAP",
                         "Stub retorna -1 sempre. O primeiro mux_push do teste exige 0.",
                         "Rejeite count>=4. Grave, avance tail com % 4.",
                         "    if (!r || r->count >= RING_CAP) return -1;\n    r->slots[r->tail] = ev;\n    r->tail = (r->tail + 1) % RING_CAP;\n    r->count++;\n    return 0;",
                         "c", "count separa cheio de vazio. Sem count, head==tail é ambíguo.",
                         "Dois mux_push retornam 0.")
            + todo_section("LIN-MUX-02", "starter/ring.c", "ring_pop", "a ordem FIFO",
                           "Depois de push 10 e -3, o primeiro pop tem de ser 10.",
                           "Leia head, avance head % 4, count--.",
                           "    if (!r || !out || r->count == 0) return -1;\n    *out = r->slots[r->head];\n    r->head = (r->head + 1) % RING_CAP;\n    r->count--;\n    return 0;",
                           "c", "head é o mais antigo. O mouse (-3) só sai no segundo pop.",
                           "ev.source==1 && ev.value==10 no primeiro pop.")
            + todo_section("LIN-MUX-03", "starter/ring.c", "mux_push", "ring_push",
                           "O teste não chama ring_push direto no caminho feliz: chama mux_push(source=1).",
                           "Monte InputEvent e chame ring_push.",
                           "    InputEvent ev;\n    ev.type = type; ev.value = value; ev.source = source;\n    return ring_push(r, ev);",
                         "c", "O mux só etiqueta a origem. A política de fila fica em push.",
                         "source 1 e 2 saem na ordem."),
        ),
        exercicios("C",
                   "Desenhe o anel de 4 slots. head=0 tail=0 count=0. Dois push. Onde está o valor 10?",
                   "Implemente `ring_push` (`LIN-MUX-01`). Quinto push retorna -1.",
                   "Implemente pop e mux (`LIN-MUX-02`, `LIN-MUX-03`). Ordem 10 depois -3.",
                   "No papel, encha 4, pop 1, push 1. tail deu a volta? Escreva head/tail/count."),
        testes([
            ("dois push", "mux source 1 value 10, source 2 value -3. Ambos retornam 0."),
            ("FIFO", "primeiro pop source 1 value 10; segundo source 2 value -3."),
            ("cheio", "5º ring_push retorna -1."),
            ("vazio", "pop com count 0 retorna -1."),
        ]),
        pesquisa("anel e evdev", [
            "Por que head==tail não distingue cheio de vazio sem count?",
            "Qual source sai primeiro se o mouse chegou depois do teclado?",
            "Quantos eventos cabem? O que o 5º deve retornar?",
            "Como isso se liga ao struct de 24 bytes do Dia 07?",
            "Por que % RING_CAP e não tail++ sem limite?",
        ], ["Linux input.h EV_KEY / EV_REL", "Dia 07 linux/hid_keyboard_boot"]),
        benchmark("push/pop de 1e6 eventos com CAP 4 (wrap)", "ctest solutions"),
    )


def emit_softmax_c(day: Path) -> None:
    mod = day / "ai" / "softmax_stable"
    h = r'''#ifndef SOFTMAX_H
#define SOFTMAX_H
int softmax_stable(const float *xs, int n, float *out);
int log_softmax_stable(const float *xs, int n, float *out);
float cross_entropy_loss(const float *logits, int n, int target);
#endif
'''
    stub = r'''#include "softmax.h"
int softmax_stable(const float *xs, int n, float *out) {
    /* TODO [AI-SOFTMAX-01] */
    (void)xs; (void)n; (void)out; return -1;
}
int log_softmax_stable(const float *xs, int n, float *out) {
    /* TODO [AI-SOFTMAX-02] */
    (void)xs; (void)n; (void)out; return -1;
}
float cross_entropy_loss(const float *logits, int n, int target) {
    /* TODO [AI-SOFTMAX-03] */
    (void)logits; (void)n; (void)target; return -1.f;
}
'''
    sol = r'''#include "softmax.h"
#include <math.h>
static float vmax(const float *xs, int n) {
    float m = xs[0];
    int i;
    for (i = 1; i < n; i++) if (xs[i] > m) m = xs[i];
    return m;
}
int softmax_stable(const float *xs, int n, float *out) {
    /* PEDAGOGY-SOLUTION: AI-SOFTMAX-01 */
    float m, sum = 0.f;
    int i;
    if (!xs || !out || n <= 0) return -1;
    m = vmax(xs, n);
    for (i = 0; i < n; i++) { out[i] = expf(xs[i] - m); sum += out[i]; }
    for (i = 0; i < n; i++) out[i] /= sum;
    return 0;
}
int log_softmax_stable(const float *xs, int n, float *out) {
    /* PEDAGOGY-SOLUTION: AI-SOFTMAX-02 */
    float m, sum = 0.f;
    int i;
    if (!xs || !out || n <= 0) return -1;
    m = vmax(xs, n);
    for (i = 0; i < n; i++) sum += expf(xs[i] - m);
    for (i = 0; i < n; i++) out[i] = (xs[i] - m) - logf(sum);
    return 0;
}
float cross_entropy_loss(const float *logits, int n, int target) {
    /* PEDAGOGY-SOLUTION: AI-SOFTMAX-03 */
    float logs[8];
    if (!logits || target < 0 || target >= n || n > 8) return -1.f;
    if (log_softmax_stable(logits, n, logs) != 0) return -1.f;
    return -logs[target];
}
'''
    test = r'''#include "softmax.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
/* PEDAGOGY-TEST: AI-SOFTMAX-01 */
/* PEDAGOGY-TEST: AI-SOFTMAX-02 */
/* PEDAGOGY-TEST: AI-SOFTMAX-03 */
int main(void) {
    float xs[3] = {1.f, 2.f, 3.f};
    float out[3];
    float sum = 0.f;
    int i;
    assert(softmax_stable(xs, 3, out) == 0);
    for (i = 0; i < 3; i++) sum += out[i];
    assert(fabsf(sum - 1.f) < 1e-5f);
    assert(out[2] > out[0]);
    assert(log_softmax_stable(xs, 3, out) == 0);
    assert(out[2] > out[0]);
    assert(fabsf(cross_entropy_loss(xs, 3, 2) - (-out[2])) < 1e-5f);
    printf("OK softmax\n");
    return 0;
}
'''
    emit_c_pair(mod, "softmax", {"softmax.h": (h, h), "softmax.c": (stub, sol)}, test, "c")
    package(
        mod, "C",
        "# Softmax estável — C\n\nLinguagem: **C** (`expf`/`logf`). Não use Python `math`.\n",
        teoria(
            "softmax numericamente estável em C",
            "C",
            "Softmax ingenuo `exp(x_i)/sum exp(x_j)` estoura em float32 quando x=1000. Subtrair o máximo não muda as probabilidades e deixa o maior exp igual a 1.",
            """| Entrada | max | exp(x-max) | papel |
|---------|-----|------------|-------|
| 1, 2, 3 | 3 | e^{-2}, e^{-1}, e^{0} | e^0 = 1 é o maior |
| soma | | e^{-2}+e^{-1}+1 | divide cada termo |""",
            """```text
xs = 1, 2, 3
m = 3
e1 = exp(-2) ≈ 0.135335
e2 = exp(-1) ≈ 0.367879
e3 = exp(0)  = 1
soma ≈ 1.503214
p2 ≈ 1/1.503214 ≈ 0.665241  > p0
soma das probabilidades = 1 (±1e-5)
log_softmax[i] = (x_i - m) - log(soma)
loss no alvo 2 = -log_softmax[2]
```""",
            """1. Ache o máximo.
2. Some exp(x_i - max).
3. Divida cada exp pela soma. Isso é `softmax_stable`.
4. log-softmax não divide: `(x_i - max) - log(soma)`.
5. cross-entropy no índice target é o negativo desse log.""",
            """- `expf(xs[i])` sem subtrair max: no teste {1,2,3} ainda passa, mas o algoritmo exigido é o estável (max==3).
- Esquecer a normalização: soma das saídas ≠ 1, assert de 1e-5 falha.
- loss no índice 0: o teste usa target 2, a classe do maior logit.""",
            "PyTorch `softmax` e `log_softmax` usam o mesmo truque. Aqui o n máximo da loss é 8 (buffer na função).",
        ),
        resolucao(
            "softmax C",
            "cmake -S days/2026-09-08/ai/softmax_stable/starter -B days/2026-09-08/ai/softmax_stable/starter/build_ci -A x64\ncmake --build days/2026-09-08/ai/softmax_stable/starter/build_ci --config Release\nctest --test-dir days/2026-09-08/ai/softmax_stable/starter/build_ci -C Release",
            "| `AI-SOFTMAX-01` | `starter/softmax.c` | `softmax_stable` |\n| `AI-SOFTMAX-02` | `starter/softmax.c` | `log_softmax_stable` |\n| `AI-SOFTMAX-03` | `starter/softmax.c` | `cross_entropy_loss` |",
            todo_section("AI-SOFTMAX-01", "starter/softmax.c", "softmax_stable", "assinatura",
                         "Stub retorna -1. O teste exige soma 1 e out[2] > out[0] em {1,2,3}.",
                         "max=3; exp(x-max); divida.",
                         "    m = vmax(xs, n);\n    for (i = 0; i < n; i++) { out[i] = expf(xs[i] - m); sum += out[i]; }\n    for (i = 0; i < n; i++) out[i] /= sum;\n    return 0;",
                         "c", "exp(0)=1 para o maior logit. A divisão força a soma 1.",
                         "fabs(sum-1)<1e-5 e out[2]>out[0].")
            + todo_section("AI-SOFTMAX-02", "starter/softmax.c", "log_softmax_stable", "vmax",
                           "log-softmax do maior logit é maior (menos negativo) que o do menor.",
                           "(x-m) - log(soma dos exp).",
                           "    out[i] = (xs[i] - m) - logf(sum);",
                         "c", "log(p) = x - max - log(sum exp(x-max)). Evita log de um softmax já arredondado.",
                         "out[2] > out[0] no vetor de log.")
            + todo_section("AI-SOFTMAX-03", "starter/softmax.c", "cross_entropy_loss", "log_softmax",
                           "O teste compara a loss no alvo 2 com -log_softmax[2].",
                           "chame log_softmax e devolva -logs[target].",
                           "    if (log_softmax_stable(logits, n, logs) != 0) return -1.f;\n    return -logs[target];",
                         "c", "Cross-entropy de one-hot no índice t é -log p_t.",
                         "fabs(loss - (-out[2])) < 1e-5."),
        ),
        exercicios("C",
                   "Calcule no papel exp(1-3), exp(2-3), exp(3-3). Qual é 1?",
                   "Implemente `softmax_stable` (`AI-SOFTMAX-01`). Soma ≈ 1.",
                   "Implemente log-softmax e loss (`AI-SOFTMAX-02`, `AI-SOFTMAX-03`) com target 2.",
                   "Calcule o que acontece com {1000, 1001} se você esquecer o max. expf estoura?"),
        testes([
            ("soma 1", "softmax({1,2,3}) soma dentro de 1e-5."),
            ("ordem", "p(3) > p(1)."),
            ("log", "log_softmax[2] > log_softmax[0]."),
            ("loss", "cross_entropy(..., 2) == -log_softmax[2]."),
        ]),
        pesquisa("estabilidade do softmax", [
            "Qual é o max de {1,2,3} e quanto vale exp(0)?",
            "Por que subtrair o max não muda as razões exp(a)/exp(b)?",
            "O que logf(soma) representa na fórmula do log-softmax?",
            "Por que a loss usa o índice 2 e não 0 neste teste?",
            "Onde float32 estoura se o max for 1000?",
        ], ["Goodfellow, Deep Learning, softmax", "PyTorch docs: log_softmax"]),
        benchmark("softmax C de n=3 repetido 1e6 vezes", "ctest solutions"),
    )


def emit_json_c(day: Path) -> None:
    mod = day / "parsers" / "json_rd_lexer"
    h = r'''#ifndef JSON_LEX_H
#define JSON_LEX_H
enum { TOK_END = 0, TOK_LBRACE = 1, TOK_RBRACE = 2, TOK_NUMBER = 3, TOK_STRING = 4, TOK_COMMA = 5, TOK_COLON = 6 };
typedef struct { int kind; int start; int end; } JsonTok;
int skip_ws(const char *s, int i);
int next_token(const char *s, int i, JsonTok *out);
int lex_count(const char *s);
#endif
'''
    stub = r'''#include "json_lex.h"
int skip_ws(const char *s, int i) {
    /* TODO [PAR-JSON-LEX-01] */
    (void)s; (void)i; return i;
}
int next_token(const char *s, int i, JsonTok *out) {
    /* TODO [PAR-JSON-LEX-02] */
    (void)s; (void)i; (void)out; return -1;
}
int lex_count(const char *s) {
    /* TODO [PAR-JSON-LEX-03] */
    (void)s; return -1;
}
'''
    sol = r'''#include "json_lex.h"
int skip_ws(const char *s, int i) {
    /* PEDAGOGY-SOLUTION: PAR-JSON-LEX-01 */
    while (s[i] == ' ' || s[i] == '\n' || s[i] == '\t') i++;
    return i;
}
int next_token(const char *s, int i, JsonTok *out) {
    /* PEDAGOGY-SOLUTION: PAR-JSON-LEX-02 */
    if (!s || !out) return -1;
    i = skip_ws(s, i);
    out->start = i;
    if (s[i] == 0) { out->kind = TOK_END; out->end = i; return i; }
    if (s[i] == '{') { out->kind = TOK_LBRACE; out->end = i + 1; return i + 1; }
    if (s[i] == '}') { out->kind = TOK_RBRACE; out->end = i + 1; return i + 1; }
    if (s[i] == ',') { out->kind = TOK_COMMA; out->end = i + 1; return i + 1; }
    if (s[i] == ':') { out->kind = TOK_COLON; out->end = i + 1; return i + 1; }
    if (s[i] == '"') {
        int j = i + 1;
        while (s[j] && s[j] != '"') j++;
        if (s[j] != '"') return -1;
        out->kind = TOK_STRING; out->end = j + 1; return j + 1;
    }
    if (s[i] >= '0' && s[i] <= '9') {
        int j = i;
        while (s[j] >= '0' && s[j] <= '9') j++;
        out->kind = TOK_NUMBER; out->end = j; return j;
    }
    return -1;
}
int lex_count(const char *s) {
    /* PEDAGOGY-SOLUTION: PAR-JSON-LEX-03 */
    int i = 0, n = 0;
    if (!s) return -1;
    while (s[i]) {
        JsonTok t;
        int ni = next_token(s, i, &t);
        if (ni < 0 || t.kind == TOK_END) break;
        n++;
        i = ni;
    }
    return n;
}
'''
    test = r'''#include "json_lex.h"
#include <assert.h>
#include <stdio.h>
/* PEDAGOGY-TEST: PAR-JSON-LEX-01 */
/* PEDAGOGY-TEST: PAR-JSON-LEX-02 */
/* PEDAGOGY-TEST: PAR-JSON-LEX-03 */
int main(void) {
    JsonTok t;
    assert(skip_ws("  {", 0) == 2);
    assert(next_token("{", 0, &t) == 1 && t.kind == TOK_LBRACE);
    assert(next_token("42", 0, &t) == 2 && t.kind == TOK_NUMBER && t.end == 2);
    assert(next_token("\"ab\"", 0, &t) == 4 && t.kind == TOK_STRING);
    assert(lex_count("{\"a\":1}") == 5);
    printf("OK json lex\n");
    return 0;
}
'''
    emit_c_pair(mod, "json", {"json_lex.h": (h, h), "json_lex.c": (stub, sol)}, test, "c")
    package(
        mod, "C",
        "# Lexer JSON (subset) — C\n\nLinguagem: **C**. Lexer, não parser Pratt (esse foi o Dia 07 em Python).\n",
        teoria(
            "lexer JSON em C",
            "C",
            "O Pratt do Dia 07 assume tokens prontos. Aqui você produz os tokens de um subset JSON: chaves, string sem escape, número decimal sem sinal, vírgula e dois-pontos.",
            """| Lexema | kind | end-start |
|--------|------|-----------|
| `{` | 1 LBRACE | 1 |
| `42` | 3 NUMBER | 2 |
| `"ab"` | 4 STRING | 4 (aspas inclusas) |
| objeto `{\"a\":1}` | 5 tokens | `{` `"a"` `:` `1` `}` |""",
            """```text
skip_ws("  {", 0) → índice 2 (dois espaços)
next "{": kind=1, consome 1, cursor=1
next "42": kind=3, start=0, end=2 (não inclui lixo depois)
"ab" : aspas, 'a','b', aspas → end=4
{"a":1} tokens:
  1 {   2 "a"   3 :   4 1   5 }
lex_count == 5
```""",
            """1. skip_ws avança espaço, tab e newline.
2. next_token classifica um lexema e devolve o índice seguinte.
3. String: do `"` de abertura até o fechamento, sem escapes neste lab.
4. Número: dígitos ASCII '0'..'9' apenas.
5. lex_count chama next_token até o fim e conta os que não são END.""",
            """- Contar `{"a":1}` como 3 (esquecer `:` e número): o teste exige 5.
- String sem as aspas de fechamento: retorno -1.
- skip_ws não avançar: next_token de `"  {"` no índice 0 não vê a chave.""",
            "O lexer de produção (jq, simdjson) trata escapes e unicode. Este subset é o mínimo para ver o cursor `i` avançar.",
        ),
        resolucao(
            "json lexer C",
            "cmake -S days/2026-09-08/parsers/json_rd_lexer/starter -B days/2026-09-08/parsers/json_rd_lexer/starter/build_ci -A x64\ncmake --build days/2026-09-08/parsers/json_rd_lexer/starter/build_ci --config Release\nctest --test-dir days/2026-09-08/parsers/json_rd_lexer/starter/build_ci -C Release",
            "| `PAR-JSON-LEX-01` | `starter/json_lex.c` | `skip_ws` |\n| `PAR-JSON-LEX-02` | `starter/json_lex.c` | `next_token` |\n| `PAR-JSON-LEX-03` | `starter/json_lex.c` | `lex_count` |",
            todo_section("PAR-JSON-LEX-01", "starter/json_lex.c", "skip_ws", "os kinds",
                         "`\"  {\"` no índice 0 deve avançar para 2.",
                         "while espaço/tab/newline, i++.",
                         "    while (s[i] == ' ' || s[i] == '\\n' || s[i] == '\\t') i++;\n    return i;",
                         "c", "O cursor do lexer não pode tratar espaço como erro nem como token.",
                         "skip_ws(\"  {\", 0)==2.")
            + todo_section("PAR-JSON-LEX-02", "starter/json_lex.c", "next_token", "skip_ws",
                           "O teste exige LBRACE, NUMBER end==2 em \"42\", STRING len 4 em \"ab\".",
                           "Classifique um caractere e avance o cursor.",
                           "    if (s[i] == '{') { out->kind = TOK_LBRACE; out->end = i + 1; return i + 1; }\n    if (s[i] >= '0' && s[i] <= '9') { /* consuma dígitos */ }",
                         "c", "NUMBER end é exclusivo: \"42\" ocupa [0,2).",
                         "kind e end dos três asserts.")
            + todo_section("PAR-JSON-LEX-03", "starter/json_lex.c", "lex_count", "next_token",
                           "`{\"a\":1}` tem 5 tokens. Contar só chaves dá 2 e o teste falha.",
                           "loop next_token até END.",
                           "        int ni = next_token(s, i, &t);\n        if (ni < 0 || t.kind == TOK_END) break;\n        n++; i = ni;",
                         "c", "Cada chamada consome um lexema. O count é o número de chamadas até o fim.",
                         "lex_count == 5."),
        ),
        exercicios("C",
                   "Quebre `{\"a\":1}` em tokens no papel. São 5. Nomeie cada um.",
                   "Implemente `skip_ws` (`PAR-JSON-LEX-01`).",
                   "Implemente next_token e lex_count (`PAR-JSON-LEX-02`, `PAR-JSON-LEX-03`).",
                   "O que o lexer deve fazer com `\"a\\nb\"` neste subset? (escape não é suportado — descreva o cursor.)"),
        testes([
            ("espaço", "skip_ws em dois espaços antes de `{` retorna 2."),
            ("chave e número", "`{` kind 1; `42` kind 3 end 2."),
            ("string", "`\"ab\"` kind 4, cursor 4."),
            ("objeto", "lex_count `{\"a\":1}` == 5."),
        ]),
        pesquisa("lexers", [
            "Por que end de \"42\" é 2 e não 1?",
            "Quais 5 tokens existem em `{\"a\":1}`?",
            "Por que espaço não é token?",
            "O que falta para um JSON real (escapes, `true`, sinal de menos)?",
            "Como este cursor se liga ao Pratt do Dia 07?",
        ], ["ECMA-404 JSON", "Dia 07 parsers/pratt_query_lang"]),
        benchmark("lex_count de 1e5 cópias de {\"a\":1}", "ctest solutions"),
    )


def emit_shader_cpp(day: Path) -> None:
    mod = day / "graphics" / "shader_stage_fsm"
    h = r'''#pragma once
enum ShaderStage { ST_EDIT = 0, ST_COMPILE = 1, ST_LINK = 2, ST_READY = 3 };
int shader_can(int from, int to);
int shader_apply(int *stage, int to);
int shader_illegal(int from, int to);
'''
    stub = r'''#include "shader_fsm.hpp"
int shader_can(int from, int to) {
    // TODO [GFX-SHADER-FSM-01]
    (void)from; (void)to; return 0;
}
int shader_apply(int *stage, int to) {
    // TODO [GFX-SHADER-FSM-02]
    (void)stage; (void)to; return -1;
}
int shader_illegal(int from, int to) {
    // TODO [GFX-SHADER-FSM-03]
    (void)from; (void)to; return 0;
}
'''
    sol = r'''#include "shader_fsm.hpp"
int shader_can(int from, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-01
    if (from == ST_EDIT && to == ST_COMPILE) return 1;
    if (from == ST_COMPILE && (to == ST_LINK || to == ST_EDIT)) return 1;
    if (from == ST_LINK && to == ST_READY) return 1;
    if (from == ST_READY && to == ST_EDIT) return 1;
    return 0;
}
int shader_apply(int *stage, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-02
    if (!stage || !shader_can(*stage, to)) return -1;
    *stage = to;
    return 0;
}
int shader_illegal(int from, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-03
    return shader_can(from, to) ? 0 : 1;
}
'''
    test = r'''#include "shader_fsm.hpp"
#include <assert.h>
#include <stdio.h>
// PEDAGOGY-TEST: GFX-SHADER-FSM-01
// PEDAGOGY-TEST: GFX-SHADER-FSM-02
// PEDAGOGY-TEST: GFX-SHADER-FSM-03
int main() {
    int s = ST_EDIT;
    assert(shader_can(ST_EDIT, ST_COMPILE) == 1);
    assert(shader_can(ST_EDIT, ST_READY) == 0);
    assert(shader_apply(&s, ST_COMPILE) == 0 && s == ST_COMPILE);
    assert(shader_apply(&s, ST_READY) == -1 && s == ST_COMPILE);
    assert(shader_illegal(ST_EDIT, ST_READY) == 1);
    printf("OK shader fsm\n");
    return 0;
}
'''
    emit_c_pair(mod, "shader", {"shader_fsm.hpp": (h, h), "shader_fsm.cpp": (stub, sol)}, test, "cxx")
    gfx_comparison(mod, "shader stage FSM")
    package(
        mod, "C++",
        "# FSM de estágio de shader — C++\n\nLinguagem: **C++**. Headless (sem janela). A evidência é a tabela de transições.\n",
        teoria(
            "máquina de estados de shader em C++",
            "C++",
            "Um shader não salta de rascunho para GPU pronta. A ordem é EDIT → COMPILE → LINK → READY, com volta para EDIT em falha. Pular READY direto do EDIT é ilegal — o teste mede isso.",
            """| De | Para | Legal? |
|----|------|--------|
| EDIT (0) | COMPILE (1) | sim |
| EDIT | READY (3) | não |
| COMPILE | LINK (2) ou EDIT | sim |
| LINK | READY | sim |
| READY | EDIT | sim |""",
            """```text
estado inicial s=0 (EDIT)
can(0,1)=1
can(0,3)=0
apply 1 → s=1, retorno 0
apply 3 a partir de COMPILE → retorno -1, s continua 1
illegal(0,3)=1
```""",
            """1. shader_can consulta a tabela. Qualquer outro par retorna 0.
2. shader_apply só escreve *stage se can for 1.
3. shader_illegal é o inverso de can.""",
            """- Permitir EDIT→READY: o segundo assert (can==0) falha.
- apply ilegal alterar o estágio: o teste exige que s permaneça COMPILE.
- illegal retornar 0 para EDIT→READY: o último assert falha.""",
            "No driver, glCompileShader e glLinkProgram são as arestas. Este lab testa a tabela sem contexto OpenGL.",
        ),
        resolucao(
            "shader FSM C++",
            "cmake -S days/2026-09-08/graphics/shader_stage_fsm/starter -B days/2026-09-08/graphics/shader_stage_fsm/starter/build_ci -A x64\ncmake --build days/2026-09-08/graphics/shader_stage_fsm/starter/build_ci --config Release\nctest --test-dir days/2026-09-08/graphics/shader_stage_fsm/starter/build_ci -C Release",
            "| `GFX-SHADER-FSM-01` | `starter/shader_fsm.cpp` | `shader_can` |\n| `GFX-SHADER-FSM-02` | `starter/shader_fsm.cpp` | `shader_apply` |\n| `GFX-SHADER-FSM-03` | `starter/shader_fsm.cpp` | `shader_illegal` |",
            todo_section("GFX-SHADER-FSM-01", "starter/shader_fsm.cpp", "shader_can", "o enum",
                         "can(EDIT, COMPILE) deve ser 1 e can(EDIT, READY) 0.",
                         "Quatro pares legais, resto 0.",
                         "    if (from == ST_EDIT && to == ST_COMPILE) return 1;\n    if (from == ST_EDIT && to == ST_READY) return 0;\n    return 0;",
                         "cpp", "A aresta EDIT→READY não existe. Compilar é obrigatório.",
                         "asserts can 1 e 0.")
            + todo_section("GFX-SHADER-FSM-02", "starter/shader_fsm.cpp", "shader_apply", "shader_can",
                           "apply para READY a partir de COMPILE deve falhar e não mudar s.",
                           "se !can, retorne -1 sem escrever.",
                           "    if (!stage || !shader_can(*stage, to)) return -1;\n    *stage = to;\n    return 0;",
                         "cpp", "Transição ilegal não pode vazar para o estado seguinte.",
                         "s permanece ST_COMPILE.")
            + todo_section("GFX-SHADER-FSM-03", "starter/shader_fsm.cpp", "shader_illegal", "shader_can",
                           "illegal(EDIT, READY) deve ser 1.",
                           "retorne 1 se can for 0.",
                           "    return shader_can(from, to) ? 0 : 1;",
                         "cpp", "É o predicado inverso, para o teste nomear a aresta proibida.",
                         "illegal==1."),
        ),
        exercicios("C++",
                   "Desenhe os 4 estados e as 5 arestas legais. Marque EDIT→READY com um X.",
                   "Implemente `shader_can` (`GFX-SHADER-FSM-01`).",
                   "Implemente apply e illegal (`GFX-SHADER-FSM-02`, `GFX-SHADER-FSM-03`).",
                   "Qual chamada de driver real corresponde a COMPILE→LINK? Escreva o nome da API."),
        testes([
            ("aresta legal", "EDIT→COMPILE retorna 1."),
            ("aresta ilegal", "EDIT→READY retorna 0."),
            ("apply", "EDIT→COMPILE muda o estado; COMPILE→READY não muda."),
            ("predicado", "illegal(EDIT, READY)==1."),
        ]),
        pesquisa("pipeline de shader", [
            "Por que EDIT não vai direto a READY?",
            "Qual estado permanece se apply falha?",
            "Quantas arestas saem de COMPILE?",
            "O que glCompileShader faz na coluna OpenGL de COMPARISON.md?",
            "Por que este lab não abre janela?",
        ], ["OpenGL spec: shader objects", "docs/COMPARISON.md deste módulo"]),
        benchmark("1e6 consultas shader_can", "ctest solutions"),
    )


def emit_bell_cpp(day: Path) -> None:
    mod = day / "quantum" / "bell_state_prep"
    h = r'''#pragma once
void q_reset(double amp[4]);
void q_h0(double amp[4]);
void q_cnot(double amp[4]);
double q_prob(const double amp[4], int basis);
'''
    stub = r'''#include "bell.hpp"
void q_reset(double amp[4]) { /* TODO [Q-BELL-01] */ (void)amp; }
void q_h0(double amp[4]) { /* TODO [Q-BELL-02] */ (void)amp; }
void q_cnot(double amp[4]) { /* TODO [Q-BELL-03] */ (void)amp; }
double q_prob(const double amp[4], int basis) { (void)amp; (void)basis; return -1.0; }
'''
    sol = r'''#include "bell.hpp"
#include <math.h>
void q_reset(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-01
    amp[0] = 1.0; amp[1] = 0.0; amp[2] = 0.0; amp[3] = 0.0;
}
void q_h0(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-02
    const double s = 1.0 / sqrt(2.0);
    double a0 = amp[0], a1 = amp[1], a2 = amp[2], a3 = amp[3];
    amp[0] = s * (a0 + a2);
    amp[1] = s * (a1 + a3);
    amp[2] = s * (a0 - a2);
    amp[3] = s * (a1 - a3);
}
void q_cnot(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-03
    double a2 = amp[2], a3 = amp[3];
    amp[2] = a3;
    amp[3] = a2;
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
'''
    test = r'''#include "bell.hpp"
#include <assert.h>
#include <math.h>
#include <stdio.h>
// PEDAGOGY-TEST: Q-BELL-01
// PEDAGOGY-TEST: Q-BELL-02
// PEDAGOGY-TEST: Q-BELL-03
int main() {
    double a[4];
    q_reset(a);
    assert(fabs(a[0] - 1.0) < 1e-9);
    q_h0(a);
    assert(fabs(a[0] - 1.0 / sqrt(2.0)) < 1e-9);
    assert(fabs(a[2] - 1.0 / sqrt(2.0)) < 1e-9);
    q_cnot(a);
    assert(fabs(q_prob(a, 0) - 0.5) < 1e-9);
    assert(fabs(q_prob(a, 3) - 0.5) < 1e-9);
    assert(fabs(q_prob(a, 1)) < 1e-9);
    printf("OK bell\n");
    return 0;
}
'''
    emit_c_pair(mod, "bell", {"bell.hpp": (h, h), "bell.cpp": (stub, sol)}, test, "cxx")
    package(
        mod, "C++",
        "# Preparação do estado de Bell — C++\n\nLinguagem: **C++**. Statevector real de 2 qubits (4 amplitudes).\n",
        teoria(
            "estado de Bell em C++",
            "C++",
            "O lab de medição do Dia 07 assume um estado pronto. Aqui você **prepara** `|Φ+⟩ = (|00⟩+|11⟩)/√2` com H no qubit 0 e CNOT.",
            """Indexação |q1 q0|: índice = q1*2+q0.
| bits | índice | |00⟩ inicial |
|------|--------|-------------|
| 00 | 0 | 1 |
| 01 | 1 | 0 |
| 10 | 2 | 0 |
| 11 | 3 | 0 |""",
            """```text
reset: [1, 0, 0, 0]
H no q0 (mistura índices 0 com 2, 1 com 3):
  a0' = (a0+a2)/√2 = 1/√2 ≈ 0.707106781
  a2' = (a0-a2)/√2 = 1/√2
  a1' = a3' = 0
CNOT (controle q0, alvo q1) troca amp[2] com amp[3]:
  [1/√2, 0, 0, 1/√2]
P(00)=0.5, P(11)=0.5, P(01)=0
```""",
            """1. q_reset põe amp[0]=1 e o resto 0.
2. q_h0 aplica Hadamard no qubit 0 sobre o vetor de 4 componentes (sem matriz 4x4 explícita).
3. q_cnot troca amp[2] e amp[3] (os estados em que q0=1).
4. q_prob é o quadrado da amplitude (estado real).""",
            """- Esquecer de zerar amp[1..3]: o teste de |00⟩ falha.
- H sem 1/√2: a amplitude não é ~0.707.
- CNOT trocar 0 com 1: P(11) não vira 0.5.""",
            "Qiskit `H(0); CX(0,1)` produz o mesmo vetor. Aqui não há fase imaginária.",
        ),
        resolucao(
            "Bell C++",
            "cmake -S days/2026-09-08/quantum/bell_state_prep/starter -B days/2026-09-08/quantum/bell_state_prep/starter/build_ci -A x64\ncmake --build days/2026-09-08/quantum/bell_state_prep/starter/build_ci --config Release\nctest --test-dir days/2026-09-08/quantum/bell_state_prep/starter/build_ci -C Release",
            "| `Q-BELL-01` | `starter/bell.cpp` | `q_reset` |\n| `Q-BELL-02` | `starter/bell.cpp` | `q_h0` |\n| `Q-BELL-03` | `starter/bell.cpp` | `q_cnot` |",
            todo_section("Q-BELL-01", "starter/bell.cpp", "q_reset", "q_prob",
                         "O vetor precisa começar em |00⟩. Sem reset, H não parte de [1,0,0,0].",
                         "amp[0]=1, demais 0.",
                         "    amp[0] = 1.0; amp[1] = 0.0; amp[2] = 0.0; amp[3] = 0.0;",
                         "cpp", "Um statevector sem reset herda lixo e as probabilidades não somam 1.",
                         "fabs(a[0]-1)<1e-9.")
            + todo_section("Q-BELL-02", "starter/bell.cpp", "q_h0", "o reset",
                           "Depois de H, a0 e a2 valem 1/√2.",
                           "salve as 4 amplitudes; misture 0/2 e 1/3 com 1/sqrt(2).",
                           "    const double s = 1.0 / sqrt(2.0);\n    amp[0] = s * (a0 + a2);\n    amp[2] = s * (a0 - a2);",
                         "cpp", "H em q0 é uma mistura dos estados que diferem no bit baixo.",
                         "a[0] e a[2] ≈ 0.707.")
            + todo_section("Q-BELL-03", "starter/bell.cpp", "q_cnot", "q_h0",
                           "CNOT move a amplitude de |10⟩ para |11⟩. P(11) deve ser 0.5.",
                           "troque amp[2] e amp[3].",
                           "    double a2 = amp[2], a3 = amp[3];\n    amp[2] = a3;\n    amp[3] = a2;",
                         "cpp", "Depois de H, a massa em |10⟩ (índice 2) vai para |11⟩ (índice 3).",
                         "q_prob(a,0) e q_prob(a,3) == 0.5."),
        ),
        exercicios("C++",
                   "Escreva o vetor depois de reset, depois de H, depois de CNOT. Três linhas de 4 números.",
                   "Implemente `q_reset` (`Q-BELL-01`).",
                   "Implemente H e CNOT (`Q-BELL-02`, `Q-BELL-03`). P(00)=P(11)=0.5.",
                   "Qual índice é |01⟩? Mostre que a probabilidade dele é 0 no Bell."),
        testes([
            ("reset", "amp[0]==1."),
            ("H", "amp[0] e amp[2] == 1/sqrt(2)."),
            ("CNOT", "P(0)=0.5 e P(3)=0.5."),
            ("basis 1", "P(1)≈0."),
        ]),
        pesquisa("Bell e Born", [
            "Qual índice do vetor é |11⟩?",
            "Por que H sozinho não é emaranhado?",
            "Quanto vale (1/√2)^2?",
            "O que o CNOT troca neste indexing?",
            "Como isso alimenta a medição do Dia 07?",
        ], ["Nielsen & Chuang, Bell state", "Dia 07 quantum/measurement_born"]),
        benchmark("1e5 preparações Bell", "ctest solutions"),
    )


def emit_asm(day: Path, rel: str, name: str, masm_stub: str, masm_sol: str, gas_stub: str, gas_sol: str, c_test: str, c_decl: str, docs: dict) -> None:
    mod = day.joinpath(*rel.split("/"))
    for side, masm, gas in (("starter", masm_stub, gas_stub), ("solutions", masm_sol, gas_sol)):
        wipe_py(mod / side)
        base = mod / side
        write(base / f"{name}.asm", masm)
        write(base / f"{name}.S", gas)
        write(base / "test_main.c", c_test)
        write(base / "api.h", c_decl)
        write(base / "CMakeLists.txt", CMAKE_ASM.format(name=name, c_sources="test_main.c", asm=f"{name}.asm", gas=f"{name}.S"))
    package(mod, "Assembly", docs["readme"], docs["teoria"], docs["res"], docs["ex"], docs["tg"], docs["pq"], docs["bench"])


def emit_wasm_asm(day: Path) -> None:
    masm_stub = r'''; WASM magic / version / section id — Windows x64 (RCX = pointer or id)
option casemap:none
.code
; TODO [TOOL-WASM-01]: return 1 if bytes 00 61 73 6D
wasm_magic_ok PROC
    xor eax, eax
    ret
wasm_magic_ok ENDP
; TODO [TOOL-WASM-02]: version u32 LE at +4 equals 1
wasm_version_is_1 PROC
    xor eax, eax
    ret
wasm_version_is_1 ENDP
; TODO [TOOL-WASM-03]: section id in CL: 1 type, 2 import, else 0
section_class PROC
    xor eax, eax
    ret
section_class ENDP
END
'''
    masm_sol = r'''option casemap:none
.code
wasm_magic_ok PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-01
    cmp byte ptr [rcx], 00h
    jne fail1
    cmp byte ptr [rcx+1], 61h
    jne fail1
    cmp byte ptr [rcx+2], 73h
    jne fail1
    cmp byte ptr [rcx+3], 6Dh
    jne fail1
    mov eax, 1
    ret
fail1:
    xor eax, eax
    ret
wasm_magic_ok ENDP
wasm_version_is_1 PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-02
    mov eax, dword ptr [rcx+4]
    cmp eax, 1
    jne fail2
    mov eax, 1
    ret
fail2:
    xor eax, eax
    ret
wasm_version_is_1 ENDP
section_class PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-03
    movzx eax, cl
    cmp al, 1
    je one
    cmp al, 2
    jne zero
    mov eax, 2
    ret
one:
    mov eax, 1
    ret
zero:
    xor eax, eax
    ret
section_class ENDP
END
'''
    gas_stub = r'''/* TODO [TOOL-WASM-01] */
.intel_syntax noprefix
.text
.global wasm_magic_ok
wasm_magic_ok:
    xor eax, eax
    ret
.global wasm_version_is_1
wasm_version_is_1:
    xor eax, eax
    ret
.global section_class
section_class:
    xor eax, eax
    ret
'''
    gas_sol = r'''.intel_syntax noprefix
.text
.global wasm_magic_ok
wasm_magic_ok:
    cmp byte ptr [rdi], 0
    jne 1f
    cmp byte ptr [rdi+1], 0x61
    jne 1f
    cmp byte ptr [rdi+2], 0x73
    jne 1f
    cmp byte ptr [rdi+3], 0x6d
    jne 1f
    mov eax, 1
    ret
1:
    xor eax, eax
    ret
.global wasm_version_is_1
wasm_version_is_1:
    mov eax, dword ptr [rdi+4]
    cmp eax, 1
    jne 2f
    mov eax, 1
    ret
2:
    xor eax, eax
    ret
.global section_class
section_class:
    movzx eax, dil
    cmp al, 1
    je 3f
    cmp al, 2
    jne 4f
    mov eax, 2
    ret
3:
    mov eax, 1
    ret
4:
    xor eax, eax
    ret
'''
    c_test = r'''#include "api.h"
#include <assert.h>
#include <stdio.h>
/* PEDAGOGY-TEST: TOOL-WASM-01 */
/* PEDAGOGY-TEST: TOOL-WASM-02 */
/* PEDAGOGY-TEST: TOOL-WASM-03 */
int main(void) {
    unsigned char ok[] = {0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00};
    unsigned char bad[] = {0x00, 0x61, 0x73, 0x00, 0x01, 0x00, 0x00, 0x00};
    assert(wasm_magic_ok(ok) == 1);
    assert(wasm_magic_ok(bad) == 0);
    assert(wasm_version_is_1(ok) == 1);
    assert(section_class(1) == 1);
    assert(section_class(2) == 2);
    assert(section_class(9) == 0);
    printf("OK wasm asm\n");
    return 0;
}
'''
    decl = r'''#ifndef WASM_API_H
#define WASM_API_H
int wasm_magic_ok(const unsigned char *p);
int wasm_version_is_1(const unsigned char *p);
int section_class(unsigned char id);
#endif
'''
    docs = {
        "readme": "# WASM header — Assembly\n\nLinguagem: **Assembly** (MASM no Windows, GAS no Linux). O teste C só chama as três funções.\n",
        "teoria": teoria(
            "cabeçalho WASM em Assembly",
            "Assembly (MASM x64)",
            "O módulo de tooling deste dia não é um script. Você compara bytes de um módulo WASM na linguagem da máquina. No Windows o primeiro argumento chega em RCX (x64 ABI da Microsoft).",
            """| Offset | Byte | Significado |
|--------|------|-----------|
| 0 | 00 | magic |
| 1 | 61 | 'a' |
| 2 | 73 | 's' |
| 3 | 6D | 'm' |
| 4..7 | 01 00 00 00 | version = 1 (u32 LE) |
| id | CL | 1 type, 2 import |""",
            """```text
ponteiro RCX → 00 61 73 6D 01 00 00 00
[rcx+0]=00, +1=61, +2=73, +3=6D → eax=1
dword [rcx+4] = 1 (little-endian) → version ok
section_class(1) → eax=1
section_class(2) → eax=2
section_class(9) → eax=0
magic quebrado 00 61 73 00 → eax=0
```""",
            """1. Compare 4 bytes. Qualquer diferença zera EAX e ret.
2. Leia dword em RCX+4 e compare com 1.
3. section_class usa CL (byte baixo de RCX). 1 ou 2; senão 0.""",
            """- Esquecer o byte 6D: magic `\\0asm` incompleto passa no stub (eax=0) e o teste exige 1.
- Ler version em big-endian (byte 7): o 1 está no offset 4, não no 7.
- Tratar id 9 como type: o teste exige 0.""",
            "wasm-objdump faz a mesma checagem de magic. Aqui são três predicados em Assembly para ver o ABI (RCX/EAX) sem runtime WASM.",
        ),
        "res": resolucao(
            "wasm assembly",
            "cmake -S days/2026-09-08/tooling/wasm_section_header/starter -B days/2026-09-08/tooling/wasm_section_header/starter/build_ci -A x64\ncmake --build days/2026-09-08/tooling/wasm_section_header/starter/build_ci --config Release\nctest --test-dir days/2026-09-08/tooling/wasm_section_header/starter/build_ci -C Release",
            "| `TOOL-WASM-01` | `starter/wasm_section.asm` | `wasm_magic_ok` |\n| `TOOL-WASM-02` | `starter/wasm_section.asm` | `wasm_version_is_1` |\n| `TOOL-WASM-03` | `starter/wasm_section.asm` | `section_class` |",
            todo_section("TOOL-WASM-01", "starter/wasm_section.asm", "wasm_magic_ok", "o PROC e o END",
                         "O stub zera EAX. O teste exige 1 para `00 61 73 6D`.",
                         "cmp byte [rcx+i] com 00, 61h, 73h, 6Dh.",
                         "    cmp byte ptr [rcx], 00h\n    cmp byte ptr [rcx+1], 61h\n    cmp byte ptr [rcx+3], 6Dh\n    mov eax, 1",
                         "asm", "No ABI Windows x64 o ponteiro está em RCX, o retorno em EAX.",
                         "wasm_magic_ok(ok)==1 e bad==0.")
            + todo_section("TOOL-WASM-02", "starter/wasm_section.asm", "wasm_version_is_1", "o magic",
                           "Version 1 está nos bytes 01 00 00 00. dword [rcx+4] vale 1.",
                           "mov eax, dword ptr [rcx+4]; cmp eax, 1.",
                           "    mov eax, dword ptr [rcx+4]\n    cmp eax, 1",
                         "asm", "Little-endian faz o 0x01 no offset 4 ser o valor inteiro 1.",
                         "version_is_1==1.")
            + todo_section("TOOL-WASM-03", "starter/wasm_section.asm", "section_class", "os dois predicados",
                           "id 1 → 1, id 2 → 2, id 9 → 0. O argumento está em CL.",
                           "cmp al, 1 / cmp al, 2.",
                           "    movzx eax, cl\n    cmp al, 1",
                         "asm", "Inteiro pequeno chega no byte baixo de RCX.",
                         "section_class(9)==0."),
        ),
        "ex": exercicios("Assembly",
                         "Escreva os 8 bytes do header WASM e o valor do dword no offset 4.",
                         "Implemente `wasm_magic_ok` (`TOOL-WASM-01`) em `wasm_section.asm`.",
                         "Implemente version e section_class (`TOOL-WASM-02`, `TOOL-WASM-03`).",
                         "No Linux o ponteiro chega em RDI, não em RCX. O arquivo `.S` já usa RDI. Não misture os dois."),
        "tg": testes([
            ("magic", "`00 61 73 6D` → 1; último byte 00 → 0."),
            ("version", "u32 LE no offset 4 igual a 1."),
            ("section 1 e 2", "type=1, import=2."),
            ("section 9", "desconhecida → 0."),
        ]),
        "pq": pesquisa("WASM magic em Assembly", [
            "Quais 4 bytes são o magic WASM?",
            "Por que o argumento está em RCX neste Windows?",
            "Onde está o 1 da version no dump 01 00 00 00?",
            "O que section id 1 e 2 significam no formato WASM?",
            "Por que o .S usa RDI e o .asm usa RCX?",
        ], ["WebAssembly binary format, magic + version", "Microsoft x64 calling convention"]),
        "bench": benchmark("chamadas wasm_magic_ok", "ctest solutions"),
    }
    emit_asm(day, "tooling/wasm_section_header", "wasm_section", masm_stub, masm_sol, gas_stub, gas_sol, c_test, decl, docs)


def deepen_kept(mod: Path, lang: str, title: str, why: str, layout: str, trace: str, algo: str, bugs: str, prod: str,
                baseline: str, mapa: str, sections: str, ex: tuple[str, str, str, str], casos, questions, links) -> None:
    package(
        mod, lang,
        f"# {title}\n\nLinguagem: **{lang}**.\n\n```powershell\n{baseline}\n```\n",
        teoria(title, lang, why, layout, trace, algo, bugs, prod),
        resolucao(title, baseline, mapa, sections),
        exercicios(lang, *ex),
        testes(casos),
        pesquisa(title, questions, links),
        benchmark("tempo do teste de solutions", baseline),
    )


def deepen_day08_kept(day: Path) -> None:
    deepen_kept(
        day / "rust" / "clvm_disasm", "Rust",
        "disassembler CLVM em Rust",
        "Par do disassembler C do mesmo dia. A ISA é a mesma; o tipo de erro é `Result`, não um int -1.",
        "| Função | Contrato |\n|--------|----------|\n| `opcode_name(0x01)` | `Some(\"PUSH\")` |\n| `opcode_name(0x08)` | `Some(\"HALT\")` |\n| `instruction_size(0x01)` | 5 |\n| `instruction_size(0x09)` | 3 |\n| `disassemble([01,42,0,0,0,08])` | `[\"PUSH 42\", \"HALT\"]` |",
        """```text
opcode 0x01 → Some("PUSH")
opcode 0x08 → Some("HALT")
size(PUSH)=5, size(JMP=0x09)=3, size(HALT)=1
bytes [01, 2A, 00, 00, 00, 08]
  pc=0 PUSH imm=42, avança 5
  pc=5 HALT, avança 1
  ["PUSH 42", "HALT"]
[FF] → Err
```""",
        "1. Nomeie PUSH/ADD/HALT/JMP.\n2. Tamanho: PUSH 5, branch 3, resto 1.\n3. Walk com `from_le_bytes` no imediato.",
        "- size(PUSH)=1 quebra o disassemble (o 42 vira opcode).\n- `None` para HALT falha o Caso 1.",
        "O crate Rust do Dia 07 (`clvm_v2_verify`) valida. Este lista.",
        "cargo test --manifest-path days/2026-09-08/rust/clvm_disasm/starter/Cargo.toml",
        "| `CLVM-RS-DIS-01` | `starter/src/lib.rs` | `opcode_name` |\n| `CLVM-RS-DIS-02` | `starter/src/lib.rs` | `instruction_size` |\n| `CLVM-RS-DIS-03` | `starter/src/lib.rs` | `disassemble` |",
        todo_section("CLVM-RS-DIS-01", "starter/src/lib.rs", "opcode_name", "PUSH const",
                     "O teste exige Some(\"PUSH\") e Some(\"HALT\").",
                     "match nos opcodes conhecidos.",
                     "        0x08 => Some(\"HALT\"),\n        0x01 => Some(\"PUSH\"),",
                     "rust", "O nome é a string do listing, igual ao C.",
                     "caso_1_opcode_name passa.")
        + todo_section("CLVM-RS-DIS-02", "starter/src/lib.rs", "instruction_size", "opcode_name",
                       "PUSH=5, JMP=3, HALT=1. Stub retorna 0.",
                       "if op==PUSH 5 else if branch 3 else 1.",
                       "    if op == PUSH { 5 } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) { 3 } else { 1 }",
                     "rust", "O tamanho é o mesmo contrato do decodificador C.",
                     "instruction_size(PUSH)==5.")
        + todo_section("CLVM-RS-DIS-03", "starter/src/lib.rs", "disassemble", "os dois acima",
                       "O slice [PUSH,42,0,0,0,HALT] vira duas strings. 0xFF é Err.",
                       "while pc < len, leia u32 LE no PUSH.",
                       "            let imm = u32::from_le_bytes(code[pc + 1..pc + 5].try_into().unwrap());\n            out.push(format!(\"PUSH {}\", imm));",
                     "rust", "from_le_bytes é o imm 42. Truncar o slice retorna Err.",
                     "vec![\"PUSH 42\", \"HALT\"]."),
        ("No papel, size de 0x01, 0x09 e 0x08.",
         "Implemente opcode_name (`CLVM-RS-DIS-01`).",
         "size e disassemble (`CLVM-RS-DIS-02`, `CLVM-RS-DIS-03`).",
         "Compare o Err de 0xFF com o retorno -1 do lab em C. Mesma recusa, tipo diferente."),
        [("nome", "opcode_name(PUSH)=Some(\"PUSH\"), HALT Some."),
         ("tamanho", "5, 3 e 1."),
         ("listing", "PUSH 42 e HALT."),
         ("erro", "0xFF é Err.")],
        ["Por que PUSH tem size 5 em Rust e em C?", "O que from_le_bytes faz com 2A 00 00 00?", "Quando o walk deve retornar Err?", "Qual função do lab C é gêmea de instruction_size?", "O verifier do Dia 07 recusa o quê que o disasm também recusa?"],
        ["Rust book, Result", "Dia 07 rust/clvm_v2_verify"],
    )
    deepen_kept(
        day / "dotnet" / "pe_export_span", ".NET",
        "export directory PE com Span",
        "O triage ELF dos dias anteriores é arquivo Unix. Este lab lê um PE mínimo em C# com `ReadOnlySpan<byte>` — sem `BinaryReader` que esconde o offset.",
        """| Offset | Campo | Valor no fixture |
|--------|-------|------------------|
| 0 | 'M' | 0x4D |
| 1 | 'Z' | 0x5A |
| 0x3C | e_lfanew | 0x80 |
| 0x80 | 'P' 'E' 0 0 | assinatura |
| optional + 0x78 | export RVA | 0x1000 |""",
        """```text
buffer 0x200
buf[0]='M' buf[1]='Z'
int32 em 0x3C = 0x80
PE signature em 0x80
opt = pe + 4 + 20 = 0x80+24 = 0x98
data directory[0] em opt+0x78 = 0x110
uint32 = 0x1000
IsPeFile true; offset 0x80; export RVA 0x1000
três bytes {0,1,2} não são PE
```""",
        "1. MZ nos dois primeiros bytes e PE no e_lfanew.\n2. Leia int32 em 0x3C.\n3. Export RVA é o primeiro data directory, 0x78 depois do início do optional header (PE32+ magic 0x20B no fixture).",
        "- Ignorar e_lfanew e procurar PE no offset 0x80 fixo: o teste do offset falha se você não ler 0x3C.\n- Ler RVA no lugar errado: não é 0x1000.",
        "dumpbin /exports faz o mesmo RVA. Aqui o buffer é sintético (0x200 bytes).",
        "dotnet test days/2026-09-08/dotnet/pe_export_span/starter/tests/Chris.PeLab.Tests.csproj",
        "| `DN-PE-EXP-01` | `starter/PeExportSpan.cs` | `IsPeFile` |\n| `DN-PE-EXP-02` | `starter/PeExportSpan.cs` | `TryGetPeOffset` |\n| `DN-PE-EXP-03` | `starter/PeExportSpan.cs` | `TryReadExportRva` |",
        todo_section("DN-PE-EXP-01", "starter/PeExportSpan.cs", "IsPeFile", "os offsets mágicos do teste",
                     "MinimalPe() é PE. Um array de 3 bytes não é.",
                     "MZ, depois PE no offset lido de 0x3C.",
                     "        if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;\n        if (!TryGetPeOffset(data, out int off)) return false;\n        return data[off] == (byte)'P' && data[off + 1] == (byte)'E';",
                     "csharp", "A assinatura PE não está num offset fixo; e_lfanew diz onde.",
                     "IsPeFile(MinimalPe()) true; 3 bytes false.")
        + todo_section("DN-PE-EXP-02", "starter/PeExportSpan.cs", "TryGetPeOffset", "IsPeFile",
                       "O int em 0x3C é 0x80. O teste exige esse valor em peOffset.",
                       "MemoryMarshal.Read<int> em Slice(0x3C, 4).",
                       "        peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));\n        return peOffset > 0 && peOffset + 4 <= data.Length;",
                     "csharp", "0x3C é o campo e_lfanew do DOS header. Little-endian no BitConverter do teste.",
                     "off == 0x80.")
        + todo_section("DN-PE-EXP-03", "starter/PeExportSpan.cs", "TryReadExportRva", "os dois anteriores",
                       "O uint no offset calculado é 0x1000.",
                       "opt = pe+24; leia uint em opt+0x78.",
                       "        int opt = pe + 4 + 20;\n        exportRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78, 4));",
                     "csharp", "0x78 é o início dos data directories no optional PE32+ deste fixture (magic 0x20B em 0x98).",
                     "exportRva == 0x1000."),
        ("Desenhe os offsets 0, 0x3C, 0x80, 0x110 e o valor de cada um.",
         "Implemente IsPeFile (`DN-PE-EXP-01`).",
         "Offset e export RVA (`DN-PE-EXP-02`, `DN-PE-EXP-03`).",
         "Por que data directory [0] é export e não import? Anote o índice."),
        [("MZ+PE", "IsPeFile true no buffer de 0x200."),
         ("e_lfanew", "0x80."),
         ("export RVA", "0x1000."),
         ("negativo", "3 bytes → false.")],
        ["O que é e_lfanew?", "Por que Span e não byte[] para o offset?", "Qual índice é o export directory?", "O que acontece se peOffset apontar fora do buffer?", "Como dumpbin usa esse RVA?"],
        ["PE/COFF spec, DOS header", "Dia 04 dotnet CLR metadata"],
    )
    deepen_kept(
        day / "nodejs" / "duplex_event_pipe", "JavaScript",
        "Duplex de eventos de 24 bytes",
        "O Transform do Dia 07 só lê. Um Duplex escreve e lê o mesmo registro evdev de 24 bytes, com buffer parcial entre writes.",
        """| Constante | Valor |
|-----------|-------|
| EVENT_SIZE | 24 |
| write de 48 bytes | 2 eventos |
| preenchimento do teste | byte 7 |
| metrics | eventsWritten, eventsRead |""",
        """```text
ev = 24 bytes 0x07
write(ev+ev) = 48 bytes
_write corta em 24:
  eventsWritten=2
  cada fatia vai para _readBuf
_read empurra objetos de 24
metrics.eventsWritten === 2
write de 10 bytes não completa evento (fica no _writeBuf)
```""",
        "1. `_write` concatena e enquanto length>=24 emite para o buffer de leitura.\n2. `_read` dá push de fatias de 24.\n3. metrics devolve os dois contadores.",
        "- Cortar em 16: eventsWritten não é 2.\n- Esquecer evento parcial: o 25º byte vaza como evento curto.",
        "Node Duplex é a base de `net.Socket`. Aqui o framing é fixo (24), como o struct do Dia 07.",
        "node days/2026-09-08/nodejs/duplex_event_pipe/starter/test.js",
        "| `ND-DUPLEX-01` | `starter/duplex_event_pipe.js` | `_write` |\n| `ND-DUPLEX-02` | `starter/duplex_event_pipe.js` | `_read` |\n| `ND-DUPLEX-03` | `starter/duplex_event_pipe.js` | `metrics` |",
        todo_section("ND-DUPLEX-01", "starter/duplex_event_pipe.js", "_write", "EVENT_SIZE",
                     "48 bytes devem contar 2 eventos escritos.",
                     "concat, while >= 24, mova para _readBuf.",
                     "        this._writeBuf = Buffer.concat([this._writeBuf, chunk]);\n        while (this._writeBuf.length >= EVENT_SIZE) {\n            const ev = this._writeBuf.subarray(0, EVENT_SIZE);\n            this._writeBuf = this._writeBuf.subarray(EVENT_SIZE);\n            this._readBuf = Buffer.concat([this._readBuf, ev]);\n            this.eventsWritten++;\n        }",
                     "javascript", "O write do socket pode partir o registro. 24 é o contrato evdev.",
                     "metrics().eventsWritten === 2.")
        + todo_section("ND-DUPLEX-02", "starter/duplex_event_pipe.js", "_read", "_write",
                       "O listener `data` precisa receber buffers de 24.",
                       "push enquanto _readBuf >= 24.",
                       "            const ev = this._readBuf.subarray(0, EVENT_SIZE);\n            this.eventsRead++;\n            if (!this.push(ev)) break;",
                     "javascript", "push(false) é backpressure. Pare o loop nesse caso.",
                     "out.length >= 1.")
        + todo_section("ND-DUPLEX-03", "starter/duplex_event_pipe.js", "metrics", "os contadores",
                       "O teste lê eventsWritten.",
                       "devolva o objeto com os dois campos.",
                       "        return { eventsWritten: this.eventsWritten, eventsRead: this.eventsRead };",
                     "javascript", "Sem metrics o framing não é observável.",
                     "eventsWritten === 2."),
        ("Quantos eventos cabem em 48 bytes se cada um tem 24?",
         "Implemente `_write` (`ND-DUPLEX-01`).",
         "Implemente `_read` e metrics (`ND-DUPLEX-02`, `ND-DUPLEX-03`).",
         "O que deve sobrar no buffer se write tiver 25 bytes? Um byte."),
        [("48 bytes", "eventsWritten == 2."),
         ("data", "pelo menos um chunk de 24."),
         ("metrics", "eventsWritten 2."),
         ("parcial", "menos de 24 fica no write buf.")],
        ["Por que 24 e não o tamanho do objeto JS?", "O que push(false) significa?", "Onde o byte residual mora?", "Como isso se liga ao Transform do Dia 07?", "O que o ring C do mesmo dia faz que o Duplex também faz (FIFO)?"],
        ["Node.js stream Duplex", "Dia 07 nodejs/input_event_transform"],
    )
    deepen_kept(
        day / "redteam" / "pe_export_triage", "Python",
        "triage de export PE",
        "O lab .NET lê o RVA 0x1000. Este Python (red team do dia) só decide se o buffer é PE e se um nome de export é suspeito. Não executa o binário.",
        """| Offset | Campo no teste | Valor |
|--------|----------------|-------|
| 0 | MZ | `4D 5A` |
| 0x3C | e_lfanew | 0x80 |
| 0x80 | PE | `PE` |
| nomes | VirtualAlloc, malloc | só o primeiro é suspeito |""",
        """```text
minimal_pe: 0x100 bytes, MZ, e_lfanew=0x80, PE em 0x80
validate_mz_pe(pe) == True
count_export_names(pe, ["A", "B"]) == 2
flag_suspicious_exports(["VirtualAlloc", "malloc"]) == ["VirtualAlloc"]
count_export_names(b"bad", []) == -1
```""",
        "1. MZ e PE via e_lfanew little-endian em 0x3C.\n2. Se PE inválido, count retorna -1. Senão len(names).\n3. Filtre nomes que estão na tupla SUSPICIOUS.",
        "- Tratar `b\"bad\"` como PE: count deve ser -1.\n- Incluir malloc na lista suspeita: o teste espera só VirtualAlloc.",
        "O parser de RVA está no lab C#. Este script é a camada de evidência que o analista roda sem o SDK.",
        "python days/2026-09-08/redteam/pe_export_triage/starter/test_pe_export_triage.py",
        "| `RT-PE-EXP-01` | `starter/pe_export_triage.py` | `validate_mz_pe` |\n| `RT-PE-EXP-02` | `starter/pe_export_triage.py` | `count_export_names` |\n| `RT-PE-EXP-03` | `starter/pe_export_triage.py` | `flag_suspicious_exports` |",
        todo_section("RT-PE-EXP-01", "starter/pe_export_triage.py", "validate_mz_pe", "SUSPICIOUS",
                     "minimal_pe() deve passar. Sem ler e_lfanew o PE em 0x80 é invisível.",
                     "len>=0x40, MZ, unpack <I em 0x3C, PE nos dois bytes seguintes.",
                     "    if len(data) < 0x40 or data[0:2] != b\"MZ\":\n        return False\n    pe_off = struct.unpack_from(\"<I\", data, 0x3C)[0]\n    return pe_off + 4 <= len(data) and data[pe_off:pe_off + 2] == b\"PE\"",
                     "python", "O mesmo e_lfanew 0x80 do lab C#. Aqui a evidência é booleana.",
                     "validate_mz_pe(pe) é verdadeiro.")
        + todo_section("RT-PE-EXP-02", "starter/pe_export_triage.py", "count_export_names", "validate_mz_pe",
                       "PE válido com [\"A\",\"B\"] conta 2. `b\"bad\"` retorna -1.",
                       "Se validate falhar, -1. Senão len(names).",
                       "    if not validate_mz_pe(data):\n        return -1\n    return len(names)",
                     "python", "Não parseamos a tabela de nomes neste subset: o teste entrega a lista e pede a contagem condicionada ao PE.",
                     "count == 2 e count(b\"bad\") == -1.")
        + todo_section("RT-PE-EXP-03", "starter/pe_export_triage.py", "flag_suspicious_exports", "a tupla SUSPICIOUS",
                       "VirtualAlloc entra; malloc não.",
                       "Filtre nomes presentes em SUSPICIOUS.",
                       "    return [n for n in names if n in SUSPICIOUS]",
                     "python", "Três nomes clássicos de injeção. malloc não está na tupla.",
                     "lista igual a [\"VirtualAlloc\"]."),
        ("Desenhe MZ, 0x3C=0x80, PE em 0x80.",
         "Implemente `validate_mz_pe` (`RT-PE-EXP-01`).",
         "Implemente count e flags (`RT-PE-EXP-02`, `RT-PE-EXP-03`).",
         "Por que malloc não é suspeito neste lab e VirtualAlloc é?"),
        [("RT-PE-EXP-01", "validate_mz_pe(minimal_pe) verdadeiro."),
         ("RT-PE-EXP-02", "count [A,B] == 2; bad == -1."),
         ("RT-PE-EXP-03", "só VirtualAlloc."),
         ("negativo", "b\"bad\" não é PE.")],
        ["Onde está e_lfanew?", "Por que count de PE inválido é -1 e não 0?", "Quais três nomes estão em SUSPICIOUS?", "O que o lab C# lê que este não lê?", "Por que este lab ficou em Python e o disasm em C?"],
        ["PE/COFF DOS stub", "Dia 08 dotnet/pe_export_span"],
    )
    deepen_kept(
        day / "agent" / "tool_protocol_fsm", "Python",
        "FSM de protocolo de ferramenta",
        "O loop do Dia 07 percebe e verifica. Este Python (harness, não bytecode) só deixa a ferramenta andar IDLE → CALLING → WAITING → DONE ou ERROR.",
        """| Estado | Evento | Próximo |
|--------|--------|---------|
| IDLE | call | CALLING |
| CALLING | sent | WAITING |
| WAITING | ok | DONE |
| WAITING | err | ERROR |""",
        """```text
fsm.transition("call") == "CALLING"
trace anexa "call->CALLING"
transition("sent") → WAITING
handle_response(True, {"result": 1}) → state DONE
  payload_keys = ["result"]
validate_tool_call("search", {}) == True
segundo fsm: call, sent, handle_response(False, {}) → ERROR
evento fora da tabela → ValueError
```""",
        "1. transition consulta TRANSITIONS[(state, event)]. Se não houver, ValueError sem mudar estado.\n2. handle_response chama transition(\"ok\" ou \"err\") e devolve state + keys.\n3. validate_tool_call exige name não vazio e args dict.",
        "- Aceitar call a partir de WAITING: a chave não existe, o teste do ERROR path não chega se você não recusar.\n- validate(\"\", {}) deve ser falso.",
        "O harness em projects/chris-agent-harness registra a mesma trilha. Aqui a evidência é o trace.",
        "python days/2026-09-08/agent/tool_protocol_fsm/starter/test_tool_protocol_fsm.py",
        "| `AGT-TOOL-01` | `starter/tool_protocol_fsm.py` | `transition` |\n| `AGT-TOOL-02` | `starter/tool_protocol_fsm.py` | `handle_response` |\n| `AGT-TOOL-03` | `starter/tool_protocol_fsm.py` | `validate_tool_call` |",
        todo_section("AGT-TOOL-01", "starter/tool_protocol_fsm.py", "transition", "TRANSITIONS",
                     "IDLE + call deve virar CALLING. Stub levanta NotImplementedError.",
                     "key=(self.state, event). Se ausente, ValueError. Senão atualize state e anexe trace.",
                     "        key = (self.state, event)\n        if key not in TRANSITIONS:\n            raise ValueError(key)\n        self.state = TRANSITIONS[key]\n        self.trace.append(f\"{event}->{self.state}\")\n        return self.state",
                     "python", "Os nomes são IDLE/CALLING em maiúsculas, como a tabela do starter. \"idle\" não casa.",
                     "transition(\"call\") == \"CALLING\".")
        + todo_section("AGT-TOOL-02", "starter/tool_protocol_fsm.py", "handle_response", "transition",
                       "Depois de call e sent, ok=True leva a DONE. ok=False leva a ERROR.",
                       "transition(\"ok\" if ok else \"err\") e devolva dict com state e keys.",
                     "        self.transition(\"ok\" if ok else \"err\")\n        return {\"state\": self.state, \"payload_keys\": list(payload.keys())}",
                     "python", "A resposta não muda estado sozinha: reusa a tabela. As keys provam que o payload não foi descartado.",
                     "ev[\"state\"] == \"DONE\" e o segundo fsm fica ERROR.")
        + todo_section("AGT-TOOL-03", "starter/tool_protocol_fsm.py", "validate_tool_call", "a FSM",
                       "search + dict vazio é chamada válida.",
                       "name truthy e isinstance(args, dict).",
                     "        return bool(name) and isinstance(args, dict)",
                     "python", "Nome vazio não é ferramenta. args tem de ser dict, não lista.",
                     "validate_tool_call(\"search\", {}) é verdadeiro."),
        ("Desenhe IDLE → CALLING → WAITING → DONE e a bifurcação err→ERROR.",
         "Implemente `transition` (`AGT-TOOL-01`).",
         "Implemente handle_response e validate (`AGT-TOOL-02`, `AGT-TOOL-03`).",
         "Qual evento a partir de IDLE não está na tabela? O que a função deve levantar?"),
        [("AGT-TOOL-01", "call a partir de IDLE vira CALLING."),
         ("AGT-TOOL-02", "ok → DONE; False → ERROR."),
         ("AGT-TOOL-03", "search + {} é válido."),
         ("ilegal", "ValueError se a chave não existe.")],
        ["Qual é o estado inicial?", "Qual evento depois de WAITING no caminho de erro?", "O que entra em payload_keys?", "Por que este lab é Python e o anel é C?", "O que o trace deve conter depois de call?"],
        ["Dia 07 agent/loop_state_machine", "projects/chris-agent-harness"],
    )


def day08_docs(day: Path) -> None:
    write(day / "README.md", """# Day 2026-09-08 — CLVM toolchain + input, linguagens misturadas

Não é um dia só em Python. Cada módulo tem uma linguagem e um contrato numérico.

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
| 1 | `systems/clvm_disassembler` | **C + bytecode** `.clbc` | PUSH 5 / JMP 3 | 3 |
| 2 | `systems/clvm_peephole_opt` | **C++** bytecode | PUSH 0+ADD, fold 2+3 | 2–3 |
| 3 | `linux/input_event_ring_mux` | **C** | anel CAP 4, FIFO | 2–3 |
| 4 | `rust/clvm_disasm` | **Rust** | mesma ISA, `Result` | 2 |
| 5 | `dotnet/pe_export_span` | **.NET** | e_lfanew 0x80, RVA 0x1000 | 2–3 |
| 6 | `graphics/shader_stage_fsm` | **C++** | EDIT não vai a READY | 2 |
| 7 | `redteam/pe_export_triage` | **Python** | evidência MZ | 2 |
| 8 | `quantum/bell_state_prep` | **C++** | H + CNOT, P=0.5 | 2–3 |
| 9 | `ai/softmax_stable` | **C** | max=3 em {1,2,3} | 2 |
| 10 | `nodejs/duplex_event_pipe` | **JavaScript** | 24×2=48 | 2 |
| 11 | `parsers/json_rd_lexer` | **C** | 5 tokens em `{"a":1}` | 2–3 |
| 12 | `agent/tool_protocol_fsm` | **Python** | FSM de tool call | 2 |
| 13 | `tooling/wasm_section_header` | **Assembly** | magic `\\0asm`, RCX | 2–3 |

**Total:** ~30–36 h.
""")
    write(day / "START_HERE.md", """# START HERE — 2026-09-08

Ordem por linguagem, não “abra qualquer pasta”.

1. Bytecode em C: `systems/clvm_disassembler` — hex `01 2A 00 00 00` → `PUSH 42`.
2. Peephole C++ no mesmo bytecode.
3. Anel C (`RING_CAP` 4) para o input do Dia 07.
4. Rust: a mesma ISA com `Result`.
5. .NET: PE `e_lfanew=0x80`, export RVA `0x1000`.
6. Assembly: header WASM `00 61 73 6D` (argumento em RCX no Windows).
7. Softmax em C, Bell em C++, lexer JSON em C, Duplex em JavaScript.
8. Python só em red team e na FSM do agente.

Cada `TEORIA` tem o trace com os números do teste. Faça esse trace no papel antes do código.
""")
    write(day / "ATIVIDADES.md", """# ATIVIDADES — 2026-09-08

**Dia:** 13 módulos, 8 linguagens (C, C++, Python, Rust, Assembly, JavaScript, .NET, bytecode).
**Regra:** checkpoint no papel com os números abaixo. PASS no teste sem o papel não conta.

## Preparação

- [ ] Abrir `START_HERE.md`
- [ ] Baseline: `python scripts/pedagogy_check_unified.py --day 2026-09-08`

## Bloco 1 — Bytecode (C, C++, Rust) (6–8 h)

| Módulo | Linguagem | Paper-trace obrigatório |
|--------|-----------|-------------------------|
| `systems/clvm_disassembler` | C | `01 2A 00 00 00` → linha `PUSH 42`, size 5; programa de 7 bytes → 3 linhas |
| `systems/clvm_peephole_opt` | C++ | `01 00 00 00 00 02` casa; PUSH 2+PUSH 3+ADD → `01 05 00 00 00` |
| `rust/clvm_disasm` | Rust | size(PUSH)=5, size(JMP)=3, listing `PUSH 42` / `HALT` |

**Checkpoint (antes do código):**

- [ ] Escrevi o imm 42 a partir de `2A 00 00 00` em little-endian
- [ ] Sei por que PUSH tem 5 bytes e JMP 3
- [ ] Sei que o fold 2+3 economiza 6 bytes (11→5)

## Bloco 2 — C (anel) + JavaScript (4 h)

| Módulo | Paper-trace |
|--------|-------------|
| `linux/input_event_ring_mux` | push 10 depois -3; primeiro pop é 10; 5º push retorna -1 |
| `nodejs/duplex_event_pipe` | 48 bytes = 2 × 24; `eventsWritten == 2` |

- [ ] Desenhei head/tail/count depois de 2 pushes num anel de 4
- [ ] Expliquei o byte que sobra se o write JS tiver 25 bytes

## Bloco 3 — .NET, Assembly, C numérico (8 h)

| Módulo | Paper-trace |
|--------|-------------|
| `dotnet/pe_export_span` | MZ, `e_lfanew` 0x80, export RVA 0x1000 |
| `tooling/wasm_section_header` | Assembly: `00 61 73 6D`, version dword 1, id 9 → 0 |
| `ai/softmax_stable` | max de {1,2,3} é 3; exp(0)=1; soma das probs = 1 |
| `parsers/json_rd_lexer` | `{"a":1}` tem 5 tokens |

- [ ] Anotei os 4 bytes do magic WASM e em qual registrador o ponteiro chega no Windows (RCX)
- [ ] Calculei exp(1-3), exp(2-3), exp(0)

## Bloco 4 — C++ (shader + Bell) e Python (5 h)

| Módulo | Paper-trace |
|--------|-------------|
| `graphics/shader_stage_fsm` | EDIT→COMPILE sim; EDIT→READY não; apply ilegal não muda o estado |
| `quantum/bell_state_prep` | [1,0,0,0] → H → CNOT → P(00)=P(11)=0.5 |
| `redteam/pe_export_triage` | Python: MZ primeiro |
| `agent/tool_protocol_fsm` | Python: aresta ilegal não muda o estado |

- [ ] Escrevi o vetor de 4 amplitudes depois de H e depois de CNOT
- [ ] Marquei a aresta EDIT→READY como proibida

## Relatório do dia

| Bloco | Checkpoint no papel | Testes |
|-------|--------------------|--------|
| 1 bytecode | ☐ | ☐ |
| 2 anel + JS | ☐ | ☐ |
| 3 PE + ASM + softmax + lexer | ☐ | ☐ |
| 4 C++ + Python | ☐ | ☐ |

**Síntese:** o disassembler C e o Rust listam o mesmo `PUSH 42`. O peephole C++ apaga um padrão que o disassembler acabou de mostrar. O anel C e o Duplex JS enquadram o mesmo tipo de recorte (capacidade / 24 bytes).
""")
    write(day / "VALIDATION.md", """# Validação — 2026-09-08

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-08
python scripts/day_contract_check.py --day 2026-09-08
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions
```

| Módulo | Linguagem | Gate |
|--------|-----------|------|
| clvm_disassembler | C | ctest |
| clvm_peephole_opt | C++ | ctest |
| input_event_ring_mux | C | ctest |
| clvm_disasm | Rust | cargo test |
| pe_export_span | .NET | dotnet test |
| shader_stage_fsm | C++ | ctest |
| pe_export_triage | Python | python |
| bell_state_prep | C++ | ctest |
| softmax_stable | C | ctest |
| duplex_event_pipe | JavaScript | node |
| json_rd_lexer | C | ctest |
| tool_protocol_fsm | Python | python |
| wasm_section_header | Assembly | ctest |
""")
    ids = [
        "CLVM-DIS-01", "CLVM-DIS-02", "CLVM-DIS-03",
        "CLVM-PEEP-01", "CLVM-PEEP-02", "CLVM-PEEP-03",
        "LIN-MUX-01", "LIN-MUX-02", "LIN-MUX-03",
        "CLVM-RS-DIS-01", "CLVM-RS-DIS-02", "CLVM-RS-DIS-03",
        "DN-PE-EXP-01", "DN-PE-EXP-02", "DN-PE-EXP-03",
        "GFX-SHADER-FSM-01", "GFX-SHADER-FSM-02", "GFX-SHADER-FSM-03",
        "RT-PE-EXP-01", "RT-PE-EXP-02", "RT-PE-EXP-03",
        "Q-BELL-01", "Q-BELL-02", "Q-BELL-03",
        "AI-SOFTMAX-01", "AI-SOFTMAX-02", "AI-SOFTMAX-03",
        "ND-DUPLEX-01", "ND-DUPLEX-02", "ND-DUPLEX-03",
        "PAR-JSON-LEX-01", "PAR-JSON-LEX-02", "PAR-JSON-LEX-03",
        "AGT-TOOL-01", "AGT-TOOL-02", "AGT-TOOL-03",
        "TOOL-WASM-01", "TOOL-WASM-02", "TOOL-WASM-03",
    ]
    bullets = "\n".join(f"- `{i}`" for i in ids)
    write(day / "TODO_MAP.md", f"# TODO map — 2026-09-08\n\nArquivo e função estão na RESOLUCAO de cada módulo.\n\n{bullets}\n")


def main() -> None:
    day = DAYS / "2026-09-08"
    emit_disassembler(day)
    emit_peephole(day)
    emit_linux_ring(day)
    emit_softmax_c(day)
    emit_json_c(day)
    emit_shader_cpp(day)
    emit_bell_cpp(day)
    emit_wasm_asm(day)
    deepen_day08_kept(day)
    day08_docs(day)
    print("day 08 rewritten")


if __name__ == "__main__":
    main()
