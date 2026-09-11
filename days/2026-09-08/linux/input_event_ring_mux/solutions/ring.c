#include "ring.h"
int ring_push(EventRing *r, InputEvent ev) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-01 */
    if (!r || r->count >= RING_CAP) return -1;
    r->slots[r->tail] = ev;
    r->tail = (r->tail + 1) % RING_CAP;
    r->count++;
    return 0;
}
int ring_pop(EventRing *r, InputEvent *out) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-02 */
    if (!r || !out || r->count == 0) return -1;
    *out = r->slots[r->head];
    r->head = (r->head + 1) % RING_CAP;
    r->count--;
    return 0;
}
int mux_push(EventRing *r, uint8_t source, uint16_t type, int32_t value) {
    /* PEDAGOGY-SOLUTION: LIN-MUX-03 */
    InputEvent ev;
    ev.type = type; ev.value = value; ev.source = source;
    return ring_push(r, ev);
}
