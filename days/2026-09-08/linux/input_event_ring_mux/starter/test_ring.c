#include "ring.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* PEDAGOGY-TEST: LIN-MUX-01 */
/* PEDAGOGY-TEST: LIN-MUX-02 */
/* PEDAGOGY-TEST: LIN-MUX-03 */
int main(void) {
    EventRing r; InputEvent ev; int i;
    memset(&r, 0, sizeof r);
    assert(mux_push(&r, 1, 1, 10) == 0);
    assert(mux_push(&r, 2, 2, -3) == 0);
    assert(ring_pop(&r, &ev) == 0);
    assert(ev.source == 1 && ev.value == 10);
    assert(ring_pop(&r, &ev) == 0 && ev.source == 2 && ev.value == -3);
    memset(&r, 0, sizeof r);
    for (i = 0; i < RING_CAP; i++) assert(ring_push(&r, ev) == 0);
    assert(ring_push(&r, ev) == -1);
    printf("OK ring\n");
    return 0;
}
