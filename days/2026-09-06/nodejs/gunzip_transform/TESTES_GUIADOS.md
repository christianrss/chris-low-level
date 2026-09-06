# Testes guiados — GunzipTransform

## Por que testar streams?

Gunzip “funciona” em one-shot e ainda assim vaza memória sob backpressure, ou mente métricas. `starter/test.js` amarra round-trip, bytes e drains aos IDs `ND-GZ-01..03`.

## Caso 1 — gunzip stream (PEDAGOGY-TEST: ND-GZ-01)

1. `raw = 'PORTAL-VERLET-DAY06\n'.repeat(200)`.
2. `gz = zlib.gzipSync(Buffer.from(raw,'utf8'))`.
3. `transform.end(gz)`; colete `data`; `await once(transform,'end')`.
4. `Buffer.concat(chunks).toString('utf8') === raw`.

**Invariante:** plaintext idêntico.

**Se falhar:** `_transform` sem `write` ou `_flush` sem `end`.

## Caso 2 — métricas (PEDAGOGY-TEST: ND-GZ-03)

1. Mesmo fluxo do Caso 1.
2. `transform.bytesIn === gz.length`.
3. `transform.bytesOut > transform.bytesIn`.

**Invariante:** entrada = tamanho gzip; saída expandida para texto repetitivo.

**Se falhar:** falta `bytesIn +=`; ou `bytesOut` removido do handler `data`.

## Caso 3 — backpressure (PEDAGOGY-TEST: ND-GZ-02)

1. `stats = await runGunzipBackpressureDemo(() => new GunzipTransform())`.
2. `stats.falseWrites > 0`.
3. `stats.drains === stats.falseWrites`.
4. `stats.bytesOut > 0`.

**Invariante:** cada `write===false` teve um `drain`.

**Se falhar:** demo ainda escreve plaintext; ou não `await drain`.

## Cobertura pedagógica auditada

- `ND-GZ-01` — Caso 1.
- `ND-GZ-03` — Caso 2.
- `ND-GZ-02` — Caso 3.

## Como depurar

1. Saída vazia → logue se `_transform` chama `gunzip.write`.
2. Hang → verifique `_flush` → `gunzip.end`.
3. Backpressure → `console.log(ok, falseWrites)` no loop; confira magic `1f8b` do `gz`.
