import asyncHooks from 'node:async_hooks';

export function installHooks(store) {
    // PEDAGOGY-SOLUTION: ND-ASYNC-HOOK-01
    asyncHooks.createHook({
        init(asyncId, type, triggerAsyncId) {
            store.events.push({ phase: 'init', asyncId, type, triggerAsyncId });
        },
        before(asyncId) { store.events.push({ phase: 'before', asyncId }); },
        after(asyncId) { store.events.push({ phase: 'after', asyncId }); },
    }).enable();
}

export function formatTimeline(events) {
    // PEDAGOGY-SOLUTION: ND-ASYNC-TIMELINE-02
    return events.map(e => `${e.phase}:${e.asyncId}`).join('|');
}

export function countPhases(events) {
    // PEDAGOGY-SOLUTION: ND-ASYNC-METRICS-03
    const m = {};
    for (const e of events) m[e.phase] = (m[e.phase] || 0) + 1;
    return m;
}
