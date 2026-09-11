# Resolução guiada — clvm_peephole_opt

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `CLVM-PEEP-01` | `starter/peephole.cpp` | `match_push0_add` | corpo sob `TODO [CLVM-PEEP-01]` | assinaturas e testes |
| `CLVM-PEEP-02` | `starter/peephole.cpp` | `fold_const_add` | corpo sob `TODO [CLVM-PEEP-02]` | assinaturas e testes |
| `CLVM-PEEP-03` | `starter/peephole.cpp` | `saved_bytes` | corpo sob `TODO [CLVM-PEEP-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/systems/clvm_peephole_opt/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## CLVM-PEEP-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/peephole.cpp` |
| Função / âncora | `match_push0_add` / comentário `TODO [CLVM-PEEP-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem match, PUSH0+ADD não é reconhecido e saved_bytes fica 0.

### Algoritmo / trace

Janela 6 bytes: PUSH com imm0 e ADD → return 1.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
int match_push0_add(const uint8_t *code, size_t len, size_t pc) {
    // PEDAGOGY-SOLUTION: CLVM-PEEP-01
    if (!code || pc + 6 > len) return 0;
    if (code[pc] != 0x01 || code[pc + 5] != 0x02) return 0;
    return rd_u32(code + pc + 1) == 0 ? 1 : 0;
}
```

### Por que funciona?

A rotina `match_push0_add` materializa o contrato de `CLVM-PEEP-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-PEEP-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-PEEP-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## CLVM-PEEP-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/peephole.cpp` |
| Função / âncora | `fold_const_add` / comentário `TODO [CLVM-PEEP-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem fold, 2+3+ADD não vira PUSH 5 (5 bytes).

### Algoritmo / trace

Janela 11: dois PUSH + ADD; some imms; emita PUSH s (5 bytes).

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
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
```

### Por que funciona?

A rotina `fold_const_add` materializa o contrato de `CLVM-PEEP-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-PEEP-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-PEEP-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## CLVM-PEEP-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/peephole.cpp` |
| Função / âncora | `saved_bytes` / comentário `TODO [CLVM-PEEP-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem varredura, o teste de bytes economizados falha.

### Algoritmo / trace

Varra i; some 6 por padrão matched; avance i pelo tamanho do padrão.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
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
```

### Por que funciona?

A rotina `saved_bytes` materializa o contrato de `CLVM-PEEP-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-PEEP-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-PEEP-03` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| FAIL no Caso 1 | stub intacto / endian errado | releia o trace da TEORIA e o bloco do primeiro TODO |
| PASS parcial | size/estado desalinhado no TODO do meio | imprima pc/head/estado antes do assert |
| Crash / panic | bounds | valide Length/len antes de indexar |
| Diff de string | snprintf/format | compare caractere a caractere com o esperado |

## Relatório de resolução

| TODO | Horas | Maior bug | O que aprendia de novo |
|------|-------|-----------|------------------------|
| `CLVM-PEEP-01` |  |  |  |
| `CLVM-PEEP-02` |  |  |  |
| `CLVM-PEEP-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
