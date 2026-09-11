#ifndef ATTN_H
#define ATTN_H
int causal_mask(int q, int k);
int apply_mask(float *score, int q, int k);
int visible_count(int q);
#endif
