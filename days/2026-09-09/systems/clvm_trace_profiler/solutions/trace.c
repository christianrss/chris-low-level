#include "trace.h"
void note_op(uint32_t *counts, uint8_t op) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-01 */
    if (counts && op < 16) counts[op]++;
}
int hottest(const uint32_t *counts) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-02 */
    int best = 0, i;
    if (!counts) return -1;
    for (i = 1; i < 16; i++) if (counts[i] > counts[best]) best = i;
    return best;
}
int profile_code(const uint8_t *code, size_t n, uint32_t *counts) {
    /* PEDAGOGY-SOLUTION: CLVM-TRACE-03 */
    size_t i;
    if (!code || !counts) return -1;
    for (i = 0; i < n; i++) note_op(counts, code[i]);
    return (int)n;
}
