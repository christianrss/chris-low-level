// PEDAGOGY-SOLUTION: HID-KBD-DECODE-01
// PEDAGOGY-SOLUTION: HID-KBD-MAP-02
// PEDAGOGY-SOLUTION: HID-KBD-RING-03
// PEDAGOGY-SOLUTION: HID-KBD-READ-04
#include "hid_kbd.h"
#include <string.h>

static uint64_t g_time_us = 0;

void hid_kbd_set_time(uint64_t time_us) {
    g_time_us = time_us;
}

static uint16_t hid_usage_to_key(uint8_t usage) {
    switch (usage) {
        case 0x04:
            return KEY_A;
        case 0x05:
            return KEY_B;
        case 0x28:
            return KEY_ENTER;
        case 0x2C:
            return KEY_SPACE;
        default:
            return 0;
    }
}

void hid_boot_parse_report(const uint8_t raw[8], HidBootReport* out) {
    out->modifiers = raw[0];
    out->keys[0] = raw[2];
    out->keys[1] = raw[3];
    out->keys[2] = raw[4];
    out->keys[3] = raw[5];
    out->keys[4] = raw[6];
    out->keys[5] = raw[7];
}

static int key_in_report(uint8_t usage, const HidBootReport* report) {
    if (usage == 0) {
        return 0;
    }
    for (int i = 0; i < 6; ++i) {
        if (report->keys[i] == usage) {
            return 1;
        }
    }
    return 0;
}

ssize_t hid_kbd_map_events(
    const HidBootReport* cur,
    const HidBootReport* prev,
    InputEvent* out,
    size_t max_out) {
    size_t n = 0;
    static const struct {
        uint8_t mask;
        uint16_t key;
    } mod_map[] = {
        {0x01, KEY_LEFTCTRL},
        {0x02, KEY_LEFTSHIFT},
        {0x04, KEY_LEFTALT},
        {0x08, KEY_LEFTMETA},
    };

    for (size_t i = 0; i < 4 && n < max_out; ++i) {
        int cur_on = (cur->modifiers & mod_map[i].mask) != 0;
        int prev_on = (prev->modifiers & mod_map[i].mask) != 0;
        if (cur_on != prev_on) {
            out[n].time_us = g_time_us;
            out[n].type = EV_KEY;
            out[n].code = mod_map[i].key;
            out[n].value = cur_on ? 1 : 0;
            out[n].__pad = 0;
            ++n;
        }
    }

    for (uint8_t usage = 0x04; usage <= 0x2C && n < max_out; ++usage) {
        uint16_t key = hid_usage_to_key(usage);
        if (key == 0) {
            continue;
        }
        int cur_on = key_in_report(usage, cur);
        int prev_on = key_in_report(usage, prev);
        if (cur_on && !prev_on) {
            out[n].time_us = g_time_us;
            out[n].type = EV_KEY;
            out[n].code = key;
            out[n].value = 1;
            out[n].__pad = 0;
            ++n;
        } else if (!cur_on && prev_on) {
            out[n].time_us = g_time_us;
            out[n].type = EV_KEY;
            out[n].code = key;
            out[n].value = 0;
            out[n].__pad = 0;
            ++n;
        }
    }

    return (ssize_t)n;
}

int hid_kbd_ring_push(HidKbdRing* ring, const InputEvent* ev) {
    if (ring->count >= HID_KBD_RING_CAP) {
        return -1;
    }
    ring->buf[ring->tail] = *ev;
    ring->tail = (ring->tail + 1) % HID_KBD_RING_CAP;
    ++ring->count;
    return 0;
}

ssize_t hid_kbd_ring_read(HidKbdRing* ring, InputEvent* out, size_t max_out) {
    size_t n = 0;
    while (n < max_out && ring->count > 0) {
        out[n] = ring->buf[ring->head];
        ring->head = (ring->head + 1) % HID_KBD_RING_CAP;
        --ring->count;
        ++n;
    }
    return (ssize_t)n;
}
