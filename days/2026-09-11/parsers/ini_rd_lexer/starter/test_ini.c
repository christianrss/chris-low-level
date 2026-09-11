#include "ini.h"
#include <stdio.h>
#include <string.h>
static int fail(const char *m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    IniLex L; IniToken t;
    /* PEDAGOGY-TEST: PAR-INI-01 */
    ini_lex_init(&L, "[core]\nname=demo\n");
    /* PEDAGOGY-TEST: PAR-INI-02 */
    if (ini_lex_next(&L,&t) != TOK_SECTION || strcmp(t.text,"core")) return fail("sec");
    /* PEDAGOGY-TEST: PAR-INI-03 */
    if (ini_lex_next(&L,&t) != TOK_KEY || strcmp(t.text,"name")) return fail("key");
    if (ini_lex_next(&L,&t) != TOK_EOF) return fail("eof");
    puts("ok"); return 0;
}
