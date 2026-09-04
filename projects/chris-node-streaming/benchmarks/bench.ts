import { performance } from 'node:perf_hooks';
import { Readable } from 'node:stream';
import { LineFramer } from '../src/line-framer.ts';

const lines = 100_000;
const input = Buffer.from(('abcdefghij\n').repeat(lines));
for (let warm = 0; warm < 2; ++warm) await run();
const samples: number[] = [];
for (let i = 0; i < 5; ++i) samples.push(await run());
console.log(JSON.stringify({ lines, samples_ms: samples, median_ms: [...samples].sort((a,b)=>a-b)[2] }));

async function run(): Promise<number> {
  const start = performance.now();
  let count = 0;
  const framer = new LineFramer();
  framer.on('data', () => count++);
  await new Promise<void>((resolve, reject) => Readable.from([input]).pipe(framer).on('finish', resolve).on('error', reject));
  if (count !== lines) throw new Error(`expected ${lines}, got ${count}`);
  return performance.now() - start;
}
