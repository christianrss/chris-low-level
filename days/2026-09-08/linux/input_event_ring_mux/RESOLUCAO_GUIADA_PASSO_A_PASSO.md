# Resolução guiada — input_event_ring_mux

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `LIN-MUX-01` | `starter/ring.c` | `ring_push` | corpo sob `TODO [LIN-MUX-01]` | assinaturas e testes |
| `LIN-MUX-02` | `starter/ring.c` | `ring_pop` | corpo sob `TODO [LIN-MUX-02]` | assinaturas e testes |
| `LIN-MUX-03` | `starter/ring.c` | `mux_push` | corpo sob `TODO [LIN-MUX-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/linux/input_event_ring_mux/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## LIN-MUX-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ring.c` |
| Função / âncora | `ring_push` / comentário `TODO [LIN-MUX-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem push, o anel não armazena o evento 10.

### Algoritmo / trace

Se count>=CAP return -1; slots[tail]=ev; tail=(tail+1)%CAP; count++.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
int ring_push(EventRing *r, InputEvent ev) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-01 */
    if (!r || r->count >= RING_CAP) return -1;
    r->slots[r->tail] = ev;
    r->tail = (r->tail + 1) % RING_CAP;
    r->count++;
    return 0;
}
```

### Por que funciona?

A rotina `ring_push` materializa o contrato de `LIN-MUX-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `LIN-MUX-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `LIN-MUX-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## LIN-MUX-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ring.c` |
| Função / âncora | `ring_pop` / comentário `TODO [LIN-MUX-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem pop FIFO, a ordem 10 depois -3 quebra.

### Algoritmo / trace

Se count==0 return -1; *out=slots[head]; head=(head+1)%CAP; count--.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
int ring_pop(EventRing *r, InputEvent *out) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-02 */
    if (!r || !out || r->count == 0) return -1;
    *out = r->slots[r->head];
    r->head = (r->head + 1) % RING_CAP;
    r->count--;
    return 0;
}
```

### Por que funciona?

A rotina `ring_pop` materializa o contrato de `LIN-MUX-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `LIN-MUX-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `LIN-MUX-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## LIN-MUX-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ring.c` |
| Função / âncora | `mux_push` / comentário `TODO [LIN-MUX-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem mux, source/type/value não entram no anel.

### Algoritmo / trace

Preencha InputEvent e chame ring_push.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
int mux_push(EventRing *r, uint8_t source, uint16_t type, int32_t value) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-03 */
    InputEvent ev;
    ev.type = type; ev.value = value; ev.source = source;
    return ring_push(r, ev);
}
```

### Por que funciona?

A rotina `mux_push` materializa o contrato de `LIN-MUX-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `LIN-MUX-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `LIN-MUX-03` PASS no starter
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
| `LIN-MUX-01` |  |  |  |
| `LIN-MUX-02` |  |  |  |
| `LIN-MUX-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
