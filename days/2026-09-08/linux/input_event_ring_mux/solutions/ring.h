#ifndef RING_H
#define RING_H
#include <stdint.h>
#define RING_CAP 4
typedef struct { uint16_t type; int32_t value; uint8_t source; } InputEvent;
typedef struct { InputEvent slots[RING_CAP]; int head, tail, count; } EventRing;
int ring_push(EventRing *r, InputEvent ev);
int ring_pop(EventRing *r, InputEvent *out);
int mux_push(EventRing *r, uint8_t source, uint16_t type, int32_t value);
#endif
