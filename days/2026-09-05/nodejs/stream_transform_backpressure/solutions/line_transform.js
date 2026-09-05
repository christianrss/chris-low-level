// PEDAGOGY-SOLUTION: NODE-XFORM-01
import { Transform } from 'node:stream';
import { StringDecoder } from 'node:string_decoder';

export class LineTransform extends Transform {
    constructor() {
        super({ readableObjectMode: true });
        this.decoder = new StringDecoder('utf8');
        this.pending = '';
    }

    _transform(chunk, encoding, callback) {
        const text = this.pending + this.decoder.write(chunk);
        const parts = text.split('\n');
        this.pending = parts.pop() ?? '';
        for (const line of parts) {
            this.push(line);
        }
        callback();
    }

    _flush(callback) {
        this.pending += this.decoder.end();
        if (this.pending.length > 0) {
            this.push(this.pending);
        }
        callback();
    }
}
