#pragma once
#include "input_event.h"
#include <stddef.h>
#include <stdint.h>

#if defined(_MSC_VER)
#include <basetsd.h>
typedef SSIZE_T ssize_t;
#else
#include <sys/types.h>
#endif

#define PS2_MOUSE_RING_CAP 32

typedef struct {
    int32_t dx;
    int32_t dy;
    uint8_t buttons;
} Ps2MousePacket;

typedef struct {
    InputEvent buf[PS2_MOUSE_RING_CAP];
    size_t head;
    size_t tail;
    size_t count;
} Ps2MouseRing;

void ps2_mouse_set_time(uint64_t time_us);
void ps2_mouse_decode(const uint8_t pkt[3], Ps2MousePacket* out);
ssize_t ps2_mouse_map_events(
    const Ps2MousePacket* cur,
    const Ps2MousePacket* prev,
    InputEvent* out,
    size_t max_out);
int ps2_mouse_ring_push(Ps2MouseRing* ring, const InputEvent* ev);
ssize_t ps2_mouse_ring_read(Ps2MouseRing* ring, InputEvent* out, size_t max_out);
