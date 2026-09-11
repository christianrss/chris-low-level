#include "rms.h"
#include <math.h>
float rms_of(const float *x, int n, float eps) {
    /* TODO [AI-RMS-01]: sqrt(mean(x^2)+eps) */
    (void)x;(void)n;(void)eps; return -1.f;
}
int rms_norm(const float *x, int n, float eps, float *out) {
    /* TODO [AI-RMS-02]: out = x / rms */
    (void)x;(void)n;(void)eps;(void)out; return -1;
}
int rms_norm_g(const float *x, const float *g, int n, float eps, float *out) {
    /* TODO [AI-RMS-03]: out = g * (x / rms) */
    (void)x;(void)g;(void)n;(void)eps;(void)out; return -1;
}
