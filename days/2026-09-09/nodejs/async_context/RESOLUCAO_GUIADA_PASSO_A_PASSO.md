# Resolucao guiada — async_context

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-NODE-ALS` | `starter/async_context.js` | `createStore` |
| `D7-NODE-RUN` | `starter/async_context.js` | `runWith` |
| `D7-NODE-GET` | `starter/async_context.js` | `currentId` |


## Baseline

```powershell
cd days/2026-09-09/nodejs/async_context/starter
node test.js
```

**Esperado antes dos TODOs:** FAIL.


## D7-NODE-ALS

### Onde colocar (D7-NODE-ALS)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/async_context.js` |
| Funcao | `createStore` |
| Substituir | corpo sob `TODO [D7-NODE-ALS]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-NODE-ALS` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```javascript
  return new AsyncLocalStorage();
}
function runWith(store, id, fn) {
  return store.run({ id }, fn);
}
function currentId(store) {
  const s = store.getStore();
  return s ? s.id : null;
```

### Por que funciona?
Materializa o contrato numerico de `D7-NODE-ALS`.

### Verifique
Baseline parcial; `D7-NODE-ALS` PASS.

### Checkpoint
- [ ] `D7-NODE-ALS` PASS

## D7-NODE-RUN

### Onde colocar (D7-NODE-RUN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/async_context.js` |
| Funcao | `runWith` |
| Substituir | corpo sob `TODO [D7-NODE-RUN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-NODE-RUN` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```javascript
  return store.run({ id }, fn);
}
function currentId(store) {
  const s = store.getStore();
  return s ? s.id : null;
}
module.exports = { createStore, runWith, currentId };
```

### Por que funciona?
Materializa o contrato numerico de `D7-NODE-RUN`.

### Verifique
Baseline parcial; `D7-NODE-RUN` PASS.

### Checkpoint
- [ ] `D7-NODE-RUN` PASS

## D7-NODE-GET

### Onde colocar (D7-NODE-GET)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/async_context.js` |
| Funcao | `currentId` |
| Substituir | corpo sob `TODO [D7-NODE-GET]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-NODE-GET` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```javascript
  const s = store.getStore();
  return s ? s.id : null;
}
module.exports = { createStore, runWith, currentId };
```

### Por que funciona?
Materializa o contrato numerico de `D7-NODE-GET`.

### Verifique
Baseline parcial; `D7-NODE-GET` PASS.

### Checkpoint
- [ ] `D7-NODE-GET` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco |
| off-by-one | size | refaca trace |

## Relatorio de resolucao

- TODOs:
- Saida:
- Invariantes:
- Benchmark: nao executado
