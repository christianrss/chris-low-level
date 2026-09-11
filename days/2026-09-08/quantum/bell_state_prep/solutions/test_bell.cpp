#include "bell.hpp"
#include <assert.h>
#include <math.h>
#include <stdio.h>
// PEDAGOGY-TEST: Q-BELL-01
// PEDAGOGY-TEST: Q-BELL-02
// PEDAGOGY-TEST: Q-BELL-03
int main() {
    double a[4];
    q_reset(a);
    assert(fabs(a[0] - 1.0) < 1e-9);
    q_h0(a);
    assert(fabs(a[0] - 1.0 / sqrt(2.0)) < 1e-9);
    assert(fabs(a[2] - 1.0 / sqrt(2.0)) < 1e-9);
    q_cnot(a);
    assert(fabs(q_prob(a, 0) - 0.5) < 1e-9);
    assert(fabs(q_prob(a, 3) - 0.5) < 1e-9);
    assert(fabs(q_prob(a, 1)) < 1e-9);
    printf("OK bell\n");
    return 0;
}
