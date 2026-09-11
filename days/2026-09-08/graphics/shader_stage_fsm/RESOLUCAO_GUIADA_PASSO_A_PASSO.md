# Resolução guiada — shader_stage_fsm

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `GFX-SHADER-FSM-01` | `starter/shader_fsm.cpp` | `shader_can` | corpo sob `TODO [GFX-SHADER-FSM-01]` | assinaturas e testes |
| `GFX-SHADER-FSM-02` | `starter/shader_fsm.cpp` | `shader_apply` | corpo sob `TODO [GFX-SHADER-FSM-02]` | assinaturas e testes |
| `GFX-SHADER-FSM-03` | `starter/shader_fsm.cpp` | `shader_illegal` | corpo sob `TODO [GFX-SHADER-FSM-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/graphics/shader_stage_fsm/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## GFX-SHADER-FSM-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/shader_fsm.cpp` |
| Função / âncora | `shader_can` / comentário `TODO [GFX-SHADER-FSM-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem can, EDIT→COMPILE não é permitido.

### Algoritmo / trace

Tabela de arestas permitidas; default 0.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
int shader_can(int from, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-01
    if (from == ST_EDIT && to == ST_COMPILE) return 1;
    if (from == ST_COMPILE && (to == ST_LINK || to == ST_EDIT)) return 1;
    if (from == ST_LINK && to == ST_READY) return 1;
    if (from == ST_READY && to == ST_EDIT) return 1;
    return 0;
}
```

### Por que funciona?

A rotina `shader_can` materializa o contrato de `GFX-SHADER-FSM-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `GFX-SHADER-FSM-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `GFX-SHADER-FSM-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## GFX-SHADER-FSM-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/shader_fsm.cpp` |
| Função / âncora | `shader_apply` / comentário `TODO [GFX-SHADER-FSM-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem apply, o estado não avança com segurança.

### Algoritmo / trace

Se !can return -1; senão *stage=to.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
int shader_apply(int *stage, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-02
    if (!stage || !shader_can(*stage, to)) return -1;
    *stage = to;
    return 0;
}
```

### Por que funciona?

A rotina `shader_apply` materializa o contrato de `GFX-SHADER-FSM-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `GFX-SHADER-FSM-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `GFX-SHADER-FSM-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## GFX-SHADER-FSM-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/shader_fsm.cpp` |
| Função / âncora | `shader_illegal` / comentário `TODO [GFX-SHADER-FSM-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem illegal, o teste de aresta proibida falha.

### Algoritmo / trace

return can?0:1.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
int shader_illegal(int from, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-03
    return shader_can(from, to) ? 0 : 1;
}
```

### Por que funciona?

A rotina `shader_illegal` materializa o contrato de `GFX-SHADER-FSM-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `GFX-SHADER-FSM-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `GFX-SHADER-FSM-03` PASS no starter
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
| `GFX-SHADER-FSM-01` |  |  |  |
| `GFX-SHADER-FSM-02` |  |  |  |
| `GFX-SHADER-FSM-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
