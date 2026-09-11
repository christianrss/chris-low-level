# Resolucao guiada — worker_pool_scheduler

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-NODE-POOL` | `starter/pool.js` | `createPool` |
| `D9-NODE-SUBMIT` | `starter/pool.js` | `submit` |
| `D9-NODE-SHUT` | `starter/pool.js` | `shutdown` |


## Baseline

```powershell
cd days/2026-09-11/nodejs/worker_pool_scheduler/starter
node test.js
```

**Esperado antes dos TODOs:** FAIL.


## D9-NODE-POOL

### Onde colocar (D9-NODE-POOL)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pool.js` |
| Funcao | `createPool` |
| Substituir | corpo sob `TODO [D9-NODE-POOL]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-NODE-POOL` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-NODE-POOL`.

### Escreva o codigo

```javascript
  return { size, active: 0, q: [], closed: false, nextId: 1 };
}
function submit(pool, fn) {
  if (pool.closed) return Promise.reject(new Error('closed'));
  const id = pool.nextId++;
  return new Promise((resolve, reject) => {
    const job = { id, fn, resolve, reject };
    if (pool.active < pool.size) run(pool, job);
```

### Por que funciona?
Materializa o contrato numerico de `D9-NODE-POOL`.

### Verifique
Baseline parcial; `D9-NODE-POOL` PASS.

### Checkpoint
- [ ] `D9-NODE-POOL` PASS

## D9-NODE-SUBMIT

### Onde colocar (D9-NODE-SUBMIT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pool.js` |
| Funcao | `submit` |
| Substituir | corpo sob `TODO [D9-NODE-SUBMIT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-NODE-SUBMIT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-NODE-SUBMIT`.

### Escreva o codigo

```javascript
  if (pool.closed) return Promise.reject(new Error('closed'));
  const id = pool.nextId++;
  return new Promise((resolve, reject) => {
    const job = { id, fn, resolve, reject };
    if (pool.active < pool.size) run(pool, job);
    else pool.q.push(job);
  });
}
```

### Por que funciona?
Materializa o contrato numerico de `D9-NODE-SUBMIT`.

### Verifique
Baseline parcial; `D9-NODE-SUBMIT` PASS.

### Checkpoint
- [ ] `D9-NODE-SUBMIT` PASS

## D9-NODE-SHUT

### Onde colocar (D9-NODE-SHUT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pool.js` |
| Funcao | `shutdown` |
| Substituir | corpo sob `TODO [D9-NODE-SHUT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-NODE-SHUT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-NODE-SHUT`.

### Escreva o codigo

```javascript
  pool.closed = true;
  return pool.active === 0 && pool.q.length === 0;
}
module.exports = { createPool, submit, shutdown };
```

### Por que funciona?
Materializa o contrato numerico de `D9-NODE-SHUT`.

### Verifique
Baseline parcial; `D9-NODE-SHUT` PASS.

### Checkpoint
- [ ] `D9-NODE-SHUT` PASS

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
