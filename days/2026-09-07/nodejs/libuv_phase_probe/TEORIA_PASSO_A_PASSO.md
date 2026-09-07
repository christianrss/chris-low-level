# Teoria passo a passo — Node.js libuv phase probe (D5-NODE)

## 1. O que estamos construindo

Três utilitários ESM em Node puro: **`probe()`** registra ordem parcial de callbacks (sync, microtask, nextTick, timer, immediate); **`boundedNextTick(limit)`** demonstra recursão `nextTick` limitada; **`yieldImmediate()`** cede controle via `setImmediate`. Sem dependências externas.

TODOs: `D5-NODE-PROBE`, `D5-NODE-BOUNDED`, `D5-NODE-YIELD`.

## 2. Por quê fases do event loop importam

Node não é “uma fila FIFO”. Timers, I/O poll, check (immediate) e **microtasks** (`Promise.then`) rodam em pontos distintos do ciclo libuv. `process.nextTick` roda **antes** de continuar o loop principal — prioridade extra que pode **starvar** I/O se reenfileirado sem limite. Entender ordem parcial evita bugs de teste flaky e servidores que nunca respondem.

## 3. Mapa simplificado do ciclo

```text
   ┌─────────────┐
   │  sync code  │  ← probe: "sync"
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │  microtasks │  ← Promise.then → "promise"
   │  nextTick   │  ← process.nextTick → "nextTick"
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │ timers      │  ← setTimeout(0) → "timeout"
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │ check       │  ← setImmediate → "immediate"
   └─────────────┘
```

Ordem exata entre `timeout` e `immediate` **não é garantida globalmente** — o teste só exige relações parciais.

| API | Fase típica | Lab |
|-----|-------------|-----|
| `Promise.then` | microtask | `promise` |
| `process.nextTick` | nextTick queue | `nextTick` |
| `setTimeout(0)` | timers | `timeout` |
| `setImmediate` | check | `immediate` |

## 4. Probe de ordem (`D5-NODE-PROBE`)

### O quê
`probe()` retorna array de strings na ordem observada de execução dos callbacks agendados.

### Como
1. `events = ["sync"]` — código síncrono roda primeiro.
2. Agende `process.nextTick`, `Promise.resolve().then`, `setTimeout(0)`, `setImmediate`.
3. Aguarde timer **e** immediate com contador (barreira de 2).
4. Retorne `events`.

```javascript
const e = ["sync"];
process.nextTick(() => e.push("nextTick"));
Promise.resolve().then(() => e.push("promise"));
await new Promise(r => {
  let n = 2, d = () => { if (--n === 0) r(); };
  setTimeout(() => { e.push("timeout"); d(); }, 0);
  setImmediate(() => { e.push("immediate"); d(); });
});
return e;
```

### Por quê
Testes determinísticos de concorrência exigem **barreira** — sem `await`, a função retornaria antes dos callbacks macro. Registrar ordem parcial ensina o que é garantido vs dependente de versão/carga.

### Trace manual — relações garantidas pelo teste

```text
e[0] === "sync"
"nextTick" e "promise" presentes
"timeout" e "immediate" presentes
indexOf("promise") e indexOf("nextTick") < min(indexOf("timeout"), indexOf("immediate"))
```

### Invariantes
- Primeiro elemento sempre `sync`.
- Microtasks/nextTick antes dos callbacks macro agendados no mesmo tick de setup.

### Bugs comuns
- Retornar antes do `await` da barreira.
- Exigir `timeout` antes de `immediate` (ordem não fixa).
- Esquecer `setImmediate` na contagem.

## 5. nextTick limitado (`D5-NODE-BOUNDED`)

### O quê
`boundedNextTick(limit)` executa `process.nextTick` recursivamente **limit** vezes e resolve Promise com contagem final.

### Como
```text
se limit < 0 → throw
Promise com step recursivo:
  step: count++; se count >= limit → resolve(count)
        senão process.nextTick(step)
iniciar com process.nextTick(step)
```

### Por quê
Recursão infinita de `nextTick` bloqueia fases posteriores — starvation. Limite transforma anti-padrão em experimento reprodutível (`boundedNextTick(25) === 25`).

### Trace manual — limit=3

```text
tick1: c=1 → requeue
tick2: c=2 → requeue
tick3: c=3 → resolve(3)
```

### Invariantes
- Retorno numérico igual a `limit` para entradas válidas.
- `limit < 0` rejeitado.

### Bugs comuns
- Loop `while` síncrono — nunca cede.
- Resolver antes de completar contagens.
- Não iniciar via `process.nextTick` — conta errada.

## 6. Yield cooperativo (`D5-NODE-YIELD`)

### O quê
`yieldImmediate()` retorna Promise resolvida no próximo check phase — ponto de cooperação para trabalho CPU-bound.

### Como
```javascript
return new Promise(r => setImmediate(r));
```

### Por quê
Código síncrono longo sem awaits impede timers e I/O. `setImmediate` roda após poll — melhor que busy-wait para “fatia” de trabalho entre batches.

### Trace manual — teste yield

```text
setImmediate(() => x = true)
await yieldImmediate()
x deve ser true — callback check rodou
```

### Invariantes
- Retorna Promise (async-friendly).
- Não usa `setTimeout(0)` — fase diferente do probe.

### Bugs comuns
- `Promise.resolve()` imediato — não cede ao loop.
- `process.nextTick` — prioridade excessiva, não simula yield macro.

## 7. Fluxo mental do probe

```text
sync push ──► schedule nextTick, promise, timer, immediate
                    │
                    ▼
              await barrier (2)
                    │
                    ▼
              return events[]
```

## 8. Comparação com produção

| Este lab | Apps Node reais |
|----------|-----------------|
| Array de strings | APM, async_hooks |
| nextTick limitado | backpressure, setImmediate batching |
| Ordem parcial | testes com fake timers |

Transferível: **não assumir ordem total** entre timer e immediate.

## 9. Passo a passo guiado

1. `D5-NODE-PROBE` — `probe.js` com barreira.
2. `D5-NODE-BOUNDED` — recursão limitada.
3. `D5-NODE-YIELD` — Promise + setImmediate.
4. `node starter/test.js` → `chris-node-phase tests passed`.

## 10. Como saber se está correto

- `probe()[0] === "sync"`.
- `promise` e `nextTick` antes de macro callbacks.
- `boundedNextTick(25) === 25`.
- Após `await yieldImmediate()`, flag setada em immediate passa.

## 11. Invariantes globais

- Exports ESM: `probe`, `boundedNextTick`, `yieldImmediate`.
- Sem alterar assinaturas do starter.

## 12. Por quê este módulo existe

Tornar **visível** o scheduler que normalmente esconde race silenciosa. Cada TODO protege suposição falsa sobre “async = aleatório” ou “nextTick é inofensivo”.
