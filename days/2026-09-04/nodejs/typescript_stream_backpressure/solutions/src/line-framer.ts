import { Transform, type TransformCallback } from 'node:stream';

export class LineFramer extends Transform {
  #pending: Buffer = Buffer.alloc(0);
  readonly maxLineBytes: number;

  constructor(maxLineBytes = 64 * 1024) {
    super({ readableObjectMode: true });
    if (!Number.isInteger(maxLineBytes) || maxLineBytes <= 0) throw new RangeError('maxLineBytes must be a positive integer');
    this.maxLineBytes = maxLineBytes;
  }

  _transform(chunk: Buffer | string, encoding: BufferEncoding, callback: TransformCallback): void {
    try {
      const incoming = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, encoding);
      this.#pending = this.#pending.length === 0 ? Buffer.from(incoming) : Buffer.concat([this.#pending, incoming]);
// PEDAGOGY-SOLUTION: D2-NODE-FRAME-LINES
      let newline: number;
      while ((newline = this.#pending.indexOf(0x0A)) !== -1) {
        const line = this.#pending.subarray(0, newline);
        if (line.length > this.maxLineBytes) throw new RangeError('line exceeds maxLineBytes');
        this.push(line.toString('utf8'));
        this.#pending = Buffer.from(this.#pending.subarray(newline + 1));
      }
      if (this.#pending.length > this.maxLineBytes) throw new RangeError('unterminated line exceeds maxLineBytes');
      callback();
    } catch (error) { callback(error as Error); }
  }

  _flush(callback: TransformCallback): void {
    try {
      if (this.#pending.length > 0) {
        if (this.#pending.length > this.maxLineBytes) throw new RangeError('line exceeds maxLineBytes');
        this.push(this.#pending.toString('utf8'));
      }
      this.#pending = Buffer.alloc(0);
      callback();
    } catch (error) { callback(error as Error); }
  }
}
