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

#define HID_KBD_RING_CAP 32

typedef struct {
    uint8_t modifiers;
    uint8_t keys[6];
} HidBootReport;

typedef struct {
    InputEvent buf[HID_KBD_RING_CAP];
    size_t head;
    size_t tail;
    size_t count;
} HidKbdRing;

void hid_kbd_set_time(uint64_t time_us);
void hid_boot_parse_report(const uint8_t raw[8], HidBootReport* out);
ssize_t hid_kbd_map_events(
    const HidBootReport* cur,
    const HidBootReport* prev,
    InputEvent* out,
    size_t max_out);
int hid_kbd_ring_push(HidKbdRing* ring, const InputEvent* ev);
ssize_t hid_kbd_ring_read(HidKbdRing* ring, InputEvent* out, size_t max_out);
