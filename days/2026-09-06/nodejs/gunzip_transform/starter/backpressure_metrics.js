// TODO [ND-GZ-02]
import { Writable } from 'node:stream';
import { once } from 'node:events';

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

    // TODO [ND-GZ-02]: escrever chunks gzipados; respeitar backpressure do transform
    const payload = Buffer.from('x'.repeat(4096));
    for (let i = 0; i < 40; i++) {
        transform.write(payload);
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
