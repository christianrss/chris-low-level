// PEDAGOGY-TEST: ND-ASYNC-HOOK-01
// PEDAGOGY-TEST: ND-ASYNC-TIMELINE-02
// PEDAGOGY-TEST: ND-ASYNC-METRICS-03
// Caso 1: init event
// Caso 2: timeline contains init
// Caso 3: init count >= 1
import assert from 'node:assert';
import { installHooks, formatTimeline, countPhases } from './async_trace.js';

async function main() {
    const store = { events: [] };
    installHooks(store);
    await Promise.resolve();
    assert.ok(store.events.some(e => e.phase === 'init'));
    const tl = formatTimeline(store.events);
    assert.ok(tl.includes('init'));
    const m = countPhases(store.events);
    assert.ok(m.init >= 1);
    console.log('OK async_trace');
}

main().catch(e => { console.error(e); process.exit(1); });
