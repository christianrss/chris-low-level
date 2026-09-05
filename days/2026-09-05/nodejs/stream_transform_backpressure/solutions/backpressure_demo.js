// PEDAGOGY-SOLUTION: NODE-BACKPRESSURE-02
import { Writable } from 'node:stream';
import { once } from 'node:events';

export async function runBackpressureDemo() {
    const sink = new Writable({
        highWaterMark: 8,
        write(chunk, encoding, callback) {
            setTimeout(callback, 2);
        },
    });

    let falseWrites = 0;
    let drains = 0;

    for (let i = 0; i < 50; i++) {
        const ok = sink.write(Buffer.alloc(8));
        if (!ok) {
            falseWrites++;
            await once(sink, 'drain');
            drains++;
        }
    }

    sink.end();
    await once(sink, 'finish');

    if (falseWrites === 0 || drains !== falseWrites) {
        throw new Error('backpressure not observed');
    }

    return { falseWrites, drains };
}

if (import.meta.url === `file://${process.argv[1]}`) {
    const stats = await runBackpressureDemo();
    console.log(stats);
}
