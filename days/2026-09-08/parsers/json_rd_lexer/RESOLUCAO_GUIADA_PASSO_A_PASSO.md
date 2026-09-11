# Resolução guiada — json_rd_lexer

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `PAR-JSON-LEX-01` | `starter/json_lex.c` | `skip_ws` | corpo sob `TODO [PAR-JSON-LEX-01]` | assinaturas e testes |
| `PAR-JSON-LEX-02` | `starter/json_lex.c` | `next_token` | corpo sob `TODO [PAR-JSON-LEX-02]` | assinaturas e testes |
| `PAR-JSON-LEX-03` | `starter/json_lex.c` | `lex_count` | corpo sob `TODO [PAR-JSON-LEX-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/parsers/json_rd_lexer/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## PAR-JSON-LEX-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/json_lex.c` |
| Função / âncora | `skip_ws` / comentário `TODO [PAR-JSON-LEX-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem skip_ws, espaços viram tokens.

### Algoritmo / trace

while ws: i++.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
int skip_ws(const char *s, int i) {
    /* PEDAGOGY-SOLUTION: PAR-JSON-LEX-01 */
    while (s[i] == ' ' || s[i] == '\n' || s[i] == '\t') i++;
    return i;
}
```

### Por que funciona?

A rotina `skip_ws` materializa o contrato de `PAR-JSON-LEX-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `PAR-JSON-LEX-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `PAR-JSON-LEX-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## PAR-JSON-LEX-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/json_lex.c` |
| Função / âncora | `next_token` / comentário `TODO [PAR-JSON-LEX-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem next_token, `{"a":1}` não tokeniza.

### Algoritmo / trace

skip_ws; classifique char; strings/números com cursor.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
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
```

### Por que funciona?

A rotina `next_token` materializa o contrato de `PAR-JSON-LEX-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `PAR-JSON-LEX-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `PAR-JSON-LEX-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## PAR-JSON-LEX-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/json_lex.c` |
| Função / âncora | `lex_count` / comentário `TODO [PAR-JSON-LEX-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem lex_count, o assert de 5 falha.

### Algoritmo / trace

loop next_token até END; conte.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```c
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
```

### Por que funciona?

A rotina `lex_count` materializa o contrato de `PAR-JSON-LEX-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `PAR-JSON-LEX-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `PAR-JSON-LEX-03` PASS no starter
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
| `PAR-JSON-LEX-01` |  |  |  |
| `PAR-JSON-LEX-02` |  |  |  |
| `PAR-JSON-LEX-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
