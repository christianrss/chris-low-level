# Resolução guiada — Profiler de opcodes CLVM (C)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CLVM-TRACE-01` | `starter/trace.c` | `note_op` |
| `CLVM-TRACE-02` | `starter/trace.c` | `hottest` |
| `CLVM-TRACE-03` | `starter/trace.c` | `profile_code` |

> Raiz: `days/2026-09-09/systems/clvm_trace_profiler/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cmake -S days/2026-09-09/systems/clvm_trace_profiler/starter -B days/2026-09-09/systems/clvm_trace_profiler/starter/build_ci -G "Visual Studio 17 2022" -A x64
cmake --build days/2026-09-09/systems/clvm_trace_profiler/starter/build_ci --config Release
ctest --test-dir days/2026-09-09/systems/clvm_trace_profiler/starter/build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CLVM-TRACE-01

### Onde colocar (CLVM-TRACE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/trace.c` |
| Função / âncora | `note_op` — comentário `TODO [CLVM-TRACE-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CLVM-TRACE-01`, o Caso correspondente falha: Após três note_op, `c[0x02]==2` e `c[0x08]==1`.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CLVM-TRACE-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```c
void note_op(uint32_t *counts, uint8_t op) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-01 */
    if (counts && op < 16) counts[op]++;
}
```

### Por que funciona?

Por quê este corpo satisfaz `CLVM-TRACE-01`: ele implementa exatamente o contrato do
teste (Após três note_op, `c[0x02]==2` e `c[0x08]==1`.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CLVM-TRACE-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CLVM-TRACE-02

### Onde colocar (CLVM-TRACE-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/trace.c` |
| Função / âncora | `hottest` — comentário `TODO [CLVM-TRACE-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CLVM-TRACE-02`, o Caso correspondente falha: `hottest(c)==0x02`.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CLVM-TRACE-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```c
int hottest(const uint32_t *counts) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-02 */
    int best = 0, i;
    if (!counts) return -1;
    for (i = 1; i < 16; i++) if (counts[i] > counts[best]) best = i;
    return best;
}
```

### Por que funciona?

Por quê este corpo satisfaz `CLVM-TRACE-02`: ele implementa exatamente o contrato do
teste (`hottest(c)==0x02`.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CLVM-TRACE-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CLVM-TRACE-03

### Onde colocar (CLVM-TRACE-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/trace.c` |
| Função / âncora | `profile_code` — comentário `TODO [CLVM-TRACE-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CLVM-TRACE-03`, o Caso correspondente falha: `profile_code` retorna 3 e hottest continua 2.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CLVM-TRACE-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```c
int profile_code(const uint8_t *code, size_t n, uint32_t *counts) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-03 */
    size_t i;
    if (!code || !counts) return -1;
    for (i = 0; i < n; i++) note_op(counts, code[i]);
    return (int)n;
}
```

### Por que funciona?

Por quê este corpo satisfaz `CLVM-TRACE-03`: ele implementa exatamente o contrato do
teste (`profile_code` retorna 3 e hottest continua 2.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CLVM-TRACE-03`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.


## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| NotImplemented / stub | corpo não substituído | cole o bloco do TODO |
| número/string diferente | trace errado no papel | refaça a seção 4 da TEORIA |
| caso seguinte quebra | mudou assinatura ou estado global | restaure o que “Não mexer” pede |
| listener/null (.NET) | sem ActivityListener | veja TESTES_GUIADOS |

## Checkpoint intermediário de integração

Depois do primeiro TODO que compila:

1. Rode o teste do módulo a partir de `starter/` (ou o comando do Baseline).
2. Confirme que o Caso 1 ainda falha **só** nos TODOs restantes (não por link quebrado).
3. Anote a mensagem de assert: ela aponta o próximo ID.

## Passo a passo de edição (operacional)

Para cada TODO restante, repita:

1. Abra o arquivo da tabela **Onde colocar**.
2. Localize o comentário `TODO [ID]` — não busque pelo nome do módulo na pasta pai.
3. Substitua **apenas** o corpo indicado; preserve assinatura e includes.
4. Compile; se o erro for de tipo/assinatura, você editou demais.
5. Só então avance ao próximo ID.

## Tabela de regressão rápida

| Depois de | Deve passar | Ainda pode falhar |
|-----------|-------------|-------------------|
| 1º TODO | asserts só desse ID | IDs seguintes |
| 2º TODO | IDs 1–2 | IDs seguintes |
| último TODO | suite inteira | — |

## Armadilhas específicas deste starter

- Mudar o teste para “passar” invalida o lab.
- Criar um segundo `.c`/`.py` com o mesmo símbolo gera link duplicado ou import errado.
- Reset ausente entre casos deixa estado (anel, FSM, arena) contaminado.

## Relatório — campos extras

Além do template padrão, anote:

- Tempo até o primeiro Caso 1 verde:
- Quantas vezes o endianness/size foi a causa:
- Um invariante que você quase violou:

## Relatório de resolução

- TODOs concluídos:
- Comando de teste:
- Saída observada:
- Invariantes checadas:
- Edge cases:
- Benchmark (`profile_code em 1e6 bytes sintéticos (ms)`):
