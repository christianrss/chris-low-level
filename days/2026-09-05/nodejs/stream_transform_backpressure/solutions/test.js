// PEDAGOGY-TEST [NODE-XFORM-01]: split de linhas UTF-8 com caractere multibyte
// PEDAGOGY-TEST [NODE-BACKPRESSURE-02]: demo integrada de drain/falseWrites
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
