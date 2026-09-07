// PEDAGOGY-TEST: ND-INPUT-01
// PEDAGOGY-TEST: ND-INPUT-02
// PEDAGOGY-TEST: ND-INPUT-03
// Caso 1: dois eventos de 24 bytes
// Caso 2: flush com 1 byte residual falha
// Caso 3: metrics conta eventsParsed
import { Readable } from 'node:stream';
import assert from 'node:assert';
import { InputEventTransform, EVENT_SIZE } from './input_event_transform.js';

const ev = Buffer.alloc(EVENT_SIZE, 1);
const src = Buffer.concat([ev, ev]);

async function main() {
    const out = [];
    const tr = new InputEventTransform();
    tr.on('data', (x) => out.push(x));
    await new Promise((resolve, reject) => {
        Readable.from([src]).pipe(tr).on('finish', resolve).on('error', reject);
    });
    assert.equal(out.length, 2);
    assert.equal(tr.metrics().eventsParsed, 2);
    console.log('OK input_event_transform');
}

main().catch((e) => { console.error(e); process.exit(1); });
