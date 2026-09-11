import { Duplex } from "node:stream";

export const EVENT_SIZE = 24;

export class DuplexEventPipe extends Duplex {
    constructor() {
        super();
        this._writeBuf = Buffer.alloc(0);
        this._readBuf = Buffer.alloc(0);
        this.eventsWritten = 0;
        this.eventsRead = 0;
    }

    _write(chunk, encoding, callback) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-01
        this._writeBuf = Buffer.concat([this._writeBuf, chunk]);
        while (this._writeBuf.length >= EVENT_SIZE) {
            const ev = this._writeBuf.subarray(0, EVENT_SIZE);
            this._writeBuf = this._writeBuf.subarray(EVENT_SIZE);
            this._readBuf = Buffer.concat([this._readBuf, ev]);
            this.eventsWritten++;
        }
        this._read(EVENT_SIZE);
        callback();
    }

    _read(size) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-02
        while (this._readBuf.length >= EVENT_SIZE) {
            const ev = this._readBuf.subarray(0, EVENT_SIZE);
            this._readBuf = this._readBuf.subarray(EVENT_SIZE);
            this.eventsRead++;
            if (!this.push(ev)) break;
        }
    }

    metrics() {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-03
        return { eventsWritten: this.eventsWritten, eventsRead: this.eventsRead };
    }
}
