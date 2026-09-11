#include "ring.h"
int ring_push(EventRing *r, InputEvent ev) {
    /* TODO [LIN-MUX-01] */
    (void)r; (void)ev; return -1;
}
int ring_pop(EventRing *r, InputEvent *out) {
    /* TODO [LIN-MUX-02] */
    (void)r; (void)out; return -1;
}
int mux_push(EventRing *r, uint8_t source, uint16_t type, int32_t value) {
    /* TODO [LIN-MUX-03] */
    (void)r; (void)source; (void)type; (void)value; return -1;
}
