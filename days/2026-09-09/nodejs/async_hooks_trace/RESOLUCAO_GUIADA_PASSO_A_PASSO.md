# Resolução guiada — async_hooks: fases e métricas (JavaScript)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `ND-ASYNC-HOOK-01` | `starter/async_trace.js` | `installHooks` |
| `ND-ASYNC-TIMELINE-02` | `starter/async_trace.js` | `formatTimeline` |
| `ND-ASYNC-METRICS-03` | `starter/async_trace.js` | `countPhases` |

> Raiz: `days/2026-09-09/nodejs/async_hooks_trace/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/nodejs/async_hooks_trace/starter
node --test test.js 2>$null; if (-not $?) { node test.js }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## ND-ASYNC-HOOK-01

### Onde colocar (ND-ASYNC-HOOK-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/async_trace.js` |
| Função / âncora | `installHooks` — comentário `TODO [ND-ASYNC-HOOK-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `ND-ASYNC-HOOK-01`, o Caso correspondente falha: existe evento init.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `ND-ASYNC-HOOK-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```javascript
export function installHooks(store) {
    // PEDAGOGY-SOLUTION: ND-ASYNC-HOOK-01
    asyncHooks.createHook({
        init(asyncId, type, triggerAsyncId) {
            store.events.push({ phase: 'init', asyncId, type, triggerAsyncId });
        },
        before(asyncId) { store.events.push({ phase: 'before', asyncId }); },
        after(asyncId) { store.events.push({ phase: 'after', asyncId }); },
    }).enable();
}
```

### Por que funciona?

Por quê este corpo satisfaz `ND-ASYNC-HOOK-01`: ele implementa exatamente o contrato do
teste (existe evento init.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `ND-ASYNC-HOOK-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## ND-ASYNC-TIMELINE-02

### Onde colocar (ND-ASYNC-TIMELINE-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/async_trace.js` |
| Função / âncora | `formatTimeline` — comentário `TODO [ND-ASYNC-TIMELINE-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `ND-ASYNC-TIMELINE-02`, o Caso correspondente falha: timeline contém init.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `ND-ASYNC-TIMELINE-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```javascript
export function formatTimeline(events) {
    // PEDAGOGY-SOLUTION: ND-ASYNC-TIMELINE-02
    return events.map(e => `${e.phase}:${e.asyncId}`).join('|');
}
```

### Por que funciona?

Por quê este corpo satisfaz `ND-ASYNC-TIMELINE-02`: ele implementa exatamente o contrato do
teste (timeline contém init.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `ND-ASYNC-TIMELINE-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## ND-ASYNC-METRICS-03

### Onde colocar (ND-ASYNC-METRICS-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/async_trace.js` |
| Função / âncora | `countPhases` — comentário `TODO [ND-ASYNC-METRICS-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `ND-ASYNC-METRICS-03`, o Caso correspondente falha: m.init >= 1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `ND-ASYNC-METRICS-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```javascript
export function countPhases(events) {
    // PEDAGOGY-SOLUTION: ND-ASYNC-METRICS-03
    const m = {};
    for (const e of events) m[e.phase] = (m[e.phase] || 0) + 1;
    return m;
}
```

### Por que funciona?

Por quê este corpo satisfaz `ND-ASYNC-METRICS-03`: ele implementa exatamente o contrato do
teste (m.init >= 1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `ND-ASYNC-METRICS-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e4 Promise.resolve com hooks`):
