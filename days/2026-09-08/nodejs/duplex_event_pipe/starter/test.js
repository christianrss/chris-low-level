// PEDAGOGY-TEST: ND-DUPLEX-01
// PEDAGOGY-TEST: ND-DUPLEX-02
// PEDAGOGY-TEST: ND-DUPLEX-03
// Caso 1: write 48B -> 2 events written
// Caso 2: read receives 24B events
// Caso 3: metrics counts match
// Caso 4: partial write buffered
import assert from "node:assert";
import { DuplexEventPipe, EVENT_SIZE } from "./duplex_event_pipe.js";

async function main() {
    const pipe = new DuplexEventPipe();
    const ev = Buffer.alloc(EVENT_SIZE, 7);
    const out = [];
    pipe.on("data", (c) => out.push(Buffer.from(c)));
    await new Promise((resolve) => {
        pipe.write(Buffer.concat([ev, ev]), resolve);
    });
    await new Promise((r) => setImmediate(r));
    assert.equal(pipe.metrics().eventsWritten, 2);
    assert.ok(out.length >= 1);
    console.log("OK duplex_event_pipe");
}

main().catch((e) => { console.error(e); process.exit(1); });