import { Duplex } from "node:stream";

export const EVENT_SIZE = 24;

export class DuplexEventPipe extends Duplex {
    constructor() {
        super();
        this.buffer = Buffer.alloc(0);
        this.eventsWritten = 0;
        this.eventsRead = 0;
    }

    _write(chunk, encoding, callback) {
        // TODO [ND-DUPLEX-01]: accumulate 24B events from writes
        callback();
    }

    _read(size) {
        // TODO [ND-DUPLEX-02]: push complete 24B events to reader
    }

    metrics() {
        // TODO [ND-DUPLEX-03]: return { eventsWritten, eventsRead }
        return {};
    }
}
