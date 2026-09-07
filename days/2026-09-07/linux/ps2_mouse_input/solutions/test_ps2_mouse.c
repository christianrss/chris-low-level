// PEDAGOGY-SOLUTION: PS2-MOUSE-DECODE-01
// PEDAGOGY-SOLUTION: PS2-MOUSE-EVENT-02
// PEDAGOGY-SOLUTION: PS2-MOUSE-RING-03
// PEDAGOGY-SOLUTION: PS2-MOUSE-READ-04
#include "ps2_mouse.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

#ifndef FIXTURES_DIR
#define FIXTURES_DIR "fixtures"
#endif

static int load_fixture(const char* name, uint8_t* buf, size_t len) {
    char path[512];
    snprintf(path, sizeof path, "%s/%s", FIXTURES_DIR, name);
    FILE* f = fopen(path, "rb");
    if (!f) {
        return -1;
    }
    size_t n = fread(buf, 1, len, f);
    fclose(f);
    return (n == len) ? 0 : -1;
}

static void push_mapped(Ps2MouseRing* ring, const Ps2MousePacket* cur, const Ps2MousePacket* prev) {
    InputEvent batch[8];
    ssize_t n = ps2_mouse_map_events(cur, prev, batch, 8);
    assert(n >= 0);
    for (ssize_t i = 0; i < n; ++i) {
        assert(ps2_mouse_ring_push(ring, &batch[i]) == 0);
    }
}

int main(void) {
    assert(sizeof(InputEvent) == 24);

    uint8_t move_raw[3] = {0};
    uint8_t left_raw[3] = {0};
    uint8_t up_raw[3] = {0};
    assert(load_fixture("move_right_up.raw", move_raw, 3) == 0);
    assert(load_fixture("left_down.raw", left_raw, 3) == 0);
    assert(load_fixture("buttons_up.raw", up_raw, 3) == 0);

    Ps2MousePacket zero = {0};
    Ps2MousePacket move = {0};
    ps2_mouse_set_time(2000);
    ps2_mouse_decode(move_raw, &move);
    assert(move.dx == 5);
    assert(move.dy == 3);
    assert(move.buttons == 0);

    InputEvent ev[4] = {0};
    ssize_t mapped = ps2_mouse_map_events(&move, &zero, ev, 4);
    assert(mapped == 2);
    assert(ev[0].type == EV_REL && ev[0].code == REL_X && ev[0].value == 5);
    assert(ev[1].type == EV_REL && ev[1].code == REL_Y && ev[1].value == 3);

    Ps2MousePacket left = {0};
    ps2_mouse_decode(left_raw, &left);
    mapped = ps2_mouse_map_events(&left, &move, ev, 4);
    assert(mapped == 1);
    assert(ev[0].type == EV_KEY && ev[0].code == BTN_LEFT && ev[0].value == 1);

    Ps2MouseRing ring = {0};
    push_mapped(&ring, &move, &zero);
    push_mapped(&ring, &left, &move);

    InputEvent out[8] = {0};
    ssize_t rd = ps2_mouse_ring_read(&ring, out, 8);
    assert(rd == 3);
    assert(out[0].code == REL_X);
    assert(out[1].code == REL_Y);
    assert(out[2].code == BTN_LEFT);

    Ps2MousePacket release = {0};
    ps2_mouse_decode(up_raw, &release);
    mapped = ps2_mouse_map_events(&release, &left, ev, 4);
    assert(mapped == 1);
    assert(ev[0].code == BTN_LEFT && ev[0].value == 0);

    InputEvent dummy = {0};
    for (int i = 0; i < PS2_MOUSE_RING_CAP; ++i) {
        assert(ps2_mouse_ring_push(&ring, &dummy) == 0);
    }
    assert(ps2_mouse_ring_push(&ring, &dummy) == -1);

    puts("OK ps2 mouse input");
    return 0;
}
