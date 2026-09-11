#include "bell.hpp"
#include <math.h>
void q_reset(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-01
    amp[0] = 1.0; amp[1] = 0.0; amp[2] = 0.0; amp[3] = 0.0;
}
void q_h0(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-02
    const double s = 1.0 / sqrt(2.0);
    double a0 = amp[0], a1 = amp[1], a2 = amp[2], a3 = amp[3];
    amp[0] = s * (a0 + a2);
    amp[1] = s * (a1 + a3);
    amp[2] = s * (a0 - a2);
    amp[3] = s * (a1 - a3);
}
void q_cnot(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-03
    double a2 = amp[2], a3 = amp[3];
    amp[2] = a3;
    amp[3] = a2;
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
