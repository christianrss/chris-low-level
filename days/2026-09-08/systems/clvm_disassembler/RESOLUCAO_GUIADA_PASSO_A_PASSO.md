# Resolução guiada — clvm_disassembler

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `CLVM-DIS-01` | `starter/clvm_disasm.c` | `decode_push` | corpo sob `TODO [CLVM-DIS-01]` | assinaturas e testes |
| `CLVM-DIS-02` | `starter/clvm_disasm.c` | `decode_branch` | corpo sob `TODO [CLVM-DIS-02]` | assinaturas e testes |
| `CLVM-DIS-03` | `starter/clvm_disasm.c` | `disassemble_all` | corpo sob `TODO [CLVM-DIS-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/systems/clvm_disassembler/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## CLVM-DIS-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_disasm.c` |
| Função / âncora | `decode_push` / comentário `TODO [CLVM-DIS-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem decode_push, `01 2A 00 00 00` não vira `PUSH 42` size 5 — o assert do Caso 1 falha.

### Algoritmo / trace

Leia opcode 0x01; monte imm LE dos 4 bytes; snprintf PUSH; size=5; senão -1.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
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
```

### Por que funciona?

A rotina `decode_push` materializa o contrato de `CLVM-DIS-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-DIS-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-DIS-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## CLVM-DIS-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_disasm.c` |
| Função / âncora | `decode_branch` / comentário `TODO [CLVM-DIS-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem decode_branch, `09 0A 00` não vira `JMP 10` size 3.

### Algoritmo / trace

Confirme branch; rel = b1|(b2<<8); nome via op_name; size=3.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
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
```

### Por que funciona?

A rotina `decode_branch` materializa o contrato de `CLVM-DIS-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-DIS-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-DIS-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## CLVM-DIS-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_disasm.c` |
| Função / âncora | `disassemble_all` / comentário `TODO [CLVM-DIS-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem walk, o programa de 7 bytes não produz as 3 linhas esperadas.

### Algoritmo / trace

pc=0; escolha decoder; copie line; pc+=size; opcode desconhecido → -1.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
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
```

### Por que funciona?

A rotina `disassemble_all` materializa o contrato de `CLVM-DIS-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-DIS-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-DIS-03` PASS no starter
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
| `CLVM-DIS-01` |  |  |  |
| `CLVM-DIS-02` |  |  |  |
| `CLVM-DIS-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
