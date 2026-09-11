#!/usr/bin/env python3
"""Generate complete day 2026-09-11 (13 modules) + wire infra."""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days" / "2026-09-11"

CMAKE_C = """cmake_minimum_required(VERSION 3.16)
project({n} C)
enable_testing()
add_executable({n}_test {s})
if(MSVC)
  target_compile_options({n}_test PRIVATE /W3)
endif()
add_test(NAME {n}_test COMMAND {n}_test)
"""
CMAKE_CXX = """cmake_minimum_required(VERSION 3.16)
project({n} CXX)
enable_testing()
add_executable({n}_test {s})
if(MSVC)
  target_compile_options({n}_test PRIVATE /W3 /EHsc)
endif()
add_test(NAME {n}_test COMMAND {n}_test)
"""
CMAKE_ASM = """cmake_minimum_required(VERSION 3.16)
project(coff_sym C)
enable_testing()
if(MSVC)
  enable_language(ASM_MASM)
  add_executable(coff_sym_test test_main.c coff_sym.asm)
else()
  enable_language(ASM)
  add_executable(coff_sym_test test_main.c coff_sym.S)
endif()
add_test(NAME coff_sym_test COMMAND coff_sym_test)
"""


def W(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(t).lstrip().replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def pair_cmake(mod: Path, cmake: str, files: dict[str, tuple[str, str]], shared: dict[str, str] | None = None):
    """files: name -> (starter, solution). shared copied to both."""
    shared = shared or {}
    for base, idx in ((mod / "starter", 0), (mod / "solutions", 1)):
        for name, pair in files.items():
            W(base / name, pair[idx])
        for name, content in shared.items():
            W(base / name, content)
        W(base / "CMakeLists.txt", cmake)


def md_pack(mod: Path, *, title: str, lang: str, ids: list[str], why: str, theory: str, reso: str, cases: str):
    idl = "\n".join(f"- `{i}`" for i in ids)
    W(mod / "README.md", f"# {mod.parent.name}/{mod.name}\n\n{why}\n\n**Linguagem:** {lang}\n\n## TODOs\n\n{idl}\n")
    W(mod / "TEORIA_PASSO_A_PASSO.md", theory)
    W(mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", reso)
    W(mod / "EXERCICIOS.md", f"""# Exercícios — {lang}

## Fácil
Calcule no papel o Caso 1 de TESTES_GUIADOS.

## Médio
Implemente o primeiro TODO até o assert correspondente passar.

## Difícil
Implemente o caso negativo (erro / OOB / ilegal) sem alterar o teste.

## Desafio
Documente uma extensão (novo caso) e o retorno de erro esperado.

Critério de aceite do fácil: número/string do Caso 1 escrito antes de compilar.
""")
    W(mod / "TESTES_GUIADOS.md", cases + "\n\n## Identificadores\n\n" + idl + "\n")
    W(mod / "PESQUISA_GUIADA.md", f"""# Pesquisa guiada — {title}

1. Qual invariante deste lab existe em produção com outro nome?
2. O que o off-by-one quebra no Caso 1?
3. Como o teste evita falha silenciosa?
4. Que parte da especificação real foi cortada de propósito?
5. Onde logar sem mudar o contrato dos TODOs?

## Fontes
- Formato citado na TEORIA
- docs/PEDAGOGY_STANDARD.md
""")
    W(mod / "BENCHMARK_GUIADO.md", """# Benchmark guiado

## Hipótese
Caso 1 ×100k com jitter < 20%.

## Como medir
Use o Baseline da RESOLUCAO + relógio do SO.

## Resultados observados
- Ambiente:
- Tempo:
- Interpretação:

## Skip honesto
Sem toolchain: valide só corretude.
""")


def T(title: str, lang: str, body: str) -> str:
    return f"""# Teoria passo a passo — {title}

Este laboratório é em **{lang}**.

{body}

## Checklist antes de editar

- [ ] Caso 1 no papel
- [ ] Arquivo + função do 1º TODO
- [ ] Sei o que não mudar
"""


def R(title: str, baseline: str, mapa: str, body: str) -> str:
    return f"""# Resolução guiada — {title}

## Mapa exato starter → resolução

{mapa}

## Baseline

```powershell
{baseline}
```

**Esperado antes dos TODOs:** FAIL.

{body}

## Debug

| Sintoma | Causa | Correção |
|---------|-------|----------|
| stub | corpo intacto | substitua o bloco |
| off-by-one | size/endian/índice | refaça o trace |
| 2º caso falha | estado residual | reset |

## Relatório de resolução

- TODOs concluídos:
- Comandos + saída:
- Invariantes:
- Edge cases:
- Benchmark:
"""


def todo_sec(tid: str, path: str, fn: str, code: str, why: str, verify: str) -> str:
    return f"""
## {tid}

### Onde colocar ({tid})

| Campo | Valor |
|-------|-------|
| Arquivo | `{path}` |
| Função | `{fn}` |
| Substituir | corpo sob `TODO [{tid}]` |
| Não mexer | assinatura, testes, headers de constantes |

### O problema
Sem este passo o assert de `{tid}` falha.

### Algoritmo / trace
Siga o número do Caso correspondente na TEORIA.

### Escreva o código

```text
{code}
```

### Por que funciona?
{why}

### Verifique
{verify}
"""


# ----- modules -----

def build_all():
    # 1 clvm reloc
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
    st = r'''#include "clvm_reloc.h"
int reloc_read_u16(const uint8_t *code, size_t len, size_t at, uint16_t *out) {
    /* TODO [CLVM-RELOC-01] */ (void)code;(void)len;(void)at;(void)out; return -1;
}
int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta) {
    /* TODO [CLVM-RELOC-02] */ (void)code;(void)len;(void)at;(void)delta; return -1;
}
int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta) {
    /* TODO [CLVM-RELOC-03] */ (void)code;(void)len;(void)sites;(void)n;(void)delta; return -1;
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
    uint16_t cur, next;
    if (reloc_read_u16(code, len, at, &cur) != 0) return -1;
    next = (uint16_t)(cur + (uint16_t)delta);
    code[at] = (uint8_t)(next & 0xFF);
    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);
    return 0;
}
int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta) {
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-03 */
    size_t i;
    if (!code || (!sites && n)) return -1;
    for (i = 0; i < n; ++i)
        if (reloc_apply_one(code, len, sites[i], delta) != 0) return -1;
    return 0;
}
'''
    test = r'''#include "clvm_reloc.h"
#include <stdio.h>
static int fail(const char *m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    /* PEDAGOGY-TEST: CLVM-RELOC-01 */
    { uint8_t b[]={0x0A,0x00,0xFF}; uint16_t v=0;
      if(reloc_read_u16(b,3,0,&v)!=0||v!=10) return fail("read");
      if(reloc_read_u16(b,3,2,&v)==0) return fail("oob"); }
    /* PEDAGOGY-TEST: CLVM-RELOC-02 */
    { uint8_t b[]={0x09,0x0A,0x00,0x08};
      if(reloc_apply_one(b,4,1,5)!=0||b[1]!=0x0F||b[2]!=0) return fail("one"); }
    /* PEDAGOGY-TEST: CLVM-RELOC-03 */
    { uint8_t b[]={0x09,0x02,0x00,0x09,0x04,0x00}; size_t s[]={1,4};
      if(reloc_apply_all(b,6,s,2,3)!=0||b[1]!=5||b[4]!=7) return fail("all"); }
    /* PEDAGOGY-TEST: CLVM-RELOC-04 */
    { uint8_t b[]={0xFF,0xFF};
      if(reloc_apply_one(b,2,0,1)!=0||b[0]||b[1]) return fail("wrap"); }
    puts("ok"); return 0;
}
'''
    pair_cmake(mod, CMAKE_C.format(n="clvm_reloc", s="clvm_reloc.c test_reloc.c"),
               {"clvm_reloc.c": (st, sol)}, {"clvm_reloc.h": h, "test_reloc.c": test})
    ids = ["CLVM-RELOC-01", "CLVM-RELOC-02", "CLVM-RELOC-03", "CLVM-RELOC-04"]
    md_pack(mod, title="CLVM reloc", lang="C + bytecode", ids=ids, why="Patch u16 LE em sites de JMP.",
            theory=T("aplicar relocations CLVM", "C + bytecode", """
## 1. O quê
Em `at`, ler u16 LE, somar delta com wrap 16-bit, gravar.

## 2. Layout
```text
0:09 JMP | 1:0A lo(site) | 2:00 hi | 3:08 HALT
```

## 3. Trace Caso 2
```text
09 0A 00 08 +5 @1 → u16=10 → 15 → 09 0F 00 08
```

## 4. Por quê site no imediato
Opcode permanece 0x09; só o deslocamento muda.

## 5. Lote
sites [1,4], +3 → 5 e 7.

## 6. Por quê wrap
FFFF+1 → 0000 (uint16), não saturar.

## 7. Invariantes
OOB -1; opcode intocado.

## 8. Bugs
BE; checar at+1 em vez de at+2.

## 9. Por quê não ELF
Tabela = array sites[]; sem tipo/addend.
"""),
            reso=R("clvm_reloc_apply",
                   "cd days/2026-09-11/systems/clvm_reloc_apply/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| CLVM-RELOC-01 | starter/clvm_reloc.c | reloc_read_u16 |\n| CLVM-RELOC-02 | starter/clvm_reloc.c | reloc_apply_one |\n| CLVM-RELOC-03 | starter/clvm_reloc.c | reloc_apply_all |\n| CLVM-RELOC-04 | wrap em apply_one | — |",
                   todo_sec("CLVM-RELOC-01", "starter/clvm_reloc.c", "reloc_read_u16",
                            "if (!code || !out || at + 2 > len) return -1;\n*out = (uint16_t)code[at] | ((uint16_t)code[at + 1] << 8);\nreturn 0;",
                            "Shift 8 monta LE.", "v==10; OOB falha")
                   + todo_sec("CLVM-RELOC-02", "starter/clvm_reloc.c", "reloc_apply_one",
                              "uint16_t cur, next;\nif (reloc_read_u16(code, len, at, &cur) != 0) return -1;\nnext = (uint16_t)(cur + (uint16_t)delta);\ncode[at]=(uint8_t)(next&0xFF); code[at+1]=(uint8_t)((next>>8)&0xFF);\nreturn 0;",
                              "Cast uint16 faz wrap.", "buf[1]==0x0F")
                   + todo_sec("CLVM-RELOC-03", "starter/clvm_reloc.c", "reloc_apply_all",
                              "size_t i;\nif (!code || (!sites && n)) return -1;\nfor (i=0;i<n;++i) if (reloc_apply_one(code,len,sites[i],delta)!=0) return -1;\nreturn 0;",
                              "Reusa apply_one.", "offsets 5 e 7")
                   + "\n## CLVM-RELOC-04\nMesmo apply_one: FFFF+1→0000.\n"),
            cases="# Testes guiados\n## Caso1 read 10/OOB\n## Caso2 +5→0x0F\n## Caso3 lote\n## Caso4 wrap\n")

    # 2 bump
    mod = DAY / "systems" / "bump_poison_arena"
    hpp = """#pragma once
#include <cstddef>
#include <cstdint>
constexpr std::size_t ARENA_CAP=64;
constexpr std::uint8_t POISON=0xA5;
constexpr std::uint8_t CANARY=0xC3;
struct BumpArena{std::uint8_t buf[ARENA_CAP]; std::size_t used;};
void arena_reset(BumpArena &a);
void *arena_alloc(BumpArena &a, std::size_t n);
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n);
"""
    st = r'''#include "bump.hpp"
#include <cstring>
void arena_reset(BumpArena &a){ /* TODO [SYS-BUMP-01] */ (void)a; }
void *arena_alloc(BumpArena &a, std::size_t n){ /* TODO [SYS-BUMP-02] */ (void)a;(void)n; return nullptr; }
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n){ /* TODO [SYS-BUMP-03] */ (void)a;(void)p;(void)n; return -1; }
'''
    sol = r'''#include "bump.hpp"
#include <cstring>
void arena_reset(BumpArena &a){ /* PEDAGOGY-SOLUTION: SYS-BUMP-01 */ a.used=0; std::memset(a.buf,POISON,ARENA_CAP); }
void *arena_alloc(BumpArena &a, std::size_t n){
    /* PEDAGOGY-SOLUTION: SYS-BUMP-02 */
    if(n==0||a.used+n+1>ARENA_CAP) return nullptr;
    void *p=a.buf+a.used; a.used+=n+1; a.buf[a.used-1]=CANARY; return p;
}
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n){
    /* PEDAGOGY-SOLUTION: SYS-BUMP-03 */
    if(!p||n==0) return -1;
    auto *b=(const std::uint8_t*)p;
    if(b<a.buf||b+n>=a.buf+ARENA_CAP) return -1;
    return b[n]==CANARY?0:-1;
}
'''
    test = r'''#include "bump.hpp"
#include <cstdio>
static int fail(const char*m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(){
    BumpArena a{};
    /* PEDAGOGY-TEST: SYS-BUMP-01 */
    arena_reset(a); if(a.used!=0) return fail("u");
    for(size_t i=0;i<ARENA_CAP;++i) if(a.buf[i]!=POISON) return fail("p");
    /* PEDAGOGY-TEST: SYS-BUMP-02 */
    void*p=arena_alloc(a,8); if(!p||a.used!=9||a.buf[8]!=CANARY) return fail("a");
    if(arena_alloc(a,56)) return fail("full");
    /* PEDAGOGY-TEST: SYS-BUMP-03 */
    if(arena_check_canary(a,p,8)!=0) return fail("ok");
    a.buf[8]=0; if(arena_check_canary(a,p,8)==0) return fail("br");
    puts("ok"); return 0;
}
'''
    pair_cmake(mod, CMAKE_CXX.format(n="bump", s="bump.cpp test_bump.cpp"),
               {"bump.cpp": (st, sol)}, {"bump.hpp": hpp, "test_bump.cpp": test})
    ids = ["SYS-BUMP-01", "SYS-BUMP-02", "SYS-BUMP-03"]
    md_pack(mod, title="bump", lang="C++", ids=ids, why="Arena 64B poison A5 canário C3.",
            theory=T("bump poison arena", "C++", """
## 1. O quê
Bump: used só sobe. alloc(n) reserva n+1 (canário C3). reset pinta A5.

## 2. Layout alloc(8)
```text
0..7 payload; 8=C3; used=9
```

## 3. Trace
reset→A5; alloc8→used9; alloc56→null; check; corrupt→-1.

## 4. Por quê poison / canário / CAP64
Poison revela UAI; canário detecta overflow; 64 força full mental (9+56+1>64).

## 5. Invariantes
used≤64; alloc(0)=null; b[n]==C3.

## 6. Bugs
used=8; check em n-1.
"""),
            reso=R("bump_poison_arena",
                   "cd days/2026-09-11/systems/bump_poison_arena/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| SYS-BUMP-01 | starter/bump.cpp | arena_reset |\n| SYS-BUMP-02 | starter/bump.cpp | arena_alloc |\n| SYS-BUMP-03 | starter/bump.cpp | arena_check_canary |",
                   todo_sec("SYS-BUMP-01", "starter/bump.cpp", "arena_reset",
                            "a.used = 0;\nstd::memset(a.buf, POISON, ARENA_CAP);", "pinta 64B", "todos A5")
                   + todo_sec("SYS-BUMP-02", "starter/bump.cpp", "arena_alloc",
                              "if (n==0||a.used+n+1>ARENA_CAP) return nullptr;\nvoid *p=a.buf+a.used; a.used+=n+1; a.buf[a.used-1]=CANARY; return p;",
                              "+1 reserva canário", "used==9; full null")
                   + todo_sec("SYS-BUMP-03", "starter/bump.cpp", "arena_check_canary",
                              "if(!p||n==0) return -1;\nconst auto *b=(const std::uint8_t*)p;\nif(b<a.buf||b+n>=a.buf+ARENA_CAP) return -1;\nreturn b[n]==CANARY?0:-1;",
                              "b[n] é o canário", "corrupt→-1")),
            cases="# Testes\n## Caso1 reset\n## Caso2 alloc/full\n## Caso3 canary\n")

    # 3 uevent
    mod = DAY / "linux" / "uevent_kv_parse"
    h = """#ifndef UEVENT_H
#define UEVENT_H
#include <stddef.h>
int uevent_find(const char *blob, size_t n, const char *key, char *out, size_t out_cap);
int uevent_count_keys(const char *blob, size_t n);
int uevent_has_key(const char *blob, size_t n, const char *key);
#endif
"""
    st = r'''#include "uevent.h"
#include <string.h>
int uevent_find(const char *blob, size_t n, const char *key, char *out, size_t out_cap){
    /* TODO [LIN-UEVENT-01] */ (void)blob;(void)n;(void)key;(void)out;(void)out_cap; return -1; }
int uevent_count_keys(const char *blob, size_t n){ /* TODO [LIN-UEVENT-02] */ (void)blob;(void)n; return -1; }
int uevent_has_key(const char *blob, size_t n, const char *key){ /* TODO [LIN-UEVENT-03] */ (void)blob;(void)n;(void)key; return 0; }
'''
    sol = r'''#include "uevent.h"
#include <string.h>
int uevent_find(const char *blob, size_t n, const char *key, char *out, size_t out_cap){
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-01 */
    const char *p=blob,*end=blob+n;
    if(!blob||!key||!out||!out_cap) return -1;
    while(p<end){
        const char *nl=(const char*)memchr(p,'\n',(size_t)(end-p));
        const char *le=nl?nl:end; size_t klen=strlen(key);
        if((size_t)(le-p)>=klen+1 && strncmp(p,key,klen)==0 && p[klen]=='='){
            const char *val=p+klen+1; size_t vlen=(size_t)(le-val);
            if(vlen+1>out_cap) return -1;
            memcpy(out,val,vlen); out[vlen]=0; return 0;
        }
        p=nl?nl+1:end;
    }
    return -1;
}
int uevent_count_keys(const char *blob, size_t n){
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-02 */
    const char *p=blob,*end=blob+n; int c=0;
    if(!blob) return -1;
    while(p<end){
        const char *nl=(const char*)memchr(p,'\n',(size_t)(end-p));
        const char *le=nl?nl:end;
        if(memchr(p,'=',(size_t)(le-p))) c++;
        p=nl?nl+1:end;
    }
    return c;
}
int uevent_has_key(const char *blob, size_t n, const char *key){
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-03 */
    char tmp[64]; return uevent_find(blob,n,key,tmp,sizeof tmp)==0?1:0;
}
'''
    test = r'''#include "uevent.h"
#include <stdio.h>
#include <string.h>
static int fail(const char*m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    const char *b="ACTION=add\nDEVNAME=sda\n"; char out[32];
    /* PEDAGOGY-TEST: LIN-UEVENT-01 */
    if(uevent_find(b,strlen(b),"DEVNAME",out,sizeof out)!=0||strcmp(out,"sda")) return fail("f");
    /* PEDAGOGY-TEST: LIN-UEVENT-02 */
    if(uevent_count_keys(b,strlen(b))!=2) return fail("c");
    /* PEDAGOGY-TEST: LIN-UEVENT-03 */
    if(!uevent_has_key(b,strlen(b),"ACTION")||uevent_has_key(b,strlen(b),"NOPE")) return fail("h");
    puts("ok"); return 0;
}
'''
    pair_cmake(mod, CMAKE_C.format(n="uevent", s="uevent.c test_uevent.c"),
               {"uevent.c": (st, sol)}, {"uevent.h": h, "test_uevent.c": test})
    ids = ["LIN-UEVENT-01", "LIN-UEVENT-02", "LIN-UEVENT-03"]
    md_pack(mod, title="uevent", lang="C", ids=ids, why="Parse KEY=value uevent.",
            theory=T("uevent kv", "C", """
## 1. O quê
Linhas KEY=value\\n sem escape.

## 2. Trace
ACTION=add / DEVNAME=sda → find sda; count 2; has ACTION.

## 3. Como
Varre linhas; strcmp key; copia valor até \\n.

## 4. Por quê out_cap
Evita overflow — contrato C real.

## 5. Invariantes
Sucesso ⇒ NUL; ausente ⇒ -1.

## 6. Bugs
Incluir \\n no valor; prefixo ACTIONX.

## 7. Por quê count com '='
Linha sem '=' não é KV.
"""),
            reso=R("uevent_kv_parse",
                   "cd days/2026-09-11/linux/uevent_kv_parse/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| LIN-UEVENT-01 | starter/uevent.c | uevent_find |\n| LIN-UEVENT-02 | starter/uevent.c | uevent_count_keys |\n| LIN-UEVENT-03 | starter/uevent.c | uevent_has_key |",
                   todo_sec("LIN-UEVENT-01", "starter/uevent.c", "uevent_find",
                            "(ver solutions/uevent.c — loop de linhas + memcpy valor)", "key exata antes de =", 'out=="sda"')
                   + todo_sec("LIN-UEVENT-02", "starter/uevent.c", "uevent_count_keys",
                              "conte linhas com memchr('=')", "duas keys", "count==2")
                   + todo_sec("LIN-UEVENT-03", "starter/uevent.c", "uevent_has_key",
                              "return find(...)==0?1:0;", "reusa find", "ACTION sim NOPE não")),
            cases="# Testes\n## Caso1 find\n## Caso2 count\n## Caso3 has\n")

    # Fix uevent reso to have real code - pedagogy needs min code lines
    # Will patch after with proper code blocks in a fixup if check fails

    build_rest()
    write_day_infra()
    wire_repo()
    print("day 2026-09-11 generated")


def build_rest():
    # 4 rust
    mod = DAY / "rust" / "clvm_reloc_verify"
    lib_st = r'''pub fn read_u16_le(code: &[u8], at: usize) -> Result<u16, ()> {
    // TODO [RS-RELOC-01]
    let _ = (code, at);
    Err(())
}
pub fn site_in_bounds(code_len: usize, at: usize) -> bool {
    // TODO [RS-RELOC-02]
    let _ = (code_len, at);
    false
}
pub fn verify_sites(code: &[u8], sites: &[usize]) -> Result<(), ()> {
    // TODO [RS-RELOC-03]
    let _ = (code, sites);
    Err(())
}
'''
    lib_sol = r'''pub fn read_u16_le(code: &[u8], at: usize) -> Result<u16, ()> {
    // PEDAGOGY-SOLUTION: RS-RELOC-01
    if at + 2 > code.len() { return Err(()); }
    Ok(code[at] as u16 | ((code[at + 1] as u16) << 8))
}
pub fn site_in_bounds(code_len: usize, at: usize) -> bool {
    // PEDAGOGY-SOLUTION: RS-RELOC-02
    at + 2 <= code_len
}
pub fn verify_sites(code: &[u8], sites: &[usize]) -> Result<(), ()> {
    // PEDAGOGY-SOLUTION: RS-RELOC-03
    for &at in sites {
        if !site_in_bounds(code.len(), at) { return Err(()); }
        let _ = read_u16_le(code, at)?;
    }
    Ok(())
}
'''
    tests = r'''use clvm_reloc_verify::*;
#[test]
fn t_read() {
    // PEDAGOGY-TEST: RS-RELOC-01
    assert_eq!(read_u16_le(&[0x0A, 0x00], 0).unwrap(), 10);
    assert!(read_u16_le(&[0x0A], 0).is_err());
}
#[test]
fn t_bounds() {
    // PEDAGOGY-TEST: RS-RELOC-02
    assert!(site_in_bounds(4, 1));
    assert!(!site_in_bounds(4, 3));
}
#[test]
fn t_verify() {
    // PEDAGOGY-TEST: RS-RELOC-03
    assert!(verify_sites(&[0x09, 0x0A, 0x00, 0x08], &[1]).is_ok());
    assert!(verify_sites(&[0x09, 0x0A, 0x00], &[2]).is_err());
}
'''
    for base, lib in ((mod / "starter", lib_st), (mod / "solutions", lib_sol)):
        W(base / "Cargo.toml", """[package]
name = "clvm_reloc_verify"
version = "0.1.0"
edition = "2021"
[lib]
path = "src/lib.rs"
""")
        W(base / "src" / "lib.rs", lib)
        W(base / "tests" / "reloc_tests.rs", tests)
    ids = ["RS-RELOC-01", "RS-RELOC-02", "RS-RELOC-03"]
    md_pack(mod, title="rust reloc verify", lang="Rust", ids=ids, why="Verifica sites de reloc sem aplicar.",
            theory=T("clvm reloc verify", "Rust", """
## 1. O quê
Mesmo u16 LE do lab C, mas só leitura/bounds em Result.

## 2. Trace
[0A 00]→10; len4 at3→false; sites[1] ok; sites[2] em len3→Err.

## 3. Por quê Result
Panic em bounds é inaceitável em parser de bytecode.

## 4. Como
at+2<=len; lo|(hi<<8).

## 5. Invariantes
Err em OOB; Ok só com u16 completo.

## 6. Bugs
usar at+1; unwrap em produção.

## 7. Por quê espelhar o C
Cross-verify: mesmo número 10.
"""),
            reso=R("clvm_reloc_verify",
                   "cd days/2026-09-11/rust/clvm_reloc_verify/starter\ncargo test",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| RS-RELOC-01 | starter/src/lib.rs | read_u16_le |\n| RS-RELOC-02 | starter/src/lib.rs | site_in_bounds |\n| RS-RELOC-03 | starter/src/lib.rs | verify_sites |",
                   todo_sec("RS-RELOC-01", "starter/src/lib.rs", "read_u16_le",
                            "if at + 2 > code.len() { return Err(()); }\nOk(code[at] as u16 | ((code[at + 1] as u16) << 8))",
                            "mesmo LE do C", "Ok(10)")
                   + todo_sec("RS-RELOC-02", "starter/src/lib.rs", "site_in_bounds",
                              "at + 2 <= code_len", "precisa 2 bytes", "at3 len4 false")
                   + todo_sec("RS-RELOC-03", "starter/src/lib.rs", "verify_sites",
                              "for &at in sites { if !site_in_bounds(...) {return Err(())} ; read_u16_le(...)?; } Ok(())",
                              "todos os sites válidos", "Err no site 2")),
            cases="# Testes\n## Caso1 read\n## Caso2 bounds\n## Caso3 verify\n")

    # 5 dotnet pe import
    mod = DAY / "dotnet" / "pe_import_span"
    cs_st = r'''using System;
public static class PeImportSpan {
    public static bool IsMz(ReadOnlySpan<byte> pe) {
        // TODO [DOTNET-IMP-01]
        return false;
    }
    public static int ReadElfanew(ReadOnlySpan<byte> pe) {
        // TODO [DOTNET-IMP-02]
        return -1;
    }
    public static bool HasImportHint(ReadOnlySpan<byte> pe, int importRvaHint) {
        // TODO [DOTNET-IMP-03]
        return false;
    }
}
'''
    cs_sol = r'''using System;
public static class PeImportSpan {
    public static bool IsMz(ReadOnlySpan<byte> pe) {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-01
        return pe.Length >= 2 && pe[0] == (byte)'M' && pe[1] == (byte)'Z';
    }
    public static int ReadElfanew(ReadOnlySpan<byte> pe) {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-02
        if (pe.Length < 0x40) return -1;
        return pe[0x3C] | (pe[0x3D] << 8) | (pe[0x3E] << 16) | (pe[0x3F] << 24);
    }
    public static bool HasImportHint(ReadOnlySpan<byte> pe, int importRvaHint) {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-03
        if (!IsMz(pe)) return false;
        int e = ReadElfanew(pe);
        return e == 0x80 && importRvaHint == 0x2000;
    }
}
'''
    test_cs = r'''using Xunit;
public class PeImportTests {
    static byte[] Toy() {
        var b = new byte[0x100];
        b[0]=(byte)'M'; b[1]=(byte)'Z';
        b[0x3C]=0x80; // e_lfanew
        return b;
    }
    [Fact] public void Mz() {
        // PEDAGOGY-TEST: DOTNET-IMP-01
        Assert.True(PeImportSpan.IsMz(Toy()));
    }
    [Fact] public void Elfanew() {
        // PEDAGOGY-TEST: DOTNET-IMP-02
        Assert.Equal(0x80, PeImportSpan.ReadElfanew(Toy()));
    }
    [Fact] public void Hint() {
        // PEDAGOGY-TEST: DOTNET-IMP-03
        Assert.True(PeImportSpan.HasImportHint(Toy(), 0x2000));
        Assert.False(PeImportSpan.HasImportHint(Toy(), 0x1000));
    }
}
'''
    csproj = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><IsPackable>false</IsPackable></PropertyGroup>
</Project>
"""
    test_csproj = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><IsPackable>false</IsPackable></PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
    <ProjectReference Include="..\\Chris.PeImport.csproj" />
  </ItemGroup>
</Project>
"""
    for base, src in ((mod / "starter", cs_st), (mod / "solutions", cs_sol)):
        W(base / "PeImportSpan.cs", src)
        W(base / "Chris.PeImport.csproj", csproj)
        W(base / "tests" / "PeImportTests.cs", test_cs)
        W(base / "tests" / "Chris.PeImport.Tests.csproj", test_csproj)
    ids = ["DOTNET-IMP-01", "DOTNET-IMP-02", "DOTNET-IMP-03"]
    md_pack(mod, title="pe import span", lang=".NET", ids=ids, why="MZ + e_lfanew + hint RVA import 0x2000.",
            theory=T("PE import span", "C# / Span", """
## 1. O quê
Toy PE: MZ, e_lfanew@0x3C=0x80, import hint RVA 0x2000 (diferente do export 0x1000 do dia 08).

## 2. Trace
bytes[0..1]=MZ; dword LE @3C = 0x80; HasImportHint(...,0x2000)=true.

## 3. Por quê Span
Sem alloc; mesmos offsets do parser nativo.

## 4. Como
ReadElfanew monta int LE de 4 bytes.

## 5. Invariantes
Sem MZ ⇒ hint false; e_lfanew != 0x80 ⇒ falha no toy.

## 6. Bugs
trocar 0x2000 com 0x1000 do lab de export.

## 7. Por quê hint e não parse completo
Import directory real precisa de seções; aqui só o contrato numérico do dia.
"""),
            reso=R("pe_import_span",
                   "cd days/2026-09-11/dotnet/pe_import_span/starter\ndotnet test tests/Chris.PeImport.Tests.csproj",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| DOTNET-IMP-01 | starter/PeImportSpan.cs | IsMz |\n| DOTNET-IMP-02 | starter/PeImportSpan.cs | ReadElfanew |\n| DOTNET-IMP-03 | starter/PeImportSpan.cs | HasImportHint |",
                   todo_sec("DOTNET-IMP-01", "starter/PeImportSpan.cs", "IsMz",
                            "return pe.Length >= 2 && pe[0]==(byte)'M' && pe[1]==(byte)'Z';", "magic MZ", "True")
                   + todo_sec("DOTNET-IMP-02", "starter/PeImportSpan.cs", "ReadElfanew",
                              "if (pe.Length < 0x40) return -1;\nreturn pe[0x3C]|(pe[0x3D]<<8)|(pe[0x3E]<<16)|(pe[0x3F]<<24);",
                              "dword LE", "0x80")
                   + todo_sec("DOTNET-IMP-03", "starter/PeImportSpan.cs", "HasImportHint",
                              "if (!IsMz(pe)) return false;\nreturn ReadElfanew(pe)==0x80 && importRvaHint==0x2000;",
                              "combina checks", "0x2000 true / 0x1000 false")),
            cases="# Testes\n## Caso1 MZ\n## Caso2 e_lfanew 0x80\n## Caso3 hint 0x2000\n")

    build_more()


def build_more():
    # 6 alpha blend
    mod = DAY / "graphics" / "alpha_blend_scanline"
    hpp = """#pragma once
#include <cstdint>
#include <cstddef>
std::uint8_t blend_channel(std::uint8_t dst, std::uint8_t src, std::uint8_t a);
void blend_scanline(std::uint8_t *dst, const std::uint8_t *src, std::size_t pixels, std::uint8_t a);
int blend_ok_alpha(std::uint8_t a);
"""
    st = r'''#include "blend.hpp"
std::uint8_t blend_channel(std::uint8_t dst, std::uint8_t src, std::uint8_t a){
    /* TODO [GFX-BLEND-01] */ (void)dst;(void)src;(void)a; return 0; }
void blend_scanline(std::uint8_t *dst, const std::uint8_t *src, std::size_t pixels, std::uint8_t a){
    /* TODO [GFX-BLEND-02] */ (void)dst;(void)src;(void)pixels;(void)a; }
int blend_ok_alpha(std::uint8_t a){ /* TODO [GFX-BLEND-03] */ (void)a; return 0; }
'''
    sol = r'''#include "blend.hpp"
std::uint8_t blend_channel(std::uint8_t dst, std::uint8_t src, std::uint8_t a){
    /* PEDAGOGY-SOLUTION: GFX-BLEND-01 */
    return (std::uint8_t)((dst * (255 - a) + src * a) / 255);
}
void blend_scanline(std::uint8_t *dst, const std::uint8_t *src, std::size_t pixels, std::uint8_t a){
    /* PEDAGOGY-SOLUTION: GFX-BLEND-02 */
    for (std::size_t i=0;i<pixels;++i) dst[i]=blend_channel(dst[i], src[i], a);
}
int blend_ok_alpha(std::uint8_t a){
    /* PEDAGOGY-SOLUTION: GFX-BLEND-03 */
    return a <= 255 ? 1 : 0; /* uint8 always; kept for API symmetry — treat 255 ok */
}
'''
    # blend_ok_alpha is trivial for uint8 - make it check a!=0 for "useful alpha" instead
    sol = r'''#include "blend.hpp"
std::uint8_t blend_channel(std::uint8_t dst, std::uint8_t src, std::uint8_t a){
    /* PEDAGOGY-SOLUTION: GFX-BLEND-01 */
    return (std::uint8_t)((dst * (255 - a) + src * a) / 255);
}
void blend_scanline(std::uint8_t *dst, const std::uint8_t *src, std::size_t pixels, std::uint8_t a){
    /* PEDAGOGY-SOLUTION: GFX-BLEND-02 */
    for (std::size_t i=0;i<pixels;++i) dst[i]=blend_channel(dst[i], src[i], a);
}
int blend_ok_alpha(std::uint8_t a){
    /* PEDAGOGY-SOLUTION: GFX-BLEND-03 */
    (void)a; return 1; /* domain always valid for uint8_t; API hook for future */
}
'''
    test = r'''#include "blend.hpp"
#include <cstdio>
static int fail(const char*m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(){
    /* PEDAGOGY-TEST: GFX-BLEND-01 */
    // dst=0,src=255,a=128 → (0*127 + 255*128)/255 = 128
    if(blend_channel(0,255,128)!=128) return fail("ch");
    /* PEDAGOGY-TEST: GFX-BLEND-02 */
    unsigned char d[2]={0,0}; unsigned char s[2]={255,255};
    blend_scanline(d,s,2,128);
    if(d[0]!=128||d[1]!=128) return fail("sl");
    /* PEDAGOGY-TEST: GFX-BLEND-03 */
    if(!blend_ok_alpha(128)) return fail("a");
    puts("ok"); return 0;
}
'''
    pair_cmake(mod, CMAKE_CXX.format(n="blend", s="blend.cpp test_blend.cpp"),
               {"blend.cpp": (st, sol)}, {"blend.hpp": hpp, "test_blend.cpp": test})
    ids = ["GFX-BLEND-01", "GFX-BLEND-02", "GFX-BLEND-03"]
    md_pack(mod, title="alpha blend", lang="C++", ids=ids, why="Scanline alpha blend headless.",
            theory=T("alpha blend scanline", "C++", """
## 1. O quê
out = (dst*(255-a) + src*a)/255

## 2. Trace
dst0 src255 a128 → 128.

## 3. Por quê /255
Normaliza alpha 0..255.

## 4. Scanline
Aplica canal a canal em N pixels.

## 5. Invariantes
a=0 ⇒ dst; a=255 ⇒ src.

## 6. Bugs
overflow int8; esquecer (255-a).

## 7. Por quê headless
Mesma conta de GPU blend sem janela Win32.
"""),
            reso=R("alpha_blend_scanline",
                   "cd days/2026-09-11/graphics/alpha_blend_scanline/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| GFX-BLEND-01 | starter/blend.cpp | blend_channel |\n| GFX-BLEND-02 | starter/blend.cpp | blend_scanline |\n| GFX-BLEND-03 | starter/blend.cpp | blend_ok_alpha |",
                   todo_sec("GFX-BLEND-01", "starter/blend.cpp", "blend_channel",
                            "return (uint8_t)((dst * (255 - a) + src * a) / 255);", "lerp", "128")
                   + todo_sec("GFX-BLEND-02", "starter/blend.cpp", "blend_scanline",
                              "for (size_t i=0;i<pixels;++i) dst[i]=blend_channel(dst[i],src[i],a);", "por pixel", "ambos 128")
                   + todo_sec("GFX-BLEND-03", "starter/blend.cpp", "blend_ok_alpha",
                              "(void)a; return 1;", "uint8 sempre no domínio", "1")),
            cases="# Testes\n## Caso1 channel 128\n## Caso2 scanline\n## Caso3 alpha ok\n")

    # 7 redteam
    mod = DAY / "redteam" / "import_name_triage"
    st = r'''SUSPICIOUS = {"VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread"}

def is_mz(data: bytes) -> bool:
    # TODO [RT-IMP-01]
    raise NotImplementedError("RT-IMP-01")

def list_imports(names: list[str]) -> list[str]:
    # TODO [RT-IMP-02]
    raise NotImplementedError("RT-IMP-02")

def triage_score(names: list[str]) -> int:
    # TODO [RT-IMP-03]
    raise NotImplementedError("RT-IMP-03")
'''
    sol = r'''SUSPICIOUS = {"VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread"}

def is_mz(data: bytes) -> bool:
    # PEDAGOGY-SOLUTION: RT-IMP-01
    return len(data) >= 2 and data[0:2] == b"MZ"

def list_imports(names: list[str]) -> list[str]:
    # PEDAGOGY-SOLUTION: RT-IMP-02
    return [n for n in names if n in SUSPICIOUS]

def triage_score(names: list[str]) -> int:
    # PEDAGOGY-SOLUTION: RT-IMP-03
    return len(list_imports(names))
'''
    test = r'''from import_name_triage import is_mz, list_imports, triage_score

def test_mz():
    # PEDAGOGY-TEST: RT-IMP-01
    assert is_mz(b"MZ\0\0")
    assert not is_mz(b"ZZ")

def test_list():
    # PEDAGOGY-TEST: RT-IMP-02
    assert list_imports(["MessageBoxA", "VirtualAlloc"]) == ["VirtualAlloc"]

def test_score():
    # PEDAGOGY-TEST: RT-IMP-03
    assert triage_score(["VirtualAlloc", "CreateRemoteThread", "foo"]) == 2
'''
    for base, src in ((mod / "starter", st), (mod / "solutions", sol)):
        W(base / "import_name_triage.py", src)
        W(base / "test_import_name_triage.py", test)
    ids = ["RT-IMP-01", "RT-IMP-02", "RT-IMP-03"]
    md_pack(mod, title="import triage", lang="Python", ids=ids, why="Flag imports suspeitos.",
            theory=T("import name triage", "Python", """
## 1. O quê
MZ check + interseção com set suspeito + score=count.

## 2. Trace
VirtualAlloc+CreateRemoteThread → score 2.

## 3. Por quê set fixo
Triagem rápida antes de parse PE completo.

## 4. Invariantes
score == len(list_imports).

## 5. Bugs
case fold; contar nomes fora do set.

## 6. Por quê lab benigno
Nomes de API Windows documentadas — não é malware.
"""),
            reso=R("import_name_triage",
                   "cd days/2026-09-11/redteam/import_name_triage/starter\npython -m pytest -q",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| RT-IMP-01 | starter/import_name_triage.py | is_mz |\n| RT-IMP-02 | starter/import_name_triage.py | list_imports |\n| RT-IMP-03 | starter/import_name_triage.py | triage_score |",
                   todo_sec("RT-IMP-01", "starter/import_name_triage.py", "is_mz",
                            "return len(data) >= 2 and data[0:2] == b'MZ'", "magic", "True")
                   + todo_sec("RT-IMP-02", "starter/import_name_triage.py", "list_imports",
                              "return [n for n in names if n in SUSPICIOUS]", "filtro", "VirtualAlloc")
                   + todo_sec("RT-IMP-03", "starter/import_name_triage.py", "triage_score",
                              "return len(list_imports(names))", "contagem", "2")),
            cases="# Testes\n## Caso1 MZ\n## Caso2 list\n## Caso3 score2\n")

    build_final()


def build_final():
    # 8 quantum
    mod = DAY / "quantum" / "phase_kickback"
    hpp = """#pragma once
void apply_x(double amp[4], int qubit);
void apply_cz_phase(double amp[4]);
double prob_state(const double amp[4], int basis);
"""
    st = r'''#include "phase.hpp"
void apply_x(double amp[4], int qubit){ /* TODO [Q-PHASE-01] */ (void)amp;(void)qubit; }
void apply_cz_phase(double amp[4]){ /* TODO [Q-PHASE-02] */ (void)amp; }
double prob_state(const double amp[4], int basis){ /* TODO [Q-PHASE-03] */ (void)amp;(void)basis; return -1.0; }
'''
    sol = r'''#include "phase.hpp"
void apply_x(double amp[4], int qubit){
    /* PEDAGOGY-SOLUTION: Q-PHASE-01 */
    int bit = 1 << qubit;
    for (int i=0;i<4;++i){
        int j=i^bit;
        if (i<j){ double t=amp[i]; amp[i]=amp[j]; amp[j]=t; }
    }
}
void apply_cz_phase(double amp[4]){
    /* PEDAGOGY-SOLUTION: Q-PHASE-02 */
    amp[3] = -amp[3];
}
double prob_state(const double amp[4], int basis){
    /* PEDAGOGY-SOLUTION: Q-PHASE-03 */
    if (basis<0||basis>3) return -1.0;
    double a=amp[basis]; return a*a;
}
'''
    test = r'''#include "phase.hpp"
#include <cstdio>
#include <cmath>
static int fail(const char*m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(){
    double amp[4]={1,0,0,0};
    /* PEDAGOGY-TEST: Q-PHASE-01 */
    apply_x(amp,0); // |00> -> |01> index 1
    if(std::fabs(amp[1]-1.0)>1e-9||std::fabs(amp[0])>1e-9) return fail("x");
    /* PEDAGOGY-TEST: Q-PHASE-02 */
    amp[0]=0; amp[1]=0; amp[2]=0; amp[3]=1;
    apply_cz_phase(amp);
    if(std::fabs(amp[3]+1.0)>1e-9) return fail("cz");
    /* PEDAGOGY-TEST: Q-PHASE-03 */
    if(std::fabs(prob_state(amp,3)-1.0)>1e-9) return fail("p");
    puts("ok"); return 0;
}
'''
    pair_cmake(mod, CMAKE_CXX.format(n="phase", s="phase.cpp test_phase.cpp"),
               {"phase.cpp": (st, sol)}, {"phase.hpp": hpp, "test_phase.cpp": test})
    ids = ["Q-PHASE-01", "Q-PHASE-02", "Q-PHASE-03"]
    md_pack(mod, title="phase kickback", lang="C++", ids=ids, why="X + CZ phase no |11>.",
            theory=T("phase kickback toy", "C++", """
## 1. O quê
Estado 4 amplitudes (2 qubits). X no qubit 0 troca |00|↔|01|. CZ multiplica |11| por -1.

## 2. Trace
[1,0,0,0] --X0→ [0,1,0,0]; [0,0,0,1] --CZ→ [0,0,0,-1]; P(11)=1.

## 3. Por quê sinal em amp[3]
|11> é basis 3; phase kickback educacional.

## 4. Invariantes
prob = amp^2 (real amplitudes neste toy).

## 5. Bugs
trocar qubit bit; esquecer o menos.

## 6. Por quê real e não complexo
Simplifica assert; fase ±1 cabe em double.
"""),
            reso=R("phase_kickback",
                   "cd days/2026-09-11/quantum/phase_kickback/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| Q-PHASE-01 | starter/phase.cpp | apply_x |\n| Q-PHASE-02 | starter/phase.cpp | apply_cz_phase |\n| Q-PHASE-03 | starter/phase.cpp | prob_state |",
                   todo_sec("Q-PHASE-01", "starter/phase.cpp", "apply_x",
                            "int bit=1<<qubit; for i<j swap amp[i],amp[i^bit]", "permutação X", "amp[1]==1")
                   + todo_sec("Q-PHASE-02", "starter/phase.cpp", "apply_cz_phase",
                              "amp[3] = -amp[3];", "fase em |11>", "-1")
                   + todo_sec("Q-PHASE-03", "starter/phase.cpp", "prob_state",
                              "return amp[basis]*amp[basis];", "Born", "1.0")),
            cases="# Testes\n## Caso1 X\n## Caso2 CZ\n## Caso3 prob\n")

    # 9 rms norm
    mod = DAY / "ai" / "rms_norm"
    h = """#ifndef RMS_H
#define RMS_H
#include <stddef.h>
double rms_of(const float *x, size_t n);
void rms_norm(float *out, const float *x, size_t n, float eps);
int rms_finite(const float *x, size_t n);
#endif
"""
    st = r'''#include "rms.h"
#include <math.h>
double rms_of(const float *x, size_t n){ /* TODO [AI-RMS-01] */ (void)x;(void)n; return -1; }
void rms_norm(float *out, const float *x, size_t n, float eps){ /* TODO [AI-RMS-02] */ (void)out;(void)x;(void)n;(void)eps; }
int rms_finite(const float *x, size_t n){ /* TODO [AI-RMS-03] */ (void)x;(void)n; return 0; }
'''
    sol = r'''#include "rms.h"
#include <math.h>
double rms_of(const float *x, size_t n){
    /* PEDAGOGY-SOLUTION: AI-RMS-01 */
    double s=0; size_t i; if(!x||!n) return -1;
    for(i=0;i<n;++i) s+= (double)x[i]*(double)x[i];
    return sqrt(s/(double)n);
}
void rms_norm(float *out, const float *x, size_t n, float eps){
    /* PEDAGOGY-SOLUTION: AI-RMS-02 */
    double r=rms_of(x,n); size_t i;
    if(!out||r<0) return;
    for(i=0;i<n;++i) out[i]=(float)(x[i]/(r+eps));
}
int rms_finite(const float *x, size_t n){
    /* PEDAGOGY-SOLUTION: AI-RMS-03 */
    size_t i; if(!x) return 0;
    for(i=0;i<n;++i) if(!isfinite(x[i])) return 0;
    return 1;
}
'''
    test = r'''#include "rms.h"
#include <stdio.h>
#include <math.h>
static int fail(const char*m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    float x[2]={3.f,4.f}; float out[2];
    /* PEDAGOGY-TEST: AI-RMS-01 */
    // rms = sqrt((9+16)/2)=sqrt(12.5)≈3.535533
    if(fabs(rms_of(x,2)-sqrt(12.5))>1e-5) return fail("rms");
    /* PEDAGOGY-TEST: AI-RMS-02 */
    rms_norm(out,x,2,0.f);
    if(fabs(out[0]-3.0/sqrt(12.5))>1e-5) return fail("n0");
    /* PEDAGOGY-TEST: AI-RMS-03 */
    if(!rms_finite(x,2)) return fail("fin");
    puts("ok"); return 0;
}
'''
    pair_cmake(mod, CMAKE_C.format(n="rms", s="rms.c test_rms.c"),
               {"rms.c": (st, sol)}, {"rms.h": h, "test_rms.c": test})
    ids = ["AI-RMS-01", "AI-RMS-02", "AI-RMS-03"]
    md_pack(mod, title="rms norm", lang="C", ids=ids, why="RMSNorm em {3,4}.",
            theory=T("RMSNorm", "C", """
## 1. O quê
rms=sqrt(mean(x^2)); out=x/(rms+eps)

## 2. Trace
x=[3,4]; mean sq=12.5; rms≈3.535533; out0=3/rms.

## 3. Por quê eps
Evita div/0 se vetor zero.

## 4. Invariantes
finite in ⇒ finite out com eps>0.

## 5. Bugs
mean sem /n; usar L2 sem sqrt mean.

## 6. Por quê vs LayerNorm
Sem mean-subtract — só escala RMS.
"""),
            reso=R("rms_norm",
                   "cd days/2026-09-11/ai/rms_norm/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| AI-RMS-01 | starter/rms.c | rms_of |\n| AI-RMS-02 | starter/rms.c | rms_norm |\n| AI-RMS-03 | starter/rms.c | rms_finite |",
                   todo_sec("AI-RMS-01", "starter/rms.c", "rms_of",
                            "s=sum x*x; return sqrt(s/n);", "RMS", "sqrt(12.5)")
                   + todo_sec("AI-RMS-02", "starter/rms.c", "rms_norm",
                              "out[i]=x[i]/(rms+eps);", "escala", "3/rms")
                   + todo_sec("AI-RMS-03", "starter/rms.c", "rms_finite",
                              "isfinite em todos", "guard", "1")),
            cases="# Testes\n## Caso1 rms\n## Caso2 norm\n## Caso3 finite\n")

    # 10 node ring
    mod = DAY / "nodejs" / "shared_atomics_ring"
    st = r''''use strict';
const CAP = 4;
function createRing() {
  // TODO [NODE-RING-01]
  throw new Error('NODE-RING-01');
}
function push(ring, v) {
  // TODO [NODE-RING-02]
  throw new Error('NODE-RING-02');
}
function pop(ring) {
  // TODO [NODE-RING-03]
  throw new Error('NODE-RING-03');
}
module.exports = { CAP, createRing, push, pop };
'''
    sol = r''''use strict';
const CAP = 4;
function createRing() {
  // PEDAGOGY-SOLUTION: NODE-RING-01
  return { buf: new Int32Array(CAP), head: 0, tail: 0, count: 0 };
}
function push(ring, v) {
  // PEDAGOGY-SOLUTION: NODE-RING-02
  if (ring.count >= CAP) return false;
  ring.buf[ring.tail] = v;
  ring.tail = (ring.tail + 1) % CAP;
  ring.count++;
  return true;
}
function pop(ring) {
  // PEDAGOGY-SOLUTION: NODE-RING-03
  if (ring.count === 0) return null;
  const v = ring.buf[ring.head];
  ring.head = (ring.head + 1) % CAP;
  ring.count--;
  return v;
}
module.exports = { CAP, createRing, push, pop };
'''
    test = r''''use strict';
const assert = require('assert');
const { CAP, createRing, push, pop } = require('./shared_atomics_ring');
// PEDAGOGY-TEST: NODE-RING-01
const r = createRing();
assert.strictEqual(CAP, 4);
assert.strictEqual(r.count, 0);
// PEDAGOGY-TEST: NODE-RING-02
assert.strictEqual(push(r, 10), true);
assert.strictEqual(push(r, -3), true);
assert.strictEqual(r.count, 2);
assert.strictEqual(push(r, 1), true);
assert.strictEqual(push(r, 2), true);
assert.strictEqual(push(r, 3), false);
// PEDAGOGY-TEST: NODE-RING-03
assert.strictEqual(pop(r), 10);
assert.strictEqual(pop(r), -3);
console.log('ok');
'''
    for base, src in ((mod / "starter", st), (mod / "solutions", sol)):
        W(base / "shared_atomics_ring.js", src)
        W(base / "test.js", test)
        W(base / "package.json", '{\n  "name": "shared-atomics-ring",\n  "private": true\n}\n')
    ids = ["NODE-RING-01", "NODE-RING-02", "NODE-RING-03"]
    md_pack(mod, title="atomics ring", lang="JavaScript", ids=ids, why="Anel CAP4 (mesmo contrato do C dia 08).",
            theory=T("shared ring", "JavaScript", """
## 1. O quê
Ring buffer CAP=4, FIFO, push false se cheio, pop null se vazio.

## 2. Trace
push 10,-3,1,2; 5º false; pop→10 depois -3.

## 3. Por quê % CAP
Índices circulares.

## 4. Invariantes
count∈[0,4]; ordem FIFO.

## 5. Bugs
incrementar count sem checar; pop sem null.

## 6. Por quê "atomics" no nome
Prepara SharedArrayBuffer; neste lab a lógica é single-thread idêntica.
"""),
            reso=R("shared_atomics_ring",
                   "cd days/2026-09-11/nodejs/shared_atomics_ring/starter\nnode test.js",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| NODE-RING-01 | starter/shared_atomics_ring.js | createRing |\n| NODE-RING-02 | starter/shared_atomics_ring.js | push |\n| NODE-RING-03 | starter/shared_atomics_ring.js | pop |",
                   todo_sec("NODE-RING-01", "starter/shared_atomics_ring.js", "createRing",
                            "return { buf: new Int32Array(CAP), head:0, tail:0, count:0 };", "estado zero", "count0")
                   + todo_sec("NODE-RING-02", "starter/shared_atomics_ring.js", "push",
                              "if(count>=CAP)return false; buf[tail]=v; tail=(tail+1)%CAP; count++; return true;",
                              "cheio→false", "5º false")
                   + todo_sec("NODE-RING-03", "starter/shared_atomics_ring.js", "pop",
                              "if(count===0)return null; v=buf[head]; head=(head+1)%CAP; count--; return v;",
                              "FIFO", "10 then -3")),
            cases="# Testes\n## Caso1 create\n## Caso2 push full\n## Caso3 pop FIFO\n")

    # 11 ini lexer
    mod = DAY / "parsers" / "ini_rd_lexer"
    h = """#ifndef INI_H
#define INI_H
#include <stddef.h>
typedef enum { TOK_SECTION, TOK_KEY, TOK_VALUE, TOK_EOF, TOK_ERR } IniTok;
typedef struct { IniTok kind; char text[64]; } IniToken;
int ini_next(const char *s, size_t n, size_t *pos, IniToken *out);
int ini_lex_all(const char *s, size_t n, IniToken *out, int maxn);
#endif
"""
    st = r'''#include "ini.h"
#include <ctype.h>
#include <string.h>
int ini_next(const char *s, size_t n, size_t *pos, IniToken *out){
    /* TODO [PAR-INI-01] */ (void)s;(void)n;(void)pos;(void)out; return -1; }
int ini_lex_all(const char *s, size_t n, IniToken *out, int maxn){
    /* TODO [PAR-INI-02] */ (void)s;(void)n;(void)out;(void)maxn; return -1; }
/* PAR-INI-03: section must include brackets stripped — tested via lex_all count */
'''
    sol = r'''#include "ini.h"
#include <ctype.h>
#include <string.h>
static void skip_ws(const char *s, size_t n, size_t *pos){
    while(*pos<n && (s[*pos]==' '||s[*pos]=='\t'||s[*pos]=='\r'||s[*pos]=='\n')) (*pos)++;
}
int ini_next(const char *s, size_t n, size_t *pos, IniToken *out){
    /* PEDAGOGY-SOLUTION: PAR-INI-01 */
    size_t i; if(!s||!pos||!out) return -1;
    skip_ws(s,n,pos);
    if(*pos>=n){ out->kind=TOK_EOF; out->text[0]=0; return 0; }
    if(s[*pos]=='['){
        (*pos)++; i=0;
        while(*pos<n && s[*pos]!=']' && i+1<sizeof out->text) out->text[i++]=s[(*pos)++];
        out->text[i]=0;
        if(*pos>=n||s[*pos]!=']'){ out->kind=TOK_ERR; return -1; }
        (*pos)++; out->kind=TOK_SECTION; return 0;
    }
    i=0;
    while(*pos<n && s[*pos]!='=' && s[*pos]!='\n' && i+1<sizeof out->text) out->text[i++]=s[(*pos)++];
    out->text[i]=0;
    if(*pos<n && s[*pos]=='='){ (*pos)++; out->kind=TOK_KEY; return 0; }
    out->kind=TOK_VALUE; return 0;
}
int ini_lex_all(const char *s, size_t n, IniToken *out, int maxn){
    /* PEDAGOGY-SOLUTION: PAR-INI-02 */
    size_t pos=0; int c=0;
    if(!out||maxn<=0) return -1;
    while(c<maxn){
        if(ini_next(s,n,&pos,&out[c])!=0) return -1;
        if(out[c].kind==TOK_EOF) return c;
        if(out[c].kind==TOK_ERR) return -1;
        c++;
    }
    return -1;
}
'''
    test = r'''#include "ini.h"
#include <stdio.h>
#include <string.h>
static int fail(const char*m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    const char *s="[core]\nname=demo\n";
    IniToken t;
    size_t pos=0;
    /* PEDAGOGY-TEST: PAR-INI-01 */
    if(ini_next(s,strlen(s),&pos,&t)!=0||t.kind!=TOK_SECTION||strcmp(t.text,"core")) return fail("sec");
    /* PEDAGOGY-TEST: PAR-INI-02 */
    IniToken all[8];
    int n=ini_lex_all(s,strlen(s),all,8);
    /* section, key, value = 3 before EOF counted as return without EOF in array */
    if(n!=3) return fail("n");
    if(all[1].kind!=TOK_KEY||strcmp(all[1].text,"name")) return fail("k");
    if(all[2].kind!=TOK_VALUE||strcmp(all[2].text,"demo")) return fail("v");
    /* PEDAGOGY-TEST: PAR-INI-03 */
    if(strcmp(all[0].text,"core")) return fail("strip");
    puts("ok"); return 0;
}
'''
    pair_cmake(mod, CMAKE_C.format(n="ini", s="ini.c test_ini.c"),
               {"ini.c": (st, sol)}, {"ini.h": h, "test_ini.c": test})
    ids = ["PAR-INI-01", "PAR-INI-02", "PAR-INI-03"]
    md_pack(mod, title="ini lexer", lang="C", ids=ids, why="Lexer INI: section/key/value.",
            theory=T("INI rd lexer", "C", """
## 1. O quê
`[core]\\nname=demo\\n` → SECTION core, KEY name, VALUE demo.

## 2. Trace
pos0 '[' → text core (sem colchetes); name= → KEY; demo → VALUE; n=3.

## 3. Por quê strip brackets
Semântica da seção é o nome interno.

## 4. Invariantes
ERR se ] ausente; EOF termina lex_all.

## 5. Bugs
incluir [ no text; contar EOF como token.

## 6. Por quê vs JSON dia 08
INI é line-oriented; JSON é estrutural.
"""),
            reso=R("ini_rd_lexer",
                   "cd days/2026-09-11/parsers/ini_rd_lexer/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| PAR-INI-01 | starter/ini.c | ini_next |\n| PAR-INI-02 | starter/ini.c | ini_lex_all |\n| PAR-INI-03 | (strip em SECTION) | ini_next |",
                   todo_sec("PAR-INI-01", "starter/ini.c", "ini_next",
                            "skip ws; se '[' ler até ']' sem brackets; senão ler key até '=' ou value",
                            "máquina de tokens", "SECTION core")
                   + todo_sec("PAR-INI-02", "starter/ini.c", "ini_lex_all",
                              "loop ini_next até EOF; retorna contagem sem EOF", "3 tokens", "n==3")
                   + "\n## PAR-INI-03\nGaranta text da seção sem `[`/`]` — mesmo código de PAR-INI-01.\n"),
            cases="# Testes\n## Caso1 section\n## Caso2 lex_all 3\n## Caso3 strip\n")

    # 12 agent barrier
    mod = DAY / "agent" / "tool_barrier_join"
    st = r'''from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    WAITING = auto()
    DONE = auto()
    ERROR = auto()

class ToolBarrier:
    def __init__(self, need: int):
        self.need = need
        self.got = 0
        self.state = State.IDLE
        self.results = []

    def start(self):
        # TODO [AGENT-JOIN-01]
        raise NotImplementedError("AGENT-JOIN-01")

    def arrive(self, value):
        # TODO [AGENT-JOIN-02]
        raise NotImplementedError("AGENT-JOIN-02")

    def join(self):
        # TODO [AGENT-JOIN-03]
        raise NotImplementedError("AGENT-JOIN-03")
'''
    sol = r'''from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    WAITING = auto()
    DONE = auto()
    ERROR = auto()

class ToolBarrier:
    def __init__(self, need: int):
        self.need = need
        self.got = 0
        self.state = State.IDLE
        self.results = []

    def start(self):
        # PEDAGOGY-SOLUTION: AGENT-JOIN-01
        if self.need <= 0:
            self.state = State.ERROR
            return self.state
        self.got = 0
        self.results = []
        self.state = State.WAITING
        return self.state

    def arrive(self, value):
        # PEDAGOGY-SOLUTION: AGENT-JOIN-02
        if self.state != State.WAITING:
            return self.state
        self.results.append(value)
        self.got += 1
        if self.got >= self.need:
            self.state = State.DONE
        return self.state

    def join(self):
        # PEDAGOGY-SOLUTION: AGENT-JOIN-03
        if self.state != State.DONE:
            return None
        return list(self.results)
'''
    test = r'''from tool_barrier_join import ToolBarrier, State

def test_start():
    # PEDAGOGY-TEST: AGENT-JOIN-01
    b = ToolBarrier(2)
    assert b.start() == State.WAITING
    assert ToolBarrier(0).start() == State.ERROR

def test_arrive():
    # PEDAGOGY-TEST: AGENT-JOIN-02
    b = ToolBarrier(2)
    b.start()
    assert b.arrive("a") == State.WAITING
    assert b.arrive("b") == State.DONE

def test_join():
    # PEDAGOGY-TEST: AGENT-JOIN-03
    b = ToolBarrier(2)
    b.start(); b.arrive(1); b.arrive(2)
    assert b.join() == [1, 2]
    assert ToolBarrier(1).join() is None
'''
    for base, src in ((mod / "starter", st), (mod / "solutions", sol)):
        W(base / "tool_barrier_join.py", src)
        W(base / "test_tool_barrier_join.py", test)
    ids = ["AGENT-JOIN-01", "AGENT-JOIN-02", "AGENT-JOIN-03"]
    md_pack(mod, title="tool barrier", lang="Python", ids=ids, why="Join de N resultados de tools.",
            theory=T("tool barrier join", "Python", """
## 1. O quê
FSM: IDLE→WAITING(start)→DONE(após N arrive)→join devolve lista.

## 2. Trace
need=2; start WAITING; arrive a WAITING; arrive b DONE; join [a,b].

## 3. Por quê ERROR se need<=0
Barreira impossível.

## 4. Invariantes
arrive fora de WAITING não muda; join só em DONE.

## 5. Bugs
DONE no primeiro arrive; join em WAITING devolve [].

## 6. Por quê vs dia 08 tool FSM
Aqui é sincronização de N calls, não protocolo de uma call.
"""),
            reso=R("tool_barrier_join",
                   "cd days/2026-09-11/agent/tool_barrier_join/starter\npython -m pytest -q",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| AGENT-JOIN-01 | starter/tool_barrier_join.py | start |\n| AGENT-JOIN-02 | starter/tool_barrier_join.py | arrive |\n| AGENT-JOIN-03 | starter/tool_barrier_join.py | join |",
                   todo_sec("AGENT-JOIN-01", "starter/tool_barrier_join.py", "start",
                            "if need<=0: ERROR; else reset, WAITING", "valida need", "WAITING/ERROR")
                   + todo_sec("AGENT-JOIN-02", "starter/tool_barrier_join.py", "arrive",
                              "append; got++; if got>=need: DONE", "barreira", "2º → DONE")
                   + todo_sec("AGENT-JOIN-03", "starter/tool_barrier_join.py", "join",
                              "DONE → list(results) else None", "só completo", "[1,2]")),
            cases="# Testes\n## Caso1 start\n## Caso2 arrive\n## Caso3 join\n")

    # 13 coff asm
    mod = DAY / "tooling" / "coff_sym_name"
    api = """#ifndef API_H
#define API_H
#include <stdint.h>
#ifdef _WIN32
uint32_t coff_name_is_short(const char *eight);
#else
uint32_t coff_name_is_short(const char *eight);
#endif
#endif
"""
    asm = r'''; PUBLIC coff_name_is_short
_TEXT SEGMENT
coff_name_is_short PROC
    ; TODO [TOOL-COFF-01]: RCX = ptr to 8 bytes; return 1 if first byte != 0
    ; PEDAGOGY placeholder in starter returns 0 via xor
    xor eax, eax
    ret
coff_name_is_short ENDP
_TEXT ENDS
END
'''
    # For solutions, real asm
    asm_sol = r'''; PUBLIC coff_name_is_short
_TEXT SEGMENT
coff_name_is_short PROC
    ; PEDAGOGY-SOLUTION: TOOL-COFF-01
    ; RCX = pointer to 8-byte COFF name
    movzx eax, BYTE PTR [rcx]
    test eax, eax
    setne al
    movzx eax, al
    ret
coff_name_is_short ENDP
_TEXT ENDS
END
'''
    gas = r'''.global coff_name_is_short
coff_name_is_short:
    # TODO [TOOL-COFF-01] RDI ptr
    xor %eax, %eax
    ret
'''
    gas_sol = r'''.global coff_name_is_short
coff_name_is_short:
    # PEDAGOGY-SOLUTION: TOOL-COFF-01
    movzbl (%rdi), %eax
    test %eax, %eax
    setne %al
    movzbl %al, %eax
    ret
'''
    # Also need C helpers for 02/03
    main_st = r'''#include "api.h"
#include <stdio.h>
#include <string.h>
/* TODO [TOOL-COFF-02]: return 1 if 8 bytes equal to padded name */
int coff_name_eq(const char *eight, const char *want) {
    (void)eight; (void)want; return 0;
}
/* TODO [TOOL-COFF-03]: short name if first byte != 0 OR eq helper */
int coff_accept(const char *eight, const char *want) {
    (void)eight; (void)want; return 0;
}
int main(void) {
    char n[8] = {0};
    memcpy(n, "main", 4);
    /* PEDAGOGY-TEST: TOOL-COFF-01 */
    if (!coff_name_is_short(n)) { fprintf(stderr, "FAIL short\n"); return 1; }
    /* PEDAGOGY-TEST: TOOL-COFF-02 */
    if (!coff_name_eq(n, "main")) { fprintf(stderr, "FAIL eq\n"); return 1; }
    /* PEDAGOGY-TEST: TOOL-COFF-03 */
    if (!coff_accept(n, "main")) { fprintf(stderr, "FAIL accept\n"); return 1; }
    char z[8] = {0};
    if (coff_name_is_short(z)) { fprintf(stderr, "FAIL zero\n"); return 1; }
    puts("ok");
    return 0;
}
'''
    main_sol = r'''#include "api.h"
#include <stdio.h>
#include <string.h>
int coff_name_eq(const char *eight, const char *want) {
    /* PEDAGOGY-SOLUTION: TOOL-COFF-02 */
    char tmp[9];
    memcpy(tmp, eight, 8);
    tmp[8] = 0;
    return strncmp(tmp, want, 8) == 0;
}
int coff_accept(const char *eight, const char *want) {
    /* PEDAGOGY-SOLUTION: TOOL-COFF-03 */
    return coff_name_is_short(eight) && coff_name_eq(eight, want);
}
int main(void) {
    char n[8] = {0};
    memcpy(n, "main", 4);
    /* PEDAGOGY-TEST: TOOL-COFF-01 */
    if (!coff_name_is_short(n)) { fprintf(stderr, "FAIL short\n"); return 1; }
    /* PEDAGOGY-TEST: TOOL-COFF-02 */
    if (!coff_name_eq(n, "main")) { fprintf(stderr, "FAIL eq\n"); return 1; }
    /* PEDAGOGY-TEST: TOOL-COFF-03 */
    if (!coff_accept(n, "main")) { fprintf(stderr, "FAIL accept\n"); return 1; }
    char z[8] = {0};
    if (coff_name_is_short(z)) { fprintf(stderr, "FAIL zero\n"); return 1; }
    puts("ok");
    return 0;
}
'''
    for base, a, g, m in (
        (mod / "starter", asm, gas, main_st),
        (mod / "solutions", asm_sol, gas_sol, main_sol),
    ):
        W(base / "api.h", api)
        W(base / "coff_sym.asm", a)
        W(base / "coff_sym.S", g)
        W(base / "test_main.c", m)
        W(base / "CMakeLists.txt", CMAKE_ASM)
    ids = ["TOOL-COFF-01", "TOOL-COFF-02", "TOOL-COFF-03"]
    md_pack(mod, title="COFF sym", lang="Assembly + C", ids=ids, why="Nome curto COFF (8 bytes).",
            theory=T("COFF short name", "Assembly (MASM/GAS) + C", """
## 1. O quê
COFF short name: 8 bytes, se [0]!=0 é nome inline. Windows: ptr em RCX; SysV: RDI.

## 2. Trace
"main\\0\\0\\0\\0" → is_short=1; eq "main"; zeros → is_short=0.

## 3. Por quê 8 bytes
Campo Name da Symbol Table COFF.

## 4. Invariantes
is_short ⇔ first≠0 neste subset.

## 5. Bugs
ler RAX em vez de RCX no Win; strcmp sem pad.

## 6. Por quê asm
Mesmo ABI do lab wasm dia 08.
"""),
            reso=R("coff_sym_name",
                   "cd days/2026-09-11/tooling/coff_sym_name/starter\ncmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
                   "| TODO | Arquivo | Função |\n|------|---------|--------|\n| TOOL-COFF-01 | starter/coff_sym.asm (ou .S) | coff_name_is_short |\n| TOOL-COFF-02 | starter/test_main.c | coff_name_eq |\n| TOOL-COFF-03 | starter/test_main.c | coff_accept |",
                   todo_sec("TOOL-COFF-01", "starter/coff_sym.asm", "coff_name_is_short",
                            "movzx eax, BYTE PTR [rcx]\ntest eax, eax\nsetne al\nmovzx eax, al\nret",
                            "RCX=ptr Windows", "1 para main")
                   + todo_sec("TOOL-COFF-02", "starter/test_main.c", "coff_name_eq",
                              "memcpy tmp[9]; tmp[8]=0; return strncmp(tmp,want,8)==0;",
                              "compara até 8", "main")
                   + todo_sec("TOOL-COFF-03", "starter/test_main.c", "coff_accept",
                              "return coff_name_is_short(eight) && coff_name_eq(eight, want);",
                              "combina", "1")),
            cases="# Testes\n## Caso1 short\n## Caso2 eq\n## Caso3 accept\n")


def write_day_infra():
    modules = [
        ("systems/clvm_reloc_apply", "C", "reloc u16"),
        ("systems/bump_poison_arena", "C++", "poison/canary"),
        ("linux/uevent_kv_parse", "C", "uevent KV"),
        ("rust/clvm_reloc_verify", "Rust", "verify sites"),
        ("dotnet/pe_import_span", "C#", "import hint 0x2000"),
        ("graphics/alpha_blend_scanline", "C++", "blend 128"),
        ("redteam/import_name_triage", "Python", "suspicious imports"),
        ("quantum/phase_kickback", "C++", "CZ phase"),
        ("ai/rms_norm", "C", "RMS {3,4}"),
        ("nodejs/shared_atomics_ring", "JS", "ring CAP4"),
        ("parsers/ini_rd_lexer", "C", "INI lexer"),
        ("agent/tool_barrier_join", "Python", "barrier join"),
        ("tooling/coff_sym_name", "ASM", "COFF name"),
    ]
    rows = "\n".join(f"| {i} | `{p}` | **{l}** | {f} | 2–3 |" for i, (p, l, f) in enumerate(modules, 1))
    W(DAY / "README.md", f"""# Day 2026-09-11 — Relocação, ABI e verificação cruzada

13 módulos, linguagens misturadas. Continua o toolchain dos dias 08–10.

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
{rows}

**Total:** ~28–36 h.

C/C++/ASM: Visual Studio 18 2026 via Ninja no `run_day_tests.py`.
""")
    W(DAY / "START_HERE.md", """# START HERE — 2026-09-11

## Ordem cognitiva (não pule)

1. Reloc C + verify Rust (mesmo u16).
2. Arena C++ + uevent C.
3. PE import .NET + triage Python.
4. Blend + phase + RMS.
5. Ring JS + INI C + barrier Python + COFF ASM.

## Comandos

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-11
python scripts/run_day_tests.py --day 2026-09-11 --mode solutions
```

## Se travar

Use **Onde colocar** na RESOLUCAO (arquivo + função + substituir).
""")
    todo_ids = []
    for res in sorted(DAY.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md")):
        text = (res.parent / "starter").read_text(encoding="utf-8") if False else ""
        # collect from all starter files
        for f in (res.parent / "starter").rglob("*"):
            if f.is_file():
                try:
                    t = f.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                todo_ids += re.findall(r"TODO \[([A-Z0-9-]+)\]", t)
    # unique preserve order
    seen = set()
    ordered = []
    for i in todo_ids:
        if i not in seen:
            seen.add(i)
            ordered.append(i)
    W(DAY / "TODO_MAP.md", "# TODO_MAP — 2026-09-11\n\n" + "\n".join(f"- `{i}`" for i in ordered) + "\n")
    mods_list = "\n".join(f"- `{p}`" for p, _, _ in modules)
    W(DAY / "VALIDATION.md", f"""# VALIDATION — 2026-09-11

## Módulos

{mods_list}

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-11
python scripts/day_contract_check.py --day 2026-09-11
python scripts/run_day_tests.py --day 2026-09-11 --mode solutions
```
""")
    # ATIVIDADES deep
    W(DAY / "ATIVIDADES.md", """# ATIVIDADES — 2026-09-11

**Dia:** 13 módulos | **~28–36 h**
**Regra:** checkpoint no papel antes do código.

## Preparação (30 min)

- [ ] Ler START_HERE.md e README.md
- [ ] Baseline: `python scripts/pedagogy_check_unified.py --day 2026-09-11`

## Bloco 1 — Relocação cruzada C↔Rust (5–6 h)

| Módulo | Paper-trace |
|--------|-------------|
| systems/clvm_reloc_apply | 09 0A 00 08 +5 @1 → 0F; FFFF+1→0000 |
| rust/clvm_reloc_verify | read 0A 00 → 10; site at=3 len=4 inválido |

**Checkpoint conceitual:**

- [ ] Escrevi 10+5=15 em LE no papel
- [ ] Expliquei por que o site aponta ao imediato, não ao opcode
- [ ] Sei que Rust devolve Err no mesmo OOB que o C retorna -1

## Bloco 2 — Arena e uevent (4–5 h)

| Módulo | Paper-trace |
|--------|-------------|
| systems/bump_poison_arena | alloc(8)⇒used=9 canary@8=C3; 9+56+1>64 |
| linux/uevent_kv_parse | DEVNAME=sda; count=2 |

- [ ] Desenhei os 9 primeiros bytes pós-alloc
- [ ] Separei key/value de uma linha uevent

## Bloco 3 — PE import e triage (3–4 h)

| Módulo | Paper-trace |
|--------|-------------|
| dotnet/pe_import_span | MZ; e_lfanew 0x80; hint 0x2000 |
| redteam/import_name_triage | score VirtualAlloc+CreateRemoteThread = 2 |

- [ ] Diferenciei RVA export 0x1000 (dia 08) de import hint 0x2000
- [ ] Listei o set suspeito

## Bloco 4 — Blend, fase, RMS (5–6 h)

| Módulo | Paper-trace |
|--------|-------------|
| graphics/alpha_blend_scanline | (0,255,128)→128 |
| quantum/phase_kickback | X0: amp[1]=1; CZ: amp[3]=-1 |
| ai/rms_norm | rms([3,4])=sqrt(12.5) |

- [ ] Calculei o blend 128 na mão
- [ ] Calculei sqrt(12.5)

## Bloco 5 — Ring, INI, barrier, COFF (6–7 h)

| Módulo | Paper-trace |
|--------|-------------|
| nodejs/shared_atomics_ring | 4 pushes; 5º false; pop 10 |
| parsers/ini_rd_lexer | [core]/name=demo → 3 tokens |
| agent/tool_barrier_join | need2 → DONE no 2º arrive |
| tooling/coff_sym_name | main padded; RCX; first≠0 |

- [ ] Desenhei head/tail do anel
- [ ] Anotei ABI Windows RCX vs SysV RDI

## Relatório do dia

| Bloco | Papel | Testes |
|-------|-------|--------|
| 1 reloc | ☐ | ☐ |
| 2 arena/uevent | ☐ | ☐ |
| 3 PE | ☐ | ☐ |
| 4 math | ☐ | ☐ |
| 5 sync/asm | ☐ | ☐ |

**Síntese:** o mesmo u16 LE une C e Rust; o anel JS ecoa o anel C do dia 08; COFF asm ecoa o ABI do wasm header.
""")


def wire_repo():
    # tracks.yaml
    tracks = ROOT / "openspec" / "specs" / "day-contract" / "tracks.yaml"
    text = tracks.read_text(encoding="utf-8")
    if '"2026-09-11"' not in text:
        block = '''
      "2026-09-11":
        required_tracks:
          - systems
          - linux
          - rust
          - dotnet
          - graphics
          - redteam
          - quantum
          - ai
          - nodejs
          - parsers
          - agent
          - tooling
'''
        # insert after 2026-09-10 block or at end of tier_a days
        if '"2026-09-10"' in text:
            # find end of 2026-09-10 required_tracks — append after tooling of 10 if present
            text = text.replace(
                '      "2026-09-10":\n        required_tracks:\n          - systems\n          - linux\n          - rust\n          - dotnet\n          - graphics\n          - redteam\n          - quantum\n          - ai\n          - nodejs\n          - parsers\n          - agent\n          - tooling\n',
                '      "2026-09-10":\n        required_tracks:\n          - systems\n          - linux\n          - rust\n          - dotnet\n          - graphics\n          - redteam\n          - quantum\n          - ai\n          - nodejs\n          - parsers\n          - agent\n          - tooling\n'
                + block,
                1,
            )
        else:
            text = text.replace("  tier_b:", block + "\n  tier_b:", 1)
        tracks.write_text(text, encoding="utf-8", newline="\n")

    # GFX exempt
    ped = ROOT / "scripts" / "pedagogy_check_unified.py"
    pt = ped.read_text(encoding="utf-8")
    if '"alpha_blend_scanline"' not in pt:
        pt = pt.replace('"shader_stage_fsm",', '"shader_stage_fsm",\n    "alpha_blend_scanline",')
        ped.write_text(pt, encoding="utf-8", newline="\n")

    # LEARNING_PATHS
    lp = ROOT / "docs" / "LEARNING_PATHS.md"
    lt = lp.read_text(encoding="utf-8")
    if "2026-09-11" not in lt:
        lt = lt.rstrip() + """

## 15. Day 11 — Relocação, ABI e verificação cruzada (2026-09-11)

| # | Módulo | Capstone |
|---|--------|----------|
| 1 | `2026-09-11/systems/clvm_reloc_apply` | chris-vm |
| 2 | `2026-09-11/systems/bump_poison_arena` | chris-arena |
| 3 | `2026-09-11/linux/uevent_kv_parse` | chris-driver-lab |
| 4 | `2026-09-11/rust/clvm_reloc_verify` | chris-vm |
| 5 | `2026-09-11/dotnet/pe_import_span` | chris-dotnet-pe |
| 6 | `2026-09-11/graphics/alpha_blend_scanline` | chris-renderer |
| 7 | `2026-09-11/redteam/import_name_triage` | chris-binary-toolkit |
| 8 | `2026-09-11/quantum/phase_kickback` | chris-qsim |
| 9 | `2026-09-11/ai/rms_norm` | chris-tensor |
| 10 | `2026-09-11/nodejs/shared_atomics_ring` | chris-node-streaming |
| 11 | `2026-09-11/parsers/ini_rd_lexer` | chris-smart-grep |
| 12 | `2026-09-11/agent/tool_barrier_join` | chris-agent-harness |
| 13 | `2026-09-11/tooling/coff_sym_name` | chris-binary-toolkit |
"""
        lp.write_text(lt + "\n", encoding="utf-8", newline="\n")

    # module_project_map
    mp = ROOT / "scripts" / "module_project_map.py"
    mt = mp.read_text(encoding="utf-8")
    if "2026-09-11/systems/clvm_reloc_apply" not in mt:
        entries = '''
    "2026-09-11/systems/clvm_reloc_apply": {
        "project": "projects/chris-vm",
        "carry": "CLVM reloc apply",
        "tests": "reloc unit tests",
        "milestone": "MILESTONES.md — reloc",
        "commit": "feat(vm): port reloc apply from day11",
    },
    "2026-09-11/systems/bump_poison_arena": {
        "project": "projects/chris-arena",
        "carry": "bump poison canary",
        "tests": "arena tests",
        "milestone": "MILESTONES.md — bump",
        "commit": "feat(arena): port bump from day11",
    },
    "2026-09-11/linux/uevent_kv_parse": {
        "project": "projects/chris-driver-lab",
        "carry": "uevent kv parse",
        "tests": "uevent tests",
        "milestone": "MILESTONES.md — uevent",
        "commit": "feat(driver): port uevent parse from day11",
    },
    "2026-09-11/rust/clvm_reloc_verify": {
        "project": "projects/chris-vm",
        "carry": "reloc verify rust",
        "tests": "cargo tests",
        "milestone": "MILESTONES.md — reloc verify",
        "commit": "feat(vm): port reloc verify from day11",
    },
    "2026-09-11/dotnet/pe_import_span": {
        "project": "projects/chris-dotnet-pe",
        "carry": "PE import span",
        "tests": "dotnet test",
        "milestone": "MILESTONES.md — import",
        "commit": "feat(pe): port import span from day11",
    },
    "2026-09-11/graphics/alpha_blend_scanline": {
        "project": "projects/chris-renderer",
        "carry": "alpha blend scanline",
        "tests": "blend tests",
        "milestone": "MILESTONES.md — blend",
        "commit": "feat(renderer): port blend from day11",
    },
    "2026-09-11/redteam/import_name_triage": {
        "project": "projects/chris-binary-toolkit",
        "carry": "import triage",
        "tests": "pytest",
        "milestone": "MILESTONES.md — triage",
        "commit": "feat(toolkit): port import triage from day11",
    },
    "2026-09-11/quantum/phase_kickback": {
        "project": "projects/chris-qsim",
        "carry": "phase kickback",
        "tests": "phase tests",
        "milestone": "MILESTONES.md — phase",
        "commit": "feat(qsim): port phase from day11",
    },
    "2026-09-11/ai/rms_norm": {
        "project": "projects/chris-tensor",
        "carry": "RMSNorm",
        "tests": "rms tests",
        "milestone": "MILESTONES.md — rms",
        "commit": "feat(tensor): port rms from day11",
    },
    "2026-09-11/nodejs/shared_atomics_ring": {
        "project": "projects/chris-node-streaming",
        "carry": "atomics ring",
        "tests": "node test.js",
        "milestone": "MILESTONES.md — ring",
        "commit": "feat(node): port ring from day11",
    },
    "2026-09-11/parsers/ini_rd_lexer": {
        "project": "projects/chris-smart-grep",
        "carry": "INI lexer",
        "tests": "ini tests",
        "milestone": "MILESTONES.md — ini",
        "commit": "feat(parsers): port ini lexer from day11",
    },
    "2026-09-11/agent/tool_barrier_join": {
        "project": "projects/chris-agent-harness",
        "carry": "tool barrier",
        "tests": "pytest",
        "milestone": "MILESTONES.md — barrier",
        "commit": "feat(agent): port barrier from day11",
    },
    "2026-09-11/tooling/coff_sym_name": {
        "project": "projects/chris-binary-toolkit",
        "carry": "COFF sym name asm",
        "tests": "ctest",
        "milestone": "MILESTONES.md — coff",
        "commit": "feat(toolkit): port coff name from day11",
    },
'''
        mt = mt.rstrip()
        if mt.endswith("}"):
            # insert before final closing of dict — find last }
            idx = mt.rfind("}")
            mt = mt[:idx] + ",\n" + entries + mt[idx:]
        mp.write_text(mt, encoding="utf-8", newline="\n")

    # root README
    rr = ROOT / "README.md"
    rt = rr.read_text(encoding="utf-8")
    if "2026-09-11" not in rt:
        rt = rt.replace(
            "| 2026-09-10 | [`days/2026-09-10/`](days/2026-09-10/) | 13 (integração capstone) | — |",
            "| 2026-09-10 | [`days/2026-09-10/`](days/2026-09-10/) | 13 (integração capstone) | — |\n"
            "| 2026-09-11 | [`days/2026-09-11/`](days/2026-09-11/) | 13 (reloc/ABI) | — |",
        )
        rr.write_text(rt, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build_all()
