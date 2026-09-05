# Resolução guiada passo a passo — Node.js/TypeScript streams e backpressure

## Mapa exato starter → resolução
- `D2-NODE-FRAME-LINES` → `starter/src/line-framer.ts` → `LineFramer._transform`.

Neste milestone, normalização de chunk, `_flush` e o demo de backpressure **já vêm implementados como infraestrutura de leitura**. O exercício de código é o framing entre chunks; as demais partes são estudadas e depuradas, não fingidas como TODOs.

## 0. Baseline
```bash
node --experimental-strip-types --test starter/tests/*.test.ts
```
O starter deve falhar no teste de framing porque mantém bytes em `#pending` sem emitir linhas completas.

## 1. Leia o scaffolding já fornecido
Abra `starter/src/line-framer.ts`.

Dentro de `_transform`, estas duas linhas **já existem**:
```ts
const incoming = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, encoding);
this.#pending = this.#pending.length === 0
  ? Buffer.from(incoming)
  : Buffer.concat([this.#pending, incoming]);
```
Explique com suas palavras por que `Buffer` é usado em vez de concatenar strings: um caractere UTF-8 multibyte pode ser dividido entre chunks; manter bytes evita decodificar uma sequência parcial.

Também leia `_flush`: ele emite o último fragmento quando a stream termina sem `\n`. Não reimplemente essa função hoje.

## 2. `D2-NODE-FRAME-LINES` — extrair linhas completas
No TODO de `starter/src/line-framer.ts`, substitua `newline = -1` pelo bloco:
```ts
let newline: number;
while ((newline = this.#pending.indexOf(0x0A)) !== -1) {
  const line = this.#pending.subarray(0, newline);
  if (line.length > this.maxLineBytes) throw new RangeError('line exceeds maxLineBytes');
  this.push(line.toString('utf8'));
  this.#pending = Buffer.from(this.#pending.subarray(newline + 1));
}
```
Depois mantenha a validação que já está logo abaixo:
```ts
if (this.#pending.length > this.maxLineBytes)
  throw new RangeError('unterminated line exceeds maxLineBytes');
```

### Por que copiar o remainder?
`subarray` é uma view para o mesmo backing buffer. `Buffer.from(subarray)` copia apenas o remainder; neste milestone isso simplifica ownership e evita manter acidentalmente um buffer grande vivo por causa de poucos bytes restantes.

## 3. Testes
```bash
node --experimental-strip-types --test starter/tests/*.test.ts
```
Agora existem quatro casos concretos:
1. delimitadores atravessando chunks;
2. linha sem terminador acima do limite;
3. linha vazia;
4. caractere UTF-8 multibyte dividido fisicamente entre dois Buffers.

Esperado: 4 testes passando e 0 falhando.

## 4. Backpressure — código fornecido para observação
Abra `starter/src/demo.ts`. Não há TODO aqui. O `Writable` usa `highWaterMark: 1` e só chama `callback` depois de um pequeno atraso. Rode:
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
A `pipeline()` coordena o fluxo; o objetivo é observar que o produtor não precisa despejar todos os objetos de uma vez no consumidor lento.

## Debugging
Adicione temporariamente dentro de `_transform`:
```ts
console.error({
  pending: this.#pending.length,
  readableLength: this.readableLength,
  writableLength: this.writableLength
});
```
Se `beta` virar `be` e `ta`, você emitiu por chunk, não por delimitador. Se memória crescer com entrada sem newline, confirme que `maxLineBytes` é verificado depois do loop. Para o teste UTF-8, inspecione `this.#pending.toString('hex')` antes de decodificar.

## Solução final comentada
Depois dos quatro testes verdes, compare apenas o bloco `PEDAGOGY-SOLUTION: D2-NODE-FRAME-LINES` em `solutions/src/line-framer.ts`. Não há implementação escondida de `_flush` ou do demo para você copiar.
