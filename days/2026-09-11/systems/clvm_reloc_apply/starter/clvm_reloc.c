#include "clvm_reloc.h"

int reloc_read_u16(const uint8_t *code, size_t len, size_t at, uint16_t *out) {
    /* TODO [CLVM-RELOC-01]: read u16 LE at `at`; return -1 if OOB */
    (void)code; (void)len; (void)at; (void)out;
    return -1;
}

int reloc_apply_one(uint8_t *code, size_t len, size_t at, int16_t delta) {
    /* TODO [CLVM-RELOC-02]: add delta to u16 LE at `at` with wrap; -1 if OOB */
    /* TODO [CLVM-RELOC-04]: wrap 0xFFFF+1 → 0 via uint16 arithmetic */
    (void)code; (void)len; (void)at; (void)delta;
    return -1;
}

int reloc_apply_all(uint8_t *code, size_t len, const size_t *sites, size_t n, int16_t delta) {
    /* TODO [CLVM-RELOC-03]: apply delta at every site; stop on first error */
    (void)code; (void)len; (void)sites; (void)n; (void)delta;
    return -1;
}
