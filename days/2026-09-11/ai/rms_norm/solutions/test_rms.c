#include "rms.h"
#include <math.h>
#include <stdio.h>
static int fail(const char *m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    float x[2]={3.f,4.f}; float out[2]; float g[2]={2.f,2.f};
    /* PEDAGOGY-TEST: AI-RMS-01 */
    /* mean sq = (9+16)/2=12.5; rms=sqrt(12.5)=√(25/2)=5/√2≈3.535533 */
    {
        float r = rms_of(x,2,0.f);
        if (fabsf(r - sqrtf(12.5f)) > 1e-5f) return fail("rms");
    }
    /* PEDAGOGY-TEST: AI-RMS-02 */
    if (rms_norm(x,2,0.f,out)!=0) return fail("norm");
    if (fabsf(out[0]-3.f/sqrtf(12.5f))>1e-5f) return fail("o0");
    if (fabsf(out[1]-4.f/sqrtf(12.5f))>1e-5f) return fail("o1");
    /* PEDAGOGY-TEST: AI-RMS-03 */
    if (rms_norm_g(x,g,2,0.f,out)!=0) return fail("g");
    if (fabsf(out[0]-2.f*3.f/sqrtf(12.5f))>1e-5f) return fail("g0");
    puts("ok"); return 0;
}
