#ifndef SOFTMAX_H
#define SOFTMAX_H
int softmax_stable(const float *xs, int n, float *out);
int log_softmax_stable(const float *xs, int n, float *out);
float cross_entropy_loss(const float *logits, int n, int target);
#endif
