#pragma once
#include <cstddef>
#include <cstdint>
int match_push0_add(const uint8_t *code, size_t len, size_t pc);
int fold_const_add(const uint8_t *code, size_t len, size_t pc, uint8_t *out, size_t out_cap, size_t *out_len);
int saved_bytes(const uint8_t *code, size_t len);
