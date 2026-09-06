# RESOLUÇÃO GUIADA — Node.js / GunzipTransform

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `ND-GZ-01` | `starter/gunzip_transform.js` | `_transform`, `_flush` |
| `ND-GZ-02` | `starter/backpressure_metrics.js` | loop de writes + drain |
| `ND-GZ-03` | `starter/gunzip_transform.js` | `bytesIn` (+ métricas out/pause no ctor) |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION` no gabarito e `PEDAGOGY-TEST` em `starter/test.js`.

> Trabalhe em `days/2026-09-06/nodejs/gunzip_transform/starter/`. `solutions/` só depois.

---

## ND-GZ-01 — encaminhar chunks ao gunzip

### 1. O problema (starter stub)

```javascript
_transform(chunk, encoding, callback) {
    // TODO [ND-GZ-01]
    callback();
}

_flush(callback) {
    // TODO [ND-GZ-01]
    callback();
}
```

Chamar só `callback()` sem `write`/`end` → saída vazia e/ou hang.

### 2. O algoritmo

```text
_transform:
  (bytesIn — ver ND-GZ-03)
  ok ← this.gunzip.write(chunk)
  se !ok: this.gunzip.once('drain', callback); return
  callback()

_flush:
  this.gunzip.end(callback)
```

### 3. Código completo (`_transform` + `_flush`)

Substitua os dois métodos em `starter/gunzip_transform.js` (já com `bytesIn` — ND-GZ-03):

```javascript
_transform(chunk, encoding, callback) {
    this.bytesIn += chunk.length;
    const ok = this.gunzip.write(chunk);
    if (!ok) {
        this.gunzip.once('drain', callback);
        return;
    }
    callback();
}

_flush(callback) {
    this.gunzip.end(callback);
}
```

### 4. Por que funciona? (entenda linha a linha)

- `gunzip.write(chunk)`: alimenta o inflate incremental.
- `ok === false`: buffer interno do gunzip cheio — **não** chame `callback` imediatamente; espere `drain` para não violar backpressure upstream.
- `gunzip.end(callback)`: sinaliza EOF ao zlib; quando flush interno termina, o callback do Transform dispara e o handler `'end'` faz `push(null)`.
- Construtor já liga `data`→`push`, `error`→`destroy` — não remova.

### 5. Verificação parcial

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\nodejs\gunzip_transform\starter
node --input-type=module -e "import zlib from 'node:zlib'; import { once } from 'node:events'; import { GunzipTransform } from './gunzip_transform.js'; const raw='hi\n'.repeat(10); const t=new GunzipTransform(); const c=[]; t.on('data',d=>c.push(d)); t.end(zlib.gzipSync(raw)); await once(t,'end'); console.log(Buffer.concat(c).toString()===raw, t.bytesIn, t.bytesOut);"
```

Esperado: `true` e `bytesOut > bytesIn`. A suite ainda pode falhar em `ND-GZ-02`.

---

## ND-GZ-03 — métricas bytesIn / bytesOut / pauses

### 1. O problema

O starter marca no construtor:

```javascript
// TODO [ND-GZ-03]: incrementar bytesIn/bytesOut e backpressurePauses
```

Na prática o gabarito já deixa `bytesOut` e `backpressurePauses` no handler `data`; o que **falta** no fluxo completo é `bytesIn` dentro de `_transform` (incluído no código da seção anterior).

### 2–4. Código e entendimento

Linha crítica:

```javascript
this.bytesIn += chunk.length;
```

Confirme que o construtor mantém:

```javascript
this.gunzip.on('data', (chunk) => {
    this.bytesOut += chunk.length;
    const ok = this.push(chunk);
    if (!ok) {
        this.gunzip.pause();
        this.backpressurePauses++;
    }
});
```

### 5. Critério

Após `transform.end(gz)`: `bytesIn === gz.length` e `bytesOut > bytesIn` no teste oficial.

---

## ND-GZ-02 — demo de backpressure

### 1. O problema (starter stub)

```javascript
// TODO [ND-GZ-02]: escrever chunks gzipados; respeitar backpressure do transform
const payload = Buffer.from('x'.repeat(4096));
for (let i = 0; i < 40; i++) {
    transform.write(payload);
}
```

Problemas: (1) plaintext não é gzip; (2) ignora retorno de `write`; (3) `falseWrites`/`drains` ficam 0 → `throw new Error('backpressure not observed')`.

### 2. O algoritmo

```text
raw ← Buffer("LOWLEVEL"×512)
gz ← zlib.gzipSync(raw)
chunkSize ← 64
para offset = 0; offset < gz.length; offset += 64:
  slice ← gz.subarray(offset, offset+64)
  ok ← transform.write(slice)
  se !ok: falseWrites++; await once(transform,'drain'); drains++
transform.end()
await end do transform e finish do sink
assert falseWrites > 0 && drains === falseWrites
```

### 3. Código completo

Substitua o corpo de `runGunzipBackpressureDemo` em `starter/backpressure_metrics.js` (mantenha o `Writable` sink e os contadores). Adicione `import zlib from 'node:zlib';` no topo:

```javascript
import { Writable } from 'node:stream';
import { once } from 'node:events';
import zlib from 'node:zlib';

export async function runGunzipBackpressureDemo(gunzipFactory) {
    const sink = new Writable({
        highWaterMark: 16,
        write(chunk, encoding, callback) {
            setTimeout(callback, 1);
        },
    });

    let falseWrites = 0;
    let drains = 0;

    const transform = gunzipFactory();
    transform.pipe(sink);

    const raw = Buffer.from('LOWLEVEL'.repeat(512));
    const gz = zlib.gzipSync(raw);
    const chunkSize = 64;
    for (let offset = 0; offset < gz.length; offset += chunkSize) {
        const slice = gz.subarray(offset, offset + chunkSize);
        const ok = transform.write(slice);
        if (!ok) {
            falseWrites++;
            await once(transform, 'drain');
            drains++;
        }
    }
    transform.end();
    await once(transform, 'end');
    await once(sink, 'finish');

    if (falseWrites === 0 || drains !== falseWrites) {
        throw new Error('backpressure not observed');
    }

    return {
        falseWrites,
        drains,
        bytesIn: transform.bytesIn,
        bytesOut: transform.bytesOut,
        backpressurePauses: transform.backpressurePauses,
    };
}
```

### 4. Por que funciona? (entenda linha a linha)

- `gzipSync`: o Transform espera envelope gzip, não ASCII cru.
- Fatias 64 B + sink HWM 16 + delay 1 ms: receita para `write===false`.
- `await once(transform,'drain')`: protocolo Node — só continue quando o buffer baixar.
- Contadores iguais: cada false write tem exatamente um drain esperado neste padrão.

### 5. Verificação completa

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\nodejs\gunzip_transform\starter
node test.js
```

Saída esperada (números variam):

```text
OK gunzip transform { falseWrites: N, drains: N, bytesIn: ..., bytesOut: ..., backpressurePauses: ... }
```

Gabarito:

```powershell
cd ..\solutions
node test.js
```

---

## Ordem sugerida

1. `_transform` / `_flush` + `bytesIn` (`ND-GZ-01`/`03`).
2. Demo backpressure (`ND-GZ-02`).
3. `node test.js`.
4. Compare com `solutions/`.

## Relatório de resolução

### O que foi validado

- TODOs `ND-GZ-01..03` em `gunzip_transform.js` e `backpressure_metrics.js`.
- Round-trip + métricas + `falseWrites`/`drains` no `test.js`.
- Starter original: saída vazia / backpressure não observado.

### Armadilhas encontradas

- `_flush` sem `gunzip.end` → hang em `once(...,'end')`.
- Demo com plaintext → gunzip error ou métricas inúteis.
- Esquecer `await drain` → assert `backpressure not observed` ou OOM.
- `bytesIn` só no construtor comment — precisa viver no `_transform`.

### Depuração e saída esperada

- **Depuração:** logue `ok` de cada `write`; confira `gz[0]===0x1f && gz[1]===0x8b`.
- **Saída esperada:** `OK gunzip transform` com `falseWrites > 0`.

### Próximo passo sugerido

Refazer sem gabarito. Em `BENCHMARK_GUIADO.md`, varie `chunkSize` e `highWaterMark` e registre quantos `falseWrites` aparecem.
