#ifndef CLVM_RELOC_H
#define CLVM_RELOC_H
#include <stddef.h>
#include <stdint.h>
int reloc_read_u16(const uint8_t *code, size_t len, size_t at, uint16_t *out);
int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta);
int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta);
#endif
