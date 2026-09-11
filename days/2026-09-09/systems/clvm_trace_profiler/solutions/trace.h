#ifndef TRACE_H
#define TRACE_H
#include <stddef.h>
#include <stdint.h>
void note_op(uint32_t *counts, uint8_t op);
int hottest(const uint32_t *counts);
int profile_code(const uint8_t *code, size_t n, uint32_t *counts);
#endif
