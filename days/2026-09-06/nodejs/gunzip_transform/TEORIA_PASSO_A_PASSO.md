# Teoria passo a passo — GunzipTransform (ND-GZ)

## 1. O que estamos construindo

Um `Transform` Node.js que encapsula `zlib.createGunzip()`: encaminha chunks gzipados, emite plaintext, respeita **backpressure** e expõe métricas `bytesIn` / `bytesOut` / `backpressurePauses`. Arquivos: `gunzip_transform.js`, `backpressure_metrics.js`, teste em `test.js`.

TODOs: `ND-GZ-01` (`_transform`/`_flush`), `ND-GZ-02` (demo de backpressure), `ND-GZ-03` (métricas — sobretudo `bytesIn`).

## 2. Por que Transform + gunzip

ETL e proxies descomprimem em streaming. `zlib.createGunzip()` já é um stream; envelopá-lo num `Transform` permite `readable.pipe(gunzipTransform).pipe(sink)` com API uniforme, erros via `destroy`, e métricas de expansão.

## 3. Anatomia do `GunzipTransform` (`ND-GZ-01`)

### O quê
Classe `extends Transform`. Construtor cria `this.gunzip`, liga:

```text
gunzip 'data'  → bytesOut += len; push(chunk); se !ok → pause + backpressurePauses++
gunzip 'end'   → push(null)
gunzip 'error' → destroy(err)
this 'drain'   → gunzip.resume()
```

(O starter já traz esses handlers; você completa `_transform` / `_flush`.)

### Como
```text
_transform(chunk, encoding, callback):
  bytesIn += chunk.length          # ND-GZ-03
  ok ← gunzip.write(chunk)
  se !ok: gunzip.once('drain', callback); return
  callback()

_flush(callback):
  gunzip.end(callback)
```

### Por quê
Sem `gunzip.write`, o teste recebe saída vazia. Sem `gunzip.end` no `_flush`, o stream pode nunca emitir `end` — hang no `await once(transform,'end')`.

### Trace — teste oficial

```text
raw = "PORTAL-VERLET-DAY06\n" × 200
gz  = gzipSync(raw)
transform.end(gz)
após end:
  Buffer.concat(chunks) === raw
  bytesIn === gz.length
  bytesOut > bytesIn   (texto expandiu)
```

### Invariantes
- Round-trip UTF-8 idêntico ao `raw`.
- Todo byte de entrada conta em `bytesIn`.
- Erro gzip → `destroy` (pipeline não trava forever).

### Bugs comuns
- `_transform` só chama `callback()` sem `write`.
- `_flush` vazio.
- Contar `bytesIn` no handler `data` (aí conta saída, não entrada).

## 4. Backpressure no produtor (`ND-GZ-02`)

### O quê
`runGunzipBackpressureDemo(gunzipFactory)` escreve o gzip em fatias; quando `transform.write` retorna `false`, espera `drain` e conta `falseWrites`/`drains`.

### Como (gabarito)
```text
sink ← Writable({ highWaterMark: 16, write: setTimeout(cb,1) })
transform ← gunzipFactory(); transform.pipe(sink)
gz ← gzipSync("LOWLEVEL"×512)
para cada slice de 64 bytes de gz:
  ok ← transform.write(slice)
  se !ok: falseWrites++; await once(transform,'drain'); drains++
transform.end(); await end/finish
exigir falseWrites > 0 e drains === falseWrites
```

### Por quê o starter falha
O stub escreve `Buffer('x'.repeat(4096))` **sem gzip** direto no transform — gunzip rejeita / não observa o padrão do teste. Além disso, não espera `drain` quando `write` retorna `false`.

### Por quê highWaterMark baixo + delay
Força o sink a ser mais lento que o produtor → `write` retorna `false` → backpressure real.

### Trace mental

```text
write(slice) → false  (buffer interno cheio)
falseWrites = 1
await 'drain'
drains = 1
…
assert drains === falseWrites
```

### Invariantes
- `falseWrites > 0` (senão o lab não provou backpressure).
- `drains === falseWrites` (cada pausa tem um resume).
- `stats.bytesOut > 0` após o demo.

### Bugs comuns
- Esquecer `await once(...,'drain')` → inundar memória / assert falha.
- Alimentar plaintext em vez de gzip.
- Chunk size grande demais → às vezes `falseWrites==0` flaky; 64 B + HWM 16 é o desenho do gabarito.

## 5. Métricas (`ND-GZ-03`)

### O quê
- `bytesIn`: soma dos chunks em `_transform`.
- `bytesOut`: soma no handler `gunzip.on('data')` (já no starter).
- `backpressurePauses`: quando `push` retorna `false` (já no starter).

### Como
Garanta `this.bytesIn += chunk.length` no início de `_transform`. Não remova a lógica de `bytesOut`/`pause` do construtor.

### Por quê
O teste oficial exige `transform.bytesIn === gz.length` e `bytesOut > bytesIn`. Sem `bytesIn`, ND-GZ-01 “funciona” visualmente mas falha o assert de métricas.

### Invariantes
- Após um `end(gz)` one-shot: `bytesIn == gz.length`.
- Para texto repetitivo gzipado: `bytesOut > bytesIn`.

## 6. Fluxo mental

```text
gzip bytes
    │
    ▼
_transform → gunzip.write (+ bytesIn)
    │
    ▼
gunzip 'data' → push (+ bytesOut, possible pause)
    │
    ▼
downstream Writable (pode gerar backpressure)
```

## 7. Complexidade

| Peça | Nota |
|------|------|
| gunzip | O(n) DEFLATE inflate |
| backpressure | O(chunks); awaits por false write |
| memória | limitada por HWM se respeitado |

## 8. Comparação com produção

| Este lab | Produção |
|----------|----------|
| Transform didático | `zlib.createGunzip()` direto no pipe |
| métricas manuais | OpenTelemetry / counters |
| demo com HWM 16 | HWM default ~16 KiB |

## 9. Passo a passo guiado

1. `ND-GZ-01` — `_transform` / `_flush`.
2. `ND-GZ-03` — `bytesIn` (com out/pauses do construtor).
3. `ND-GZ-02` — demo com `gzipSync` + drain.
4. `node starter/test.js` → `OK gunzip transform …`.

## 10. Como saber se está correto

- Round-trip do texto `PORTAL-VERLET-DAY06`.
- `bytesIn` / `bytesOut` asserts.
- Demo: `falseWrites > 0` e `drains == falseWrites`.

## 11. Invariantes globais

- ESM (`"type":"module"` no `package.json`).
- Factory `() => new GunzipTransform()` no demo.
- Não troque `createGunzip` por `gunzipSync` dentro do Transform.

## 12. Bugs comuns (checklist)

| Sintoma | Causa |
|---------|--------|
| saída vazia | sem `gunzip.write` |
| hang | sem `gunzip.end` no `_flush` |
| bytesIn undefined/0 | falta `+=` em `_transform` |
| backpressure not observed | plaintext ou sem await drain |

## 13. Por quê este módulo existe

Treinar **streaming + backpressure + métricas** no mesmo objeto — o trio que evita OOM em pipelines reais de gunzip.
