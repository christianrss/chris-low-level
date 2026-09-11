# Resolução guiada — bell_state_prep

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `Q-BELL-01` | `starter/bell.cpp` | `q_reset` | corpo sob `TODO [Q-BELL-01]` | assinaturas e testes |
| `Q-BELL-02` | `starter/bell.cpp` | `q_h0` | corpo sob `TODO [Q-BELL-02]` | assinaturas e testes |
| `Q-BELL-03` | `starter/bell.cpp` | `q_cnot` | corpo sob `TODO [Q-BELL-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/quantum/bell_state_prep/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## Q-BELL-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bell.cpp` |
| Função / âncora | `q_reset` / comentário `TODO [Q-BELL-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem reset, o vetor não começa em |00⟩.

### Algoritmo / trace

amp = [1,0,0,0].

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
void q_reset(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-01
    amp[0] = 1.0; amp[1] = 0.0; amp[2] = 0.0; amp[3] = 0.0;
}
```

### Por que funciona?

A rotina `q_reset` materializa o contrato de `Q-BELL-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `Q-BELL-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `Q-BELL-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## Q-BELL-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bell.cpp` |
| Função / âncora | `q_h0` / comentário `TODO [Q-BELL-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem H0, não há superposição.

### Algoritmo / trace

H0 com s=1/√2 nas combinações (0,2) e (1,3).

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
void q_h0(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-02
    const double s = 1.0 / sqrt(2.0);
    double a0 = amp[0], a1 = amp[1], a2 = amp[2], a3 = amp[3];
    amp[0] = s * (a0 + a2);
    amp[1] = s * (a1 + a3);
    amp[2] = s * (a0 - a2);
    amp[3] = s * (a1 - a3);
}
```

### Por que funciona?

A rotina `q_h0` materializa o contrato de `Q-BELL-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `Q-BELL-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `Q-BELL-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## Q-BELL-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bell.cpp` |
| Função / âncora | `q_cnot` / comentário `TODO [Q-BELL-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem CNOT, não há Bell (P11≠0.5).

### Algoritmo / trace

swap amp[2]↔amp[3].

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```cpp
void q_cnot(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-03
    double a2 = amp[2], a3 = amp[3];
    amp[2] = a3;
    amp[3] = a2;
}
```

### Por que funciona?

A rotina `q_cnot` materializa o contrato de `Q-BELL-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `Q-BELL-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `Q-BELL-03` PASS no starter
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
| `Q-BELL-01` |  |  |  |
| `Q-BELL-02` |  |  |  |
| `Q-BELL-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
