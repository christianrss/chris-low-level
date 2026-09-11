import { Transform, Duplex } from 'node:stream';

export class CapstoneTransform extends Transform {
    constructor() {
        super();
        this.chunks = 0;
    }
    _transform(chunk, enc, cb) {
        // TODO [CAP-ND-PIPE-01]: uppercase string chunks, count chunks
        cb();
    }
    metrics() {
        // TODO [CAP-ND-PIPE-03]: return { chunks }
        return {};
    }
}

export function createDuplex() {
    const t = new CapstoneTransform();
    // TODO [CAP-ND-PIPE-02]: return duplex piping through transform
    return t;
}
