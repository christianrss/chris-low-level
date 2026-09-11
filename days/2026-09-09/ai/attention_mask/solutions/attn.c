#include "attn.h"
int causal_mask(int q, int k) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-01 */
    if (q < 0 || k < 0) return 0;
    return k <= q ? 1 : 0;
}
int apply_mask(float *score, int q, int k) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-02 */
    if (!score) return 0;
    if (!causal_mask(q, k)) { *score = -1.0e9f; return 0; }
    return 1;
}
int visible_count(int q) {
    /* PEDAGOGY-SOLUTION: AI-ATTN-03 */
    if (q < 0) return 0;
    return q + 1;
}
