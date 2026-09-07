import { Transform } from 'node:stream';

export const EVENT_SIZE = 24;

export class InputEventTransform extends Transform {
    constructor() {
        super({ readableObjectMode: true });
        this.buffer = Buffer.alloc(0);
        this.eventsParsed = 0;
        this.backpressurePauses = 0;
    }

    _transform(chunk, encoding, callback) {
        // TODO [ND-INPUT-01]: accumulate buffer, emit complete 24-byte events
        callback();
    }

    _flush(callback) {
        // TODO [ND-INPUT-02]: reject trailing partial bytes
        callback();
    }

    metrics() {
        // TODO [ND-INPUT-03]: return { eventsParsed, backpressurePauses }
        return {};
    }
}
