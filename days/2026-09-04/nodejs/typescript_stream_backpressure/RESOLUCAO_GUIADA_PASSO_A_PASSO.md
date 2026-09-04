# Resolução guiada passo a passo

Abra `starter/src/line-framer.ts`.

## 1. Fácil — normalizar chunk
Dentro de `_transform`, converta string/Buffer em Buffer:
```ts
const incoming = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, encoding);
```
Acumule com o fragmento anterior:
```ts
this.#pending = this.#pending.length === 0
  ? Buffer.from(incoming)
  : Buffer.concat([this.#pending, incoming]);
```

## 2. Médio — extrair linhas completas
Enquanto existir byte `0x0A`:
```ts
while ((newline = this.#pending.indexOf(0x0A)) !== -1) {
  const line = this.#pending.subarray(0, newline);
  if (line.length > this.maxLineBytes) throw new RangeError('line exceeds maxLineBytes');
  this.push(line.toString('utf8'));
  this.#pending = Buffer.from(this.#pending.subarray(newline + 1));
}
```
Por que copiar o remainder? Para este milestone queremos ownership simples e evitar manter acidentalmente um backing buffer muito maior que o fragmento restante.

## 3. Difícil — linha final e limite
Depois do loop:
```ts
if (this.#pending.length > this.maxLineBytes)
  throw new RangeError('unterminated line exceeds maxLineBytes');
```
Em `_flush`, emita o último fragmento sem newline e limpe o buffer.

## 4. Executar testes
```bash
node --experimental-strip-types --test starter/tests/*.test.ts
```
Esperado:
```text
pass 2
fail 0
```

## 5. Backpressure real
Abra `starter/src/demo.ts`. O `Writable` usa `highWaterMark: 1` e atrasa cada callback. Rode:
```bash
node --experimental-strip-types starter/src/demo.ts
```
Esperado:
```text
sink:alpha
sink:beta
sink:gamma
completed writes=3
```

## Debugging
Adicione temporariamente:
```ts
console.error({ pending: this.#pending.length, readableLength: this.readableLength, writableLength: this.writableLength });
```
Se `beta` virar `be` + `ta`, você está emitindo por chunk, não por delimitador. Se memória crescer com input sem newline, confirme que `maxLineBytes` é verificado também **antes** de `_flush`.
