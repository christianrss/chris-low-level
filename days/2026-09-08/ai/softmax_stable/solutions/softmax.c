#include "softmax.h"
#include <math.h>
static float vmax(const float *xs, int n) {
    float m = xs[0];
    int i;
    for (i = 1; i < n; i++) if (xs[i] > m) m = xs[i];
    return m;
}
int softmax_stable(const float *xs, int n, float *out) {
    /* PEDAGOGY-SOLUTION: AI-SOFTMAX-01 */
    float m, sum = 0.f;
    int i;
    if (!xs || !out || n <= 0) return -1;
    m = vmax(xs, n);
    for (i = 0; i < n; i++) { out[i] = expf(xs[i] - m); sum += out[i]; }
    for (i = 0; i < n; i++) out[i] /= sum;
    return 0;
}
int log_softmax_stable(const float *xs, int n, float *out) {
    /* PEDAGOGY-SOLUTION: AI-SOFTMAX-02 */
    float m, sum = 0.f;
    int i;
    if (!xs || !out || n <= 0) return -1;
    m = vmax(xs, n);
    for (i = 0; i < n; i++) sum += expf(xs[i] - m);
    for (i = 0; i < n; i++) out[i] = (xs[i] - m) - logf(sum);
    return 0;
}
float cross_entropy_loss(const float *logits, int n, int target) {
    /* PEDAGOGY-SOLUTION: AI-SOFTMAX-03 */
    float logs[8];
    if (!logits || target < 0 || target >= n || n > 8) return -1.f;
    if (log_softmax_stable(logits, n, logs) != 0) return -1.f;
    return -logs[target];
}
