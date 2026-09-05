// PEDAGOGY-TEST: NODE-XFORM-01: split de linhas UTF-8 com caractere multibyte
// PEDAGOGY-TEST: NODE-BACKPRESSURE-02: demo integrada de drain/falseWrites
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `node starter/test.js` — LineTransform + backpressure integrados.
// Caso 2: **UTF-8 multibyte:** caractere € partido entre chunks → linha `b€`.
// Caso 3: **Backpressure:** `runBackpressureDemo()` deve ter falseWrites > 0 e drains == f
// Caso 4: Rode `node backpressure_demo.js` isoladamente para observar stats.
// Caso 5: Valide solutions/ com os mesmos asserts.
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { runBackpressureDemo } from './backpressure_demo.js';
import { LineTransform } from './line_transform.js';

const transform = new LineTransform();
const lines = [];
transform.on('data', (line) => lines.push(line));

const euro = Buffer.from('€');
transform.write(Buffer.from('a\n\n'));
transform.write(Buffer.concat([Buffer.from('b'), euro.subarray(0, 1)]));
transform.write(Buffer.concat([euro.subarray(1), Buffer.from('\nc')]));
transform.end();
await once(transform, 'end');

assert.deepEqual(lines, ['a', '', 'b€', 'c']);

const { falseWrites, drains } = await runBackpressureDemo();
assert.ok(falseWrites > 0);
assert.equal(drains, falseWrites);

console.log('OK node streams', { falseWrites, drains });