#include "trace.h"
void note_op(uint32_t *counts, uint8_t op) { /* TODO [CLVM-TRACE-01] */ (void)counts; (void)op; }
int hottest(const uint32_t *counts) { /* TODO [CLVM-TRACE-02] */ (void)counts; return -1; }
int profile_code(const uint8_t *code, size_t n, uint32_t *counts) {
    /* TODO [CLVM-TRACE-03] */ (void)code; (void)n; (void)counts; return -1;
}
