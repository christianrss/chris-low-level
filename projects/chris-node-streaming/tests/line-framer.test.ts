import test from 'node:test';
import assert from 'node:assert/strict';
import { Readable } from 'node:stream';
import { LineFramer } from '../src/line-framer.ts';

async function collect(chunks: Array<Buffer | string>, maxLineBytes = 1024): Promise<string[]> {
  const out: string[] = [];
  const framer = new LineFramer(maxLineBytes);
  framer.on('data', (line: string) => out.push(line));
  await new Promise<void>((resolve, reject) => {
    Readable.from(chunks).pipe(framer).on('finish', resolve).on('error', reject);
  });
  return out;
}

test('frames across arbitrary chunk boundaries', async () => {
  assert.deepEqual(await collect(['a\nb', 'eta\nlast']), ['a', 'beta', 'last']);
});

test('rejects oversized unterminated line', async () => {
  await assert.rejects(() => collect(['12345'], 4), /maxLineBytes/);
});
