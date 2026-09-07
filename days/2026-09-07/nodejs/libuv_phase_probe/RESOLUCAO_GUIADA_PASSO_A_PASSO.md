# Resolução guiada — Node.js libuv phase probe

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-NODE-PROBE` | `starter/probe.js` | `probe` |
| `D5-NODE-BOUNDED` | `starter/probe.js` | `boundedNextTick` |
| `D5-NODE-YIELD` | `starter/probe.js` | `yieldImmediate` |

Marcadores: `TODO [ID]`, `PEDAGOGY-SOLUTION: ID`, `PEDAGOGY-TEST: ID` em `starter/test.js`.

> Trabalhe em `days/2026-09-07/nodejs/libuv_phase_probe/starter/probe.js`.

## Baseline

```powershell
cd days/2026-09-07/nodejs/libuv_phase_probe
node starter/test.js
```

**Esperado:** FAIL — `probe` retorna `[]`; bounded/yield não implementados.

---

## D5-NODE-PROBE — capturar ordem parcial

### O problema

Stub retorna array vazio. Teste exige `"sync"` primeiro, presença de cinco tags e microtasks antes de macro callbacks.

Stub:

```javascript
export async function probe(){
 // TODO [D5-NODE-PROBE]: capture ordem parcial.
 return [];
}
```

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/probe.js` |
| **Função / âncora** | `probe` — comentário `TODO [D5-NODE-PROBE]` |
| **Substituir** | corpo `return []` |
| **Não mexer** | exports das outras funções neste passo |

### Código completo

```javascript
export async function probe(){
  const e = ["sync"];
  process.nextTick(() => e.push("nextTick"));
  Promise.resolve().then(() => e.push("promise"));
  await new Promise(r => {
    let n = 2, d = () => { if (--n === 0) r(); };
    setTimeout(() => { e.push("timeout"); d(); }, 0);
    setImmediate(() => { e.push("immediate"); d(); });
  });
  return e;
}
```

### Por que funciona?

- `"sync"` entra antes de qualquer schedule — código síncrono inicial.
- `nextTick` e `Promise.then` rodam na fase microtask/nextTick, antes de timer/immediate do mesmo setup.
- Barreira `n=2` garante que timeout e immediate executaram antes do return.
- Não impõe ordem entre timeout e immediate — alinhado ao teste.

### Verificação parcial

```powershell
node -e "import {probe} from './starter/probe.js'; const e=await probe(); console.log(e);"
```

**Esperado:** array com 5 tags; `e[0]==="sync"`.

---

## D5-NODE-BOUNDED — recursão nextTick limitada

### O problema

Stub retorna `0`. Teste chama `boundedNextTick(25)` e espera `25`.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/probe.js` |
| **Função / âncora** | `boundedNextTick` — `TODO [D5-NODE-BOUNDED]` |
| **Substituir** | `return 0` |
| **Não mexer** | `probe` já passando |

### Código completo

```javascript
export async function boundedNextTick(limit){
  if (limit < 0) throw new Error("limit");
  return await new Promise(r => {
    let c = 0;
    function step(){
      if (c >= limit) return r(c);
      c++;
      process.nextTick(step);
    }
    process.nextTick(step);
  });
}
```

### Por que funciona?

- Cada `nextTick(step)` cede e reexecuta na fila nextTick — incremento uma vez por tick.
- Quando `c >= limit`, resolve com total acumulado (= limit para entradas positivas).
- `limit < 0` falha cedo conforme contrato implícito do lab.

### Verificação parcial

```powershell
node -e "import {boundedNextTick} from './starter/probe.js'; console.log(await boundedNextTick(5));"
```

**Esperado:** `5`.

---

## D5-NODE-YIELD — Promise via setImmediate

### O problema

Stub `Promise.resolve()` resolve no microtask imediato — teste seta flag em `setImmediate` e espera `true` após await.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/probe.js` |
| **Função / âncora** | `yieldImmediate` — `TODO [D5-NODE-YIELD]` |
| **Substituir** | `return Promise.resolve()` |
| **Não mexer** | probe e bounded |

### Código completo

```javascript
export function yieldImmediate(){
  return new Promise(r => setImmediate(r));
}
```

### Por que funciona?

- `setImmediate` agenda callback na fase check — após microtasks pendentes.
- Teste agenda `setImmediate(() => x=true)` e depois `await yieldImmediate()` — segunda volta do check permite primeira callback rodar.
- Retorna Promise consumível em loop async cooperativo.

### Verificação final

```powershell
node starter/test.js
```

**Esperado:** `chris-node-phase tests passed`.

---

## Debug

| Sintoma | Causa | Correção |
|---------|-------|----------|
| probe sem timeout/immediate | return cedo | await barreira |
| ordering Error | exigiu ordem timer/immediate | remova suposição |
| bounded retorna 0 | loop síncrono | use nextTick recursivo |
| yield falha | Promise.resolve | use setImmediate |

Use `node --trace-warnings starter/test.js` para warnings; timestamps opcionais com `hrtime.bigint()` só para observação.

---

## Relatório de resolução

1. **Primeiro item do array probe:** _____
2. **Relação garantida entre promise/nextTick e macro:** _____
3. **Por que boundedNextTick usa nextTick e não while?** _____
4. **Diferença yieldImmediate vs Promise.resolve():** _____
5. **Valor retornado por boundedNextTick(25):** _____
