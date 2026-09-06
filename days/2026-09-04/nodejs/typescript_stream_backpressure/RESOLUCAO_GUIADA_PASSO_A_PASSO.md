# RESOLUÇÃO GUIADA — Node.js/TypeScript streams e backpressure

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `D2-NODE-FRAME-LINES` | `starter/src/line-framer.ts` | `LineFramer._transform` — loop de `\n` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-04/nodejs/typescript_stream_backpressure/starter/`. `solutions/` é gabarito.

Neste milestone, **normalização de chunk**, `_flush` e o demo de backpressure **já vêm implementados**. O único TODO de código é o framing entre chunks; o resto é leitura e observação.

---

## Baseline

```bash
node --experimental-strip-types --test starter/tests/*.test.ts
```

O starter falha no framing: acumula bytes em `#pending` mas o TODO deixa `newline = -1`, então nenhuma linha é emitida (ou o comportamento fica incompleto). Quatro testes cobrem o contrato:

1. delimitadores atravessando chunks;
2. linha sem terminador acima do limite;
3. linha vazia (`\n\n`);
4. UTF-8 multibyte partido entre dois `Buffer`s.

---

## Leitura guiada do scaffolding (não é TODO)

Abra `starter/src/line-framer.ts`. Dentro de `_transform`, **já existem**:

```ts
const incoming = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, encoding);
this.#pending = this.#pending.length === 0
  ? Buffer.from(incoming)
  : Buffer.concat([this.#pending, incoming]);
```

### Por que `Buffer` e não `string`?

Um caractere UTF-8 (ex.: `€` = `E2 82 AC`) pode ser dividido entre chunks. Concatenar strings forçaria decode parcial e corromperia o código. Manter bytes adia o `toString('utf8')` até a linha estar completa (ou até `_flush`).

Leia `_flush`: se sobrar `#pending` no EOF, emite a última linha sem exigir `\n`. Não reimplemente `_flush`.

Construtor já valida:

```ts
if (!Number.isInteger(maxLineBytes) || maxLineBytes <= 0)
  throw new RangeError('maxLineBytes must be a positive integer');
```

---

## Exercício — `D2-NODE-FRAME-LINES`

### 1. O problema

TCP/`Readable` entrega **chunks**, não mensagens. Sem framing:

- emitir o chunk inteiro → linhas partidas (`be` + `ta`);
- acumular até EOF → OOM em streams longas;
- procurar `\n` sem limite → DoS se nunca vier newline.

O TODO pede: achar `0x0A`, emitir linhas completas, reter só o resto, respeitar `maxLineBytes`.

### 2. O algoritmo

```text
pending já contém bytes acumulados (feito pelo scaffolding)
loop:
  idx = indexOf(0x0A) em pending
  se idx == -1: break
  line = pending[0:idx]          // sem o \n
  se line.length > maxLineBytes: RangeError
  push(line como utf8 string)
  pending = cópia de pending[idx+1:]
se pending.length > maxLineBytes: RangeError  // já no starter abaixo do TODO
callback()
```

Invariante após o loop: `#pending` é sufixo **sem** `\n` completo.

### 3. Escreva o código

Substitua o placeholder `newline = -1` pelo bloco:

```ts
let newline: number;
while ((newline = this.#pending.indexOf(0x0A)) !== -1) {
  const line = this.#pending.subarray(0, newline);
  if (line.length > this.maxLineBytes) throw new RangeError('line exceeds maxLineBytes');
  this.push(line.toString('utf8'));
  this.#pending = Buffer.from(this.#pending.subarray(newline + 1));
}
```

Mantenha a validação que já está logo abaixo:

```ts
if (this.#pending.length > this.maxLineBytes)
  throw new RangeError('unterminated line exceeds maxLineBytes');
```

### 4. Por que funciona

#### Trace — chunks cruzados

Entrada do teste: `['a\nb', 'eta\nlast']`

```text
após chunk1: pending = "a\nb"
  emite "a"; pending = "b"
após chunk2: pending = "beta\nlast"
  emite "beta"; pending = "last"
_flush:        emite "last"
resultado:     ["a", "beta", "last"]
```

Se você emitisse por chunk, `beta` viraria `b` + `eta`.

#### Por que `Buffer.from(subarray(...))`?

`subarray` é view do mesmo backing store. Sem cópia, um `#pending` pequeno manteria vivo um buffer enorme concatenado. A cópia do remainder libera o backing grande para o GC.

#### Linha vazia

`a\n\nb\n` → índices de `\n` emitem `"a"`, `""`, `"b"`. O `subarray(0, newline)` com `newline==0` é buffer vazio — correto.

#### UTF-8 partido

`€\n` em hex `E2 82 AC 0A`. Se o primeiro chunk for só `E2`, `#pending` guarda bytes; só após juntar `82 AC 0A` o `indexOf(0x0A)` encontra o delimitador e `toString('utf8')` produz `"€"`.

#### Limite

`collect(['12345'], 4)` nunca vê `\n`; após o loop, `pending.length === 5 > 4` → `RangeError` com `/maxLineBytes/`.

### 5. Verifique

```bash
node --experimental-strip-types --test starter/tests/*.test.ts
```

Esperado: 4 testes passando, 0 falhando.

---

## Observação — backpressure (código fornecido)

Abra `starter/src/demo.ts`. Não há TODO. O `Writable` usa `highWaterMark: 1` e atrasa o `callback`. Rode:

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

`pipeline()` coordena o fluxo: o produtor não despeja tudo de uma vez no consumidor lento. O exercício de código é framing; o demo prova que a máquina de streams aplica pressão.

---

## Debugging

Adicione temporariamente em `_transform` (remova depois):

```ts
console.error({
  pending: this.#pending.length,
  readableLength: this.readableLength,
  writableLength: this.writableLength
});
```

| Sintoma | Causa provável |
|---------|----------------|
| `beta` vira `be`/`ta` | emitiu por chunk, não por `\n` |
| loop infinito | não avançou após `\n` (`pending` igual) |
| OOM sem newline | falta check `maxLineBytes` pós-loop |
| `€` vira `` / replacement | decode antes da linha completa |
| perde última linha | `_flush` quebrado (não edite; compare starter) |

Para UTF-8: `this.#pending.toString('hex')` antes do `toString('utf8')`.

---

## Mapa de consistência auditada

- `D2-NODE-FRAME-LINES` — `starter/src/line-framer.ts` → `solutions/src/line-framer.ts`

Compare apenas o bloco `PEDAGOGY-SOLUTION: D2-NODE-FRAME-LINES`. Não há implementação escondida de `_flush` ou do demo para copiar.

---

## Relatório de resolução

### O que foi validado

- Framing com `\n` atravessando chunks.
- Linha vazia, UTF-8 partido, rejeição por `maxLineBytes`.
- Demo observável de backpressure (`completed writes=3`).

### Armadilhas encontradas

- Tratar chunk como mensagem.
- Manter view `subarray` sem copiar o remainder (retenção de buffer grande).
- Validar só linhas completas e esquecer pending sem `\n`.

### Depuração e saída esperada

- **Depuração:** log de `pending.length`; hex antes do decode.
- **Saída esperada:** 4/4 testes; demo com três sinks.

### Próximo passo sugerido

Meça linhas/s e RSS no benchmark do módulo; varie `maxLineBytes` e anote se o gargalo é `Buffer.concat` ou `toString`.
