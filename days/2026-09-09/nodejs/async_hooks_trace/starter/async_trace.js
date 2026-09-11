import asyncHooks from 'node:async_hooks';

export function installHooks(store) {
    // TODO [ND-ASYNC-HOOK-01]: register init/before/after into store.events
    void store;
}

export function formatTimeline(events) {
    // TODO [ND-ASYNC-TIMELINE-02]: phase:asyncId joined by |
    void events;
    return '';
}

export function countPhases(events) {
    // TODO [ND-ASYNC-METRICS-03]: count per phase
    void events;
    return {};
}
