#ifndef RMS_H
#define RMS_H
int rms_norm(const float *x, int n, float eps, float *out);
float rms_of(const float *x, int n, float eps);
int rms_norm_g(const float *x, const float *g, int n, float eps, float *out);
#endif
