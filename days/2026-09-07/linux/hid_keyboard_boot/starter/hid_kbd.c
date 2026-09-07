// TODO [HID-KBD-DECODE-01] [HID-KBD-MAP-02] [HID-KBD-RING-03] [HID-KBD-READ-04]
#include "hid_kbd.h"
#include <string.h>

static uint64_t g_time_us = 0;

void hid_kbd_set_time(uint64_t time_us) {
    g_time_us = time_us;
}

void hid_boot_parse_report(const uint8_t raw[8], HidBootReport* out) {
    // TODO [HID-KBD-DECODE-01]
    memset(out, 0, sizeof(*out));
}

ssize_t hid_kbd_map_events(
    const HidBootReport* cur,
    const HidBootReport* prev,
    InputEvent* out,
    size_t max_out) {
    // TODO [HID-KBD-MAP-02]
    (void)cur;
    (void)prev;
    (void)out;
    (void)max_out;
    return -1;
}

int hid_kbd_ring_push(HidKbdRing* ring, const InputEvent* ev) {
    // TODO [HID-KBD-RING-03]
    (void)ring;
    (void)ev;
    return -1;
}

ssize_t hid_kbd_ring_read(HidKbdRing* ring, InputEvent* out, size_t max_out) {
    // TODO [HID-KBD-READ-04]
    (void)ring;
    (void)out;
    (void)max_out;
    return -1;
}
