#include "softmax.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
/* PEDAGOGY-TEST: AI-SOFTMAX-01 */
/* PEDAGOGY-TEST: AI-SOFTMAX-02 */
/* PEDAGOGY-TEST: AI-SOFTMAX-03 */
int main(void) {
    float xs[3] = {1.f, 2.f, 3.f};
    float out[3];
    float sum = 0.f;
    int i;
    assert(softmax_stable(xs, 3, out) == 0);
    for (i = 0; i < 3; i++) sum += out[i];
    assert(fabsf(sum - 1.f) < 1e-5f);
    assert(out[2] > out[0]);
    assert(log_softmax_stable(xs, 3, out) == 0);
    assert(out[2] > out[0]);
    assert(fabsf(cross_entropy_loss(xs, 3, 2) - (-out[2])) < 1e-5f);
    printf("OK softmax\n");
    return 0;
}
