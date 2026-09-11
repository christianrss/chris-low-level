// PEDAGOGY-TEST: CAP-ND-PIPE-01
// PEDAGOGY-TEST: CAP-ND-PIPE-02
// PEDAGOGY-TEST: CAP-ND-PIPE-03
import { Readable } from 'node:stream';
import assert from 'node:assert';
import { createDuplex } from './capstone_stream_pipeline.js';

async function main() {
    const out = [];
    const dup = createDuplex();
    dup.on('data', (c) => out.push(c.toString()));
    await new Promise((res, rej) => {
        Readable.from(['hello']).pipe(dup).on('finish', res).on('error', rej);
    });
    assert.equal(out.join(''), 'HELLO');
    assert.equal(dup.metrics().chunks, 1);
    console.log('OK node pipeline');
}
main().catch((e) => { console.error(e); process.exit(1); });
