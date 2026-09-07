#pragma once
#include <stdint.h>

/* Simplified Linux evdev input_event (24 bytes on x86_64). */
#define EV_SYN 0x00
#define EV_KEY 0x01
#define EV_REL 0x02

#define KEY_A 30
#define KEY_B 48
#define KEY_ENTER 28
#define KEY_SPACE 57
#define KEY_LEFTCTRL 29
#define KEY_LEFTSHIFT 42
#define KEY_LEFTALT 56
#define KEY_LEFTMETA 125

#define REL_X 0x00
#define REL_Y 0x01

#define BTN_LEFT 0x110
#define BTN_RIGHT 0x111
#define BTN_MIDDLE 0x112

typedef struct {
    uint64_t time_us;
    uint16_t type;
    uint16_t code;
    int32_t value;
    uint64_t __pad;
} InputEvent;

#if defined(__STDC_VERSION__) && __STDC_VERSION__ >= 201112L
_Static_assert(sizeof(InputEvent) == 24, "InputEvent must be 24 bytes");
#endif
