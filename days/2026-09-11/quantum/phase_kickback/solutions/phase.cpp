#include "phase.hpp"
#include <cmath>
void q_reset(double amp[4]) {
    /* PEDAGOGY-SOLUTION: Q-PHASE-01 */
    amp[0]=1; amp[1]=0; amp[2]=0; amp[3]=0;
}
void q_h0(double amp[4]) {
    /* PEDAGOGY-SOLUTION: Q-PHASE-02 */
    const double s = 1.0/std::sqrt(2.0);
    double a0=amp[0], a1=amp[1], a2=amp[2], a3=amp[3];
    amp[0]=s*(a0+a2); amp[1]=s*(a1+a3); amp[2]=s*(a0-a2); amp[3]=s*(a1-a3);
}
void q_cz(double amp[4]) {
    /* PEDAGOGY-SOLUTION: Q-PHASE-03 */
    amp[3] = -amp[3];
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
