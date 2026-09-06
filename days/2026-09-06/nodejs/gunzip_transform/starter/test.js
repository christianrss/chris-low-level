// PEDAGOGY-TEST: ND-GZ-01: GunzipTransform descomprime gzip em stream
// PEDAGOGY-TEST: ND-GZ-02: backpressure falseWrites e drains
// PEDAGOGY-TEST: ND-GZ-03: métricas bytesIn/bytesOut integradas
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `node starter/test.js` — gunzip + backpressure.
// Caso 2: **Gunzip:** payload gzipado vira texto original.
// Caso 3: **Backpressure:** falseWrites > 0 e drains == falseWrites.
// Caso 4: **Métricas:** bytesOut > bytesIn para payload repetitivo.
// Caso 5: Valide solutions/ com os mesmos asserts.
import assert from 'node:assert/strict';
import { once } from 'node:events';
import zlib from 'node:zlib';
import { runGunzipBackpressureDemo } from './backpressure_metrics.js';
import { GunzipTransform } from './gunzip_transform.js';

async function main() {
    const raw = 'PORTAL-VERLET-DAY06\n'.repeat(200);
    const gz = zlib.gzipSync(Buffer.from(raw, 'utf8'));

    const transform = new GunzipTransform();
    const chunks = [];
    transform.on('data', (c) => chunks.push(c));
    transform.end(gz);
    await once(transform, 'end');

    const out = Buffer.concat(chunks).toString('utf8');
    assert.equal(out, raw);
    assert.ok(transform.bytesIn === gz.length);
    assert.ok(transform.bytesOut > transform.bytesIn);

    const stats = await runGunzipBackpressureDemo(() => new GunzipTransform());
    assert.ok(stats.falseWrites > 0);
    assert.equal(stats.drains, stats.falseWrites);
    assert.ok(stats.bytesOut > 0);

    console.log('OK gunzip transform', stats);
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
