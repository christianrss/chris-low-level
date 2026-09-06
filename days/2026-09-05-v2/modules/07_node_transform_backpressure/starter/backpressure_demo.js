// TODO [NODE-BACKPRESSURE-01]: implement transform backpressure
import { Writable } from 'node:stream';
import { once } from 'node:events';

const sink = new Writable({ highWaterMark: 8, write(chunk, enc, cb) { setTimeout(cb, 2); } });
let falseWrites = 0;
for (let i = 0; i < 50; i++) {
  const ok = sink.write(Buffer.alloc(8));
  if (!ok) {
    falseWrites++;
  }
}
sink.end();
await once(sink, 'finish');
console.log({ falseWrites });
