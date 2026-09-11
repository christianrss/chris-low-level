#include "rms.h"
#include <math.h>
float rms_of(const float *x, int n, float eps) {
    /* PEDAGOGY-SOLUTION: AI-RMS-01 */
    float s = 0.f; int i;
    if (!x || n <= 0) return -1.f;
    for (i = 0; i < n; i++) s += x[i] * x[i];
    return sqrtf(s / (float)n + eps);
}
int rms_norm(const float *x, int n, float eps, float *out) {
    /* PEDAGOGY-SOLUTION: AI-RMS-02 */
    float r; int i;
    if (!x || !out || n <= 0) return -1;
    r = rms_of(x, n, eps);
    if (r <= 0.f) return -1;
    for (i = 0; i < n; i++) out[i] = x[i] / r;
    return 0;
}
int rms_norm_g(const float *x, const float *g, int n, float eps, float *out) {
    /* PEDAGOGY-SOLUTION: AI-RMS-03 */
    int i;
    if (!g || rms_norm(x, n, eps, out) != 0) return -1;
    for (i = 0; i < n; i++) out[i] *= g[i];
    return 0;
}
