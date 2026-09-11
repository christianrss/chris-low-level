# Resolução guiada — clvm_reloc_apply (C)

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

## CLVM-RELOC-01

### Onde colocar (CLVM-RELOC-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_reloc.c` |
| Função | `reloc_read_u16` |
| Substituir | o corpo sob o comentário `TODO [CLVM-RELOC-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Sem leitura LE, `apply_one` não tem valor base.

### Algoritmo / trace

`at=0`, bytes `0A 00` → 10. Se `at+2>len`, retorne -1.

### Escreva o código

```c
    if (!code || !out || at + 2 > len) return -1;
    *out = (uint16_t)code[at] | ((uint16_t)code[at + 1] << 8);
    return 0;
```

### Por que funciona?

O shift 8 coloca o segundo byte na metade alta do u16.

### Verifique

Caso 1: `v == 10`; leitura em `at=2` com `len=3` falha.

### Código completo alinhado ao solutions/ (CLVM-RELOC-01)

```c
PEDAGOGY-SOLUTION: CLVM-RELOC-01 */
    if (!code || !out || at + 2 > len) return -1;
    *out = (uint16_t)code[at] | ((uint16_t)code[at + 1] << 8);
    return 0;
}

int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta) {
    /* 
```

## CLVM-RELOC-02

### Onde colocar (CLVM-RELOC-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_reloc.c` |
| Função | `reloc_apply_one` |
| Substituir | o corpo sob o comentário `TODO [CLVM-RELOC-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

O teste espera `09 0A 00 08` + delta 5 no site 1 → `09 0F 00 08`.

### Algoritmo / trace

Leia 10; some 5; grave `0x0F, 0x00`.

### Escreva o código

```c
    uint16_t cur;
    uint16_t next;
    if (reloc_read_u16(code, len, at, &cur) != 0) return -1;
    next = (uint16_t)(cur + (uint16_t)delta);
    code[at] = (uint8_t)(next & 0xFF);
    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);
    return 0;
```

### Por que funciona?

Cast para uint16_t na soma dá o wrap do Caso 4 de graça.

### Verifique

`buf[1]==0x0F`, `buf[2]==0x00`, opcode permanece `0x09`.

### Código completo alinhado ao solutions/ (CLVM-RELOC-02)

```c
PEDAGOGY-SOLUTION: CLVM-RELOC-02 */
    /* 
```

## CLVM-RELOC-03

### Onde colocar (CLVM-RELOC-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_reloc.c` |
| Função | `reloc_apply_all` |
| Substituir | o corpo sob o comentário `TODO [CLVM-RELOC-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Dois JMP no mesmo buffer precisam do mesmo delta.

### Algoritmo / trace

Para cada sites[i], chame reloc_apply_one. Qualquer -1 aborta.

### Escreva o código

```c
    size_t i;
    if (!code || (!sites && n > 0)) return -1;
    for (i = 0; i < n; ++i) {
        if (reloc_apply_one(code, len, sites[i], delta) != 0) return -1;
    }
    return 0;
```

### Por que funciona?

Reusa a aritmética já testada; o lote só itera sites.

### Verifique

`buf[1]==5`, `buf[4]==7`.

### Código completo alinhado ao solutions/ (CLVM-RELOC-03)

```c
PEDAGOGY-SOLUTION: CLVM-RELOC-03 */
    size_t i;
    if (!code || (!sites && n > 0)) return -1;
    for (i = 0; i < n; ++i) {
        if (reloc_apply_one(code, len, sites[i], delta) != 0) return -1;
    }
    return 0;
}
```

## CLVM-RELOC-04

### Onde colocar (CLVM-RELOC-04)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_reloc.c` |
| Função | `reloc_apply_one` |
| Substituir | o corpo sob o comentário `TODO [CLVM-RELOC-04]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

0xFFFF+1 deve virar 0, não 65536 nem saturar.

### Algoritmo / trace

Use `(uint16_t)(cur + (uint16_t)delta)` — o mesmo corpo do 02.

### Escreva o código

```c
    next = (uint16_t)(cur + (uint16_t)delta);
    code[at] = (uint8_t)(next & 0xFF);
    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);
    return 0;
```

### Por que funciona?

Aritmética modular de 16 bits é o contrato do campo no bytecode.

### Verifique

`FF FF` +1 → `00 00`.

### Código completo alinhado ao solutions/ (CLVM-RELOC-04)

```c
PEDAGOGY-SOLUTION: CLVM-RELOC-04 */
    uint16_t cur;
    uint16_t next;
    if (reloc_read_u16(code, len, at, &cur) != 0) return -1;
    next = (uint16_t)(cur + (uint16_t)delta);
    code[at] = (uint8_t)(next & 0xFF);
    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);
    return 0;
}

int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta) {
    /* 
```

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
