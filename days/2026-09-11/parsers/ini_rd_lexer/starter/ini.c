#include "ini.h"
#include <ctype.h>
#include <string.h>
void ini_lex_init(IniLex *L, const char *src) {
    /* TODO [PAR-INI-01]: set cursor */
    (void)L; (void)src;
}
static void skip_ws(IniLex *L) {
    while (*L->p && (*L->p==' '||*L->p=='\t'||*L->p=='\r'||*L->p=='\n')) L->p++;
}
IniTok ini_lex_next(IniLex *L, IniToken *out) {
    /* TODO [PAR-INI-02]: [section] → TOK_SECTION */
    /* TODO [PAR-INI-03]: key=value → TOK_KEY with text "key" (value ignored in lexer) */
    (void)L; (void)out; return TOK_ERR;
}
