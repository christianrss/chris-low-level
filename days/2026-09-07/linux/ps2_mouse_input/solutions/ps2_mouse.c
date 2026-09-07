// PEDAGOGY-SOLUTION: PS2-MOUSE-DECODE-01
// PEDAGOGY-SOLUTION: PS2-MOUSE-EVENT-02
// PEDAGOGY-SOLUTION: PS2-MOUSE-RING-03
// PEDAGOGY-SOLUTION: PS2-MOUSE-READ-04
#include "ps2_mouse.h"
#include <string.h>

static uint64_t g_time_us = 0;

void ps2_mouse_set_time(uint64_t time_us) {
    g_time_us = time_us;
}

void ps2_mouse_decode(const uint8_t pkt[3], Ps2MousePacket* out) {
    uint8_t flags = pkt[0];
    out->buttons = flags & 0x07;
    int dx = (int)pkt[1];
    int dy = (int)pkt[2];
    if (flags & 0x10) {
        dx -= 256;
    }
    if (flags & 0x20) {
        dy -= 256;
    }
    out->dx = dx;
    out->dy = dy;
}

ssize_t ps2_mouse_map_events(
    const Ps2MousePacket* cur,
    const Ps2MousePacket* prev,
    InputEvent* out,
    size_t max_out) {
    size_t n = 0;

    if (cur->dx != 0 && n < max_out) {
        out[n].time_us = g_time_us;
        out[n].type = EV_REL;
        out[n].code = REL_X;
        out[n].value = cur->dx;
        out[n].__pad = 0;
        ++n;
    }
    if (cur->dy != 0 && n < max_out) {
        out[n].time_us = g_time_us;
        out[n].type = EV_REL;
        out[n].code = REL_Y;
        out[n].value = cur->dy;
        out[n].__pad = 0;
        ++n;
    }

    static const struct {
        uint8_t mask;
        uint16_t btn;
    } btn_map[] = {
        {0x01, BTN_LEFT},
        {0x02, BTN_RIGHT},
        {0x04, BTN_MIDDLE},
    };

    for (size_t i = 0; i < 3 && n < max_out; ++i) {
        int cur_on = (cur->buttons & btn_map[i].mask) != 0;
        int prev_on = (prev->buttons & btn_map[i].mask) != 0;
        if (cur_on != prev_on) {
            out[n].time_us = g_time_us;
            out[n].type = EV_KEY;
            out[n].code = btn_map[i].btn;
            out[n].value = cur_on ? 1 : 0;
            out[n].__pad = 0;
            ++n;
        }
    }

    return (ssize_t)n;
}

int ps2_mouse_ring_push(Ps2MouseRing* ring, const InputEvent* ev) {
    if (ring->count >= PS2_MOUSE_RING_CAP) {
        return -1;
    }
    ring->buf[ring->tail] = *ev;
    ring->tail = (ring->tail + 1) % PS2_MOUSE_RING_CAP;
    ++ring->count;
    return 0;
}

ssize_t ps2_mouse_ring_read(Ps2MouseRing* ring, InputEvent* out, size_t max_out) {
    size_t n = 0;
    while (n < max_out && ring->count > 0) {
        out[n] = ring->buf[ring->head];
        ring->head = (ring->head + 1) % PS2_MOUSE_RING_CAP;
        --ring->count;
        ++n;
    }
    return (ssize_t)n;
}
