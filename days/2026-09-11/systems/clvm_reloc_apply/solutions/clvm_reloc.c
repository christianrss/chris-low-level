#include "clvm_reloc.h"

int reloc_read_u16(const uint8_t *code, size_t len, size_t at, uint16_t *out) {
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-01 */
    if (!code || !out || at + 2 > len) return -1;
    *out = (uint16_t)code[at] | ((uint16_t)code[at + 1] << 8);
    return 0;
}

int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta) {
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-02 */
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-04 */
    uint16_t cur;
    uint16_t next;
    if (reloc_read_u16(code, len, at, &cur) != 0) return -1;
    next = (uint16_t)(cur + (uint16_t)delta);
    code[at] = (uint8_t)(next & 0xFF);
    code[at + 1] = (uint8_t)((next >> 8) & 0xFF);
    return 0;
}

int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta) {
    /* PEDAGOGY-SOLUTION: CLVM-RELOC-03 */
    size_t i;
    if (!code || (!sites && n > 0)) return -1;
    for (i = 0; i < n; ++i) {
        if (reloc_apply_one(code, len, sites[i], delta) != 0) return -1;
    }
    return 0;
}
