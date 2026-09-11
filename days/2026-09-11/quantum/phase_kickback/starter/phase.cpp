#include "phase.hpp"
#include <cmath>
void q_reset(double amp[4]) {
    /* TODO [Q-PHASE-01]: |00> */
    (void)amp;
}
void q_h0(double amp[4]) {
    /* TODO [Q-PHASE-02]: Hadamard on qubit 0 */
    (void)amp;
}
void q_cz(double amp[4]) {
    /* TODO [Q-PHASE-03]: phase kickback CZ: amp[3] *= -1 */
    (void)amp;
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
