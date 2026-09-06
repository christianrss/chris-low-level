// PEDAGOGY-SOLUTION: ND-GZ-02
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
