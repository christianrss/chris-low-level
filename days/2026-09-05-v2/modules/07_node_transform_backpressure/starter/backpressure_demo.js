// TODO [NODE-BACKPRESSURE-02]: respeitar write() === false e aguardar drain
import { Writable } from 'node:stream';
import { once } from 'node:events';

const sink = new Writable({ highWaterMark: 8, write(chunk, enc, cb) { setTimeout(cb, 2); } });
let falseWrites = 0;
for (let i = 0; i < 50; i++) {
  const ok = sink.write(Buffer.alloc(8));
  if (!ok) {
    falseWrites++;
    // TODO: await once(sink, 'drain');
  }
}
sink.end();
await once(sink, 'finish');
console.log({ falseWrites });
