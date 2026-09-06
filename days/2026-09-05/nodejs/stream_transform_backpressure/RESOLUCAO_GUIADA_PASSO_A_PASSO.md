# RESOLUÇÃO GUIADA — Node.js / Stream transform + backpressure

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `NODE-XFORM-01` | `starter/line_transform.js` | `_transform`, `_flush` — split UTF-8 |
| `NODE-BACKPRESSURE-02` | `starter/backpressure_demo.js` | `runBackpressureDemo` — `write`/`drain` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test.js`.

> Trabalhe em `days/2026-09-05/nodejs/stream_transform_backpressure/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Rode `node test.js` após cada TODO.

---

## NODE-XFORM-01 — LineTransform UTF-8

### 1. O problema (starter stub)

```javascript
_transform(chunk, encoding, callback) {
    // TODO [NODE-XFORM-01]: dividir linhas UTF-8 com suporte a multibyte
    callback();
}
_flush(callback) {
    // TODO [NODE-XFORM-01]: emitir linha pendente no final
    callback();
}
```

O teste escreve `a\n\n`, depois `b` + 1º byte de `€`, depois resto de `€` + `\nc`. Sem `StringDecoder` + `pending`, `€` parte e `lines` ≠ `['a','','b€','c']`.

### 2. O algoritmo

```text
_transform(chunk):
  text ← pending + decoder.write(chunk)
  parts ← text.split('\n')
  pending ← parts.pop()   // fragmento sem \n final
  para cada line em parts: push(line)
  callback()

_flush():
  pending ← pending + decoder.end()
  se pending.length > 0: push(pending)
  callback()
```

### 3. Código completo

Em `starter/line_transform.js` (classe já tem `decoder` e `pending` no construtor):

```javascript
_transform(chunk, encoding, callback) {
    const text = this.pending + this.decoder.write(chunk);
    const parts = text.split('\n');
    this.pending = parts.pop() ?? '';
    for (const line of parts) {
        this.push(line);
    }
    callback();
}

_flush(callback) {
    this.pending += this.decoder.end();
    if (this.pending.length > 0) {
        this.push(this.pending);
    }
    callback();
}
```

### 4. Por que funciona?

- `StringDecoder`: retém bytes UTF-8 incompletos entre chunks; `toString()` quebraria `€` (`E2 82 AC`).
- `pending + write`: junta resto da linha anterior com texto novo.
- `split('\n')` + `pop()`: linhas completas saem; o último pedaço (sem `\n`) fica pendente — inclusive string vazia entre `\n\n`.
- `_flush` + `decoder.end()`: emite resto e caracteres retidos no decoder.

### 5. Verificação parcial

Trace do teste:

```text
write "a\n\n"              → push 'a', push ''
write "b" + E2            → pending 'b' (decoder guarda E2)
write 82 AC + "\nc"       → text "b€\nc" → push 'b€', pending 'c'
end / _flush              → push 'c'
→ ['a', '', 'b€', 'c']
```

```bash
cd days/2026-09-05/nodejs/stream_transform_backpressure/starter
node test.js
```

Esperado **ainda FAIL** em backpressure se `NODE-BACKPRESSURE-02` estiver stub.

---

## NODE-BACKPRESSURE-02 — respeitar `write() === false`

### 1. O problema (starter stub)

```javascript
// TODO [NODE-BACKPRESSURE-02]: escrever 50 buffers de 8 bytes;
// quando write() retornar false, aguarde 'drain' antes de continuar.
for (let i = 0; i < 50; i++) {
    sink.write(Buffer.alloc(8));
}
```

`highWaterMark: 8` + chunks de 8 bytes → buffer enche rápido. Sem `await drain`, `falseWrites` fica 0 → `backpressure not observed`.

### 2. O algoritmo

```text
falseWrites ← 0; drains ← 0
para i em 0..49:
  ok ← sink.write(Buffer.alloc(8))
  se !ok:
    falseWrites++
    await once(sink, 'drain')
    drains++
sink.end(); await once(sink, 'finish')
exigir falseWrites > 0 e drains === falseWrites
```

### 3. Código completo

Substitua o loop em `starter/backpressure_demo.js` (`runBackpressureDemo` já declara `falseWrites`/`drains` e o `Writable` lento):

```javascript
for (let i = 0; i < 50; i++) {
    const ok = sink.write(Buffer.alloc(8));
    if (!ok) {
        falseWrites++;
        await once(sink, 'drain');
        drains++;
    }
}
```

O resto da função (`sink.end()`, `await finish`, asserts, `return`) permanece.

### 4. Por que funciona?

- `write` retorna `false` quando o buffer interno ≥ `highWaterMark` — sinal para pausar.
- `once(sink, 'drain')`: retoma só quando o `write` interno chamou `callback` o bastante para esvaziar.
- Contar `falseWrites` e `drains` 1:1 prova que você esperou em cada pausa (não só “escreveu rápido”).
- `setTimeout(callback, 2)` no sink garante que o produtor pode adiantar e observar backpressure.

### 5. Verificação

```bash
node test.js
```

Saída esperada (números variam; relação não):

```text
OK node streams { falseWrites: <n>, drains: <n> }
```

Demo isolada: `node backpressure_demo.js`.

Debug: `falseWrites === 0` → chunks menores que HWM ou loop incompleto; hang → `await drain` sem o sink completar `callback`.

---

## Mapa de consistência auditada

- `NODE-XFORM-01` — `starter/line_transform.js` → `solutions/line_transform.js`.
- `NODE-BACKPRESSURE-02` — `starter/backpressure_demo.js` → `solutions/backpressure_demo.js`.

## Relatório de resolução

### O que foi validado

- TODOs `NODE-XFORM-01` e `NODE-BACKPRESSURE-02` nos dois starters.
- `test.js`: linhas `['a','','b€','c']`; `falseWrites > 0` e `drains === falseWrites`.
- Starter falha em assert de linhas e/ou backpressure até ambos existirem.

### Armadilhas encontradas

- `chunk.toString('utf8')` sem `StringDecoder` parte multibyte.
- Aguardar `drain` sem checar `!ok` (contadores divergem).
- Esquecer `_flush` / `decoder.end()`.

### Depuração e saída esperada

- **Depuração:** logue `parts` e `pending` em `_transform`; logue `ok` no loop de write.
- **Saída esperada:** `OK node streams { falseWrites, drains }`.

### Próximo passo sugerido

Refazer sem a resolução. Meça taxa de `drain` vs HWM em `BENCHMARK_GUIADO.md`.
