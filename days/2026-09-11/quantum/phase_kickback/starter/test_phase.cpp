#include "phase.hpp"
#include <cmath>
#include <cstdio>
static int fail(const char *m){std::fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(){
    double amp[4];
    /* PEDAGOGY-TEST: Q-PHASE-01 */
    q_reset(amp);
    if (std::fabs(amp[0]-1.0)>1e-9) return fail("reset");
    /* PEDAGOGY-TEST: Q-PHASE-02 */
    q_h0(amp);
    if (std::fabs(q_prob(amp,0)-0.5)>1e-9) return fail("H p00");
    if (std::fabs(q_prob(amp,2)-0.5)>1e-9) return fail("H p10");
    /* PEDAGOGY-TEST: Q-PHASE-03 */
    /* prepare |+1> roughly: reset, flip to put amp on |01> then H — simpler: set amp manually path */
    q_reset(amp); amp[0]=0; amp[3]=1; /* |11> */
    q_cz(amp);
    if (amp[3] > 0) return fail("phase flip sign");
    q_reset(amp); q_h0(amp);
    /* put target in |1>: apply X on q1 via swap amp[0]<->amp[1], amp[2]<->amp[3] */
    { double t=amp[0]; amp[0]=amp[1]; amp[1]=t; t=amp[2]; amp[2]=amp[3]; amp[3]=t; }
    q_cz(amp);
    /* phase kickback: relative phase on control — amp[1] and amp[3] should differ in sign pattern */
    if (!(amp[1] * amp[3] < 0)) return fail("kickback relative");
    std::puts("ok"); return 0;
}
