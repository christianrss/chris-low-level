# Resolução guiada — softmax_stable

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `AI-SOFTMAX-01` | `starter/softmax.c` | `softmax_stable` | corpo sob `TODO [AI-SOFTMAX-01]` | assinaturas e testes |
| `AI-SOFTMAX-02` | `starter/softmax.c` | `log_softmax_stable` | corpo sob `TODO [AI-SOFTMAX-02]` | assinaturas e testes |
| `AI-SOFTMAX-03` | `starter/softmax.c` | `cross_entropy_loss` | corpo sob `TODO [AI-SOFTMAX-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/ai/softmax_stable/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## AI-SOFTMAX-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/softmax.c` |
| Função / âncora | `softmax_stable` / comentário `TODO [AI-SOFTMAX-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem softmax estável, Σp≠1 ou overflow.

### Algoritmo / trace

m=max; exp(x-m); normalize.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
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
```

### Por que funciona?

A rotina `softmax_stable` materializa o contrato de `AI-SOFTMAX-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `AI-SOFTMAX-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `AI-SOFTMAX-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## AI-SOFTMAX-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/softmax.c` |
| Função / âncora | `log_softmax_stable` / comentário `TODO [AI-SOFTMAX-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem log_softmax, CE não fecha.

### Algoritmo / trace

m=max; logsum; (x-m)-logsum.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
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
```

### Por que funciona?

A rotina `log_softmax_stable` materializa o contrato de `AI-SOFTMAX-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `AI-SOFTMAX-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `AI-SOFTMAX-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## AI-SOFTMAX-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/softmax.c` |
| Função / âncora | `cross_entropy_loss` / comentário `TODO [AI-SOFTMAX-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem CE, o target 2 não bate com -log_p.

### Algoritmo / trace

log_softmax; return -logs[target].

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
float cross_entropy_loss(const float *logits, int n, int target) {
    /* PEDAGOGY-SOLUTION: AI-SOFTMAX-03 */
    float logs[8];
    if (!logits || target < 0 || target >= n || n > 8) return -1.f;
    if (log_softmax_stable(logits, n, logs) != 0) return -1.f;
    return -logs[target];
}
```

### Por que funciona?

A rotina `cross_entropy_loss` materializa o contrato de `AI-SOFTMAX-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `AI-SOFTMAX-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `AI-SOFTMAX-03` PASS no starter
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
| `AI-SOFTMAX-01` |  |  |  |
| `AI-SOFTMAX-02` |  |  |  |
| `AI-SOFTMAX-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
