#include "api.h"
#include <stdio.h>
#include <string.h>
static int fail(const char *m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    unsigned char shortn[8] = {'m','a','i','n',0,0,0,0};
    unsigned char longn[8] = {0,0,0,0, 0x10,0,0,0};
    /* PEDAGOGY-TEST: TOOL-COFF-01 */
    if (coff_name_is_long(longn) != 1) return fail("long");
    if (coff_name_is_long(shortn) != 0) return fail("not long");
    /* PEDAGOGY-TEST: TOOL-COFF-02 */
    if (coff_name_is_short(shortn) != 1) return fail("short");
    if (coff_name_is_short(longn) != 0) return fail("not short");
    /* PEDAGOGY-TEST: TOOL-COFF-03 */
    if (coff_short_name_len(shortn) != 4) return fail("len4");
    puts("ok"); return 0;
}
