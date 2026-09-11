# Resolução guiada — Máscara causal de atenção (C)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `AI-ATTN-01` | `starter/attn.c` | `causal_mask` |
| `AI-ATTN-02` | `starter/attn.c` | `apply_mask` |
| `AI-ATTN-03` | `starter/attn.c` | `visible_count` |

> Raiz: `days/2026-09-09/ai/attention_mask/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cmake -S days/2026-09-09/ai/attention_mask/starter -B days/2026-09-09/ai/attention_mask/starter/build_ci -G "Visual Studio 17 2022" -A x64
cmake --build days/2026-09-09/ai/attention_mask/starter/build_ci --config Release
ctest --test-dir days/2026-09-09/ai/attention_mask/starter/build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## AI-ATTN-01

### Onde colocar (AI-ATTN-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/attn.c` |
| Função / âncora | `causal_mask` — comentário `TODO [AI-ATTN-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `AI-ATTN-01`, o Caso correspondente falha: causal_mask(2,2)==1 e (2,3)==0.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `AI-ATTN-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```c
int causal_mask(int q, int k) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-01 */
    if (q < 0 || k < 0) return 0;
    return k <= q ? 1 : 0;
}
```

### Por que funciona?

Por quê este corpo satisfaz `AI-ATTN-01`: ele implementa exatamente o contrato do
teste (causal_mask(2,2)==1 e (2,3)==0.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `AI-ATTN-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## AI-ATTN-02

### Onde colocar (AI-ATTN-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/attn.c` |
| Função / âncora | `apply_mask` — comentário `TODO [AI-ATTN-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `AI-ATTN-02`, o Caso correspondente falha: apply_mask escreve −1e9 e retorna 0.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `AI-ATTN-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```c
int apply_mask(float *score, int q, int k) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-02 */
    if (!score) return 0;
    if (!causal_mask(q, k)) { *score = -1.0e9f; return 0; }
    return 1;
}
```

### Por que funciona?

Por quê este corpo satisfaz `AI-ATTN-02`: ele implementa exatamente o contrato do
teste (apply_mask escreve −1e9 e retorna 0.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `AI-ATTN-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## AI-ATTN-03

### Onde colocar (AI-ATTN-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/attn.c` |
| Função / âncora | `visible_count` — comentário `TODO [AI-ATTN-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `AI-ATTN-03`, o Caso correspondente falha: visible_count(2)==3.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `AI-ATTN-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```c
int visible_count(int q) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-03 */
    if (q < 0) return 0;
    return q + 1;
}
```

### Por que funciona?

Por quê este corpo satisfaz `AI-ATTN-03`: ele implementa exatamente o contrato do
teste (visible_count(2)==3.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `AI-ATTN-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e7 chamadas causal_mask`):
