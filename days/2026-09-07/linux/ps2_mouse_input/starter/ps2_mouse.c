// TODO [PS2-MOUSE-DECODE-01] [PS2-MOUSE-EVENT-02] [PS2-MOUSE-RING-03] [PS2-MOUSE-READ-04]
#include "ps2_mouse.h"
#include <string.h>

static uint64_t g_time_us = 0;

void ps2_mouse_set_time(uint64_t time_us) {
    g_time_us = time_us;
}

void ps2_mouse_decode(const uint8_t pkt[3], Ps2MousePacket* out) {
    // TODO [PS2-MOUSE-DECODE-01]
    memset(out, 0, sizeof(*out));
}

ssize_t ps2_mouse_map_events(
    const Ps2MousePacket* cur,
    const Ps2MousePacket* prev,
    InputEvent* out,
    size_t max_out) {
    // TODO [PS2-MOUSE-EVENT-02]
    (void)cur;
    (void)prev;
    (void)out;
    (void)max_out;
    return -1;
}

int ps2_mouse_ring_push(Ps2MouseRing* ring, const InputEvent* ev) {
    // TODO [PS2-MOUSE-RING-03]
    (void)ring;
    (void)ev;
    return -1;
}

ssize_t ps2_mouse_ring_read(Ps2MouseRing* ring, InputEvent* out, size_t max_out) {
    // TODO [PS2-MOUSE-READ-04]
    (void)ring;
    (void)out;
    (void)max_out;
    return -1;
}
