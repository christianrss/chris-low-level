# Resolução guiada passo a passo — Node.js — Streams

## Mapa exato starter → resolução

- `NODE-XFORM-01` → `starter/line_transform.js` (`_transform`, `_flush`)
- `NODE-BACKPRESSURE-02` → `starter/backpressure_demo.js` (`runBackpressureDemo`)

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/nodejs/stream_transform_backpressure/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

```bash
cd days/2026-09-05/nodejs/stream_transform_backpressure/starter
node test.js
```

Baseline: falha porque `_transform` não emite linhas e/ou `runBackpressureDemo` lança `backpressure not observed`.

## Exercício médio — `NODE-XFORM-01` em `_transform`

### Arquivo

Abra `starter/line_transform.js`, localize `_transform`.

Substitua o corpo por:

```javascript
const text = this.pending + this.decoder.write(chunk);
const parts = text.split('\n');
this.pending = parts.pop() ?? '';
for (const line of parts) {
    this.push(line);
}
callback();
```

### Por que funciona?

- `decoder.write(chunk)` converte bytes UTF-8 em string, retendo bytes incompletos internamente.
- `pending` guarda texto da linha anterior que ainda não terminou com `\n`.
- `split('\n')` separa linhas completas; `pop()` deixa o fragmento final (sem newline) em `pending`.
- `push(line)` alimenta o lado readable em objectMode.

### Trace UTF-8 (do teste)

```text
write "a\n\n"     → push 'a', push ''
write "b" + 0xE2  → pending 'b'
write 0x82 0xAC + "\nc" → text "b€\nc" → push 'b€', push 'c'
```

## Exercício médio — `NODE-XFORM-01` em `_flush`

Localize `_flush`:

```javascript
this.pending += this.decoder.end();
if (this.pending.length > 0) {
    this.push(this.pending);
}
callback();
```

### Por que funciona?

`decoder.end()` emite caracteres retidos (multibyte incompleto). Se sobrou texto sem `\n` final, ele deve ser emitido como linha — o teste não depende disso para o caso `c` (há `\n` antes), mas `_flush` é invariante correta do Transform.

## Verificação parcial LineTransform

Comente temporariamente o bloco `runBackpressureDemo` em `test.js` ou rode só a parte do transform no REPL. Esperado após `end`:

```javascript
['a', '', 'b€', 'c']
```

## Exercício difícil — `NODE-BACKPRESSURE-02`

### Arquivo

Abra `starter/backpressure_demo.js`. Substitua o loop vazio por:

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

### Por que funciona?

- `Writable` com `highWaterMark: 8` e chunks de 8 bytes enchem o buffer rapidamente.
- `write` retorna `false` quando deve pausar — incrementamos `falseWrites`.
- `once(sink, 'drain')` bloqueia até o consumidor drenar — só então continuamos.
- Cada pausa corresponde a exatamente um `drain` → `drains === falseWrites`.

### Trace simplificado

```text
write #1 → true
write #2 → false → await drain → drains=1
...
após 50 writes: falseWrites > 0
```

## Rode os testes novamente

```bash
node test.js
```

Saída esperada (valores variam, relação não):

```text
OK node streams { falseWrites: <n>, drains: <n> }
```

Demo isolada:

```bash
node backpressure_demo.js
```

## Como depurar se falhar

- **`lines` vazio ou `['a']` só:** `_transform` não chama `push`; verifique `split` e loop.
- **`b` e `€` em linhas separadas:** você usou `toString()` em vez de `StringDecoder`.
- **`backpressure not observed` com `falseWrites === 0`:** `highWaterMark` ou tamanho do buffer — confira `Buffer.alloc(8)` e que o loop executa 50 vezes.
- **`drains !== falseWrites`:** você aguarda `drain` sem checar `!ok`, ou aguarda quando `ok` é true.
- **Hang infinito:** `await drain` sem o sink completar `callback` no `write` — o starter já tem `setTimeout(callback, 2)`.

## Solução final comentada

Compare com `solutions/line_transform.js` e `solutions/backpressure_demo.js`. Justifique: por que `pending` + `decoder`, e por que backpressure exige pareamento 1:1 entre `false` e `drain`.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| NODE-XFORM-01 | `line_transform.js` | `['a', '', 'b€', 'c']` com € partido entre chunks |
| NODE-BACKPRESSURE-02 | `backpressure_demo.js` | `falseWrites > 0` e `drains === falseWrites` |

Critério de aceite: `node test.js` imprime `OK node streams`. Se `b€` virar duas linhas, revise `StringDecoder` — não concatene Buffers como UTF-8 manualmente.
