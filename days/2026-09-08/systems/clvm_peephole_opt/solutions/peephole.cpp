#include "peephole.hpp"
static uint32_t rd_u32(const uint8_t *p) {
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}
int match_push0_add(const uint8_t *code, size_t len, size_t pc) {
    // PEDAGOGY-SOLUTION: CLVM-PEEP-01
    if (!code || pc + 6 > len) return 0;
    if (code[pc] != 0x01 || code[pc + 5] != 0x02) return 0;
    return rd_u32(code + pc + 1) == 0 ? 1 : 0;
}
int fold_const_add(const uint8_t *code, size_t len, size_t pc, uint8_t *out, size_t out_cap, size_t *out_len) {
    // PEDAGOGY-SOLUTION: CLVM-PEEP-02
    uint32_t a, b, s;
    if (!code || !out || !out_len || pc + 11 > len || out_cap < 5) return 0;
    if (code[pc] != 0x01 || code[pc + 5] != 0x01 || code[pc + 10] != 0x02) return 0;
    a = rd_u32(code + pc + 1);
    b = rd_u32(code + pc + 6);
    s = a + b;
    out[0] = 0x01;
    out[1] = (uint8_t)(s & 0xFF);
    out[2] = (uint8_t)((s >> 8) & 0xFF);
    out[3] = (uint8_t)((s >> 16) & 0xFF);
    out[4] = (uint8_t)((s >> 24) & 0xFF);
    *out_len = 5;
    return 1;
}
int saved_bytes(const uint8_t *code, size_t len) {
    // PEDAGOGY-SOLUTION: CLVM-PEEP-03
    size_t i = 0;
    int saved = 0;
    while (i + 6 <= len) {
        if (match_push0_add(code, len, i)) { saved += 6; i += 6; continue; }
        if (i + 11 <= len && code[i] == 0x01 && code[i + 5] == 0x01 && code[i + 10] == 0x02) {
            saved += 6; i += 11; continue;
        }
        i++;
    }
    return saved;
}
