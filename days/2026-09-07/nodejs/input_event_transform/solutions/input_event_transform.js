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
        // PEDAGOGY-SOLUTION: ND-INPUT-01
        this.buffer = Buffer.concat([this.buffer, chunk]);
        while (this.buffer.length >= EVENT_SIZE) {
            const ev = this.buffer.subarray(0, EVENT_SIZE);
            this.buffer = this.buffer.subarray(EVENT_SIZE);
            this.eventsParsed++;
            const ok = this.push({ raw: Buffer.from(ev) });
            if (!ok) this.backpressurePauses++;
        }
        callback();
    }

    _flush(callback) {
        // PEDAGOGY-SOLUTION: ND-INPUT-02
        if (this.buffer.length > 0) {
            callback(new Error('trailing partial event'));
            return;
        }
        callback();
    }

    metrics() {
        // PEDAGOGY-SOLUTION: ND-INPUT-03
        return { eventsParsed: this.eventsParsed, backpressurePauses: this.backpressurePauses };
    }
}
