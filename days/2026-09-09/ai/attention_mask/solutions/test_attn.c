#include "attn.h"
#include <assert.h>
#include <stdio.h>
/* PEDAGOGY-TEST: AI-ATTN-01 */
/* PEDAGOGY-TEST: AI-ATTN-02 */
/* PEDAGOGY-TEST: AI-ATTN-03 */
int main(void) {
    float s = 3.0f;
    assert(causal_mask(2, 2) == 1);
    assert(causal_mask(2, 3) == 0);
    assert(apply_mask(&s, 2, 3) == 0);
    assert(s < -1.0e8f);
    assert(visible_count(2) == 3);
    printf("OK attn\n");
    return 0;
}
