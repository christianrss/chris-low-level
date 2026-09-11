import { Transform, Duplex } from 'node:stream';

export class CapstoneTransform extends Transform {
    constructor() {
        super();
        this.chunks = 0;
    }
    _transform(chunk, enc, cb) {
        // PEDAGOGY-SOLUTION: CAP-ND-PIPE-01
        this.chunks++;
        this.push(Buffer.from(String(chunk).toUpperCase()));
        cb();
    }
    metrics() {
        // PEDAGOGY-SOLUTION: CAP-ND-PIPE-03
        return { chunks: this.chunks };
    }
}

export function createDuplex() {
    const t = new CapstoneTransform();
    // PEDAGOGY-SOLUTION: CAP-ND-PIPE-02
    return t;
}
