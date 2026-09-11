#include "ini.h"
#include <ctype.h>
#include <string.h>
void ini_lex_init(IniLex *L, const char *src) {
    /* PEDAGOGY-SOLUTION: PAR-INI-01 */
    L->p = src ? src : "";
}
static void skip_ws(IniLex *L) {
    while (*L->p && (*L->p==' '||*L->p=='\t'||*L->p=='\r'||*L->p=='\n')) L->p++;
}
IniTok ini_lex_next(IniLex *L, IniToken *out) {
    size_t i = 0;
    if (!L || !out) return TOK_ERR;
    skip_ws(L);
    if (!*L->p) { out->kind = TOK_EOF; out->text[0]=0; return TOK_EOF; }
    if (*L->p == '[') {
        /* PEDAGOGY-SOLUTION: PAR-INI-02 */
        L->p++;
        while (*L->p && *L->p != ']' && i + 1 < sizeof out->text) out->text[i++] = *L->p++;
        out->text[i]=0;
        if (*L->p == ']') L->p++;
        out->kind = TOK_SECTION;
        return TOK_SECTION;
    }
    /* PEDAGOGY-SOLUTION: PAR-INI-03 */
    while (*L->p && *L->p != '=' && *L->p != '\n' && i + 1 < sizeof out->text) {
        if (!isspace((unsigned char)*L->p)) out->text[i++] = *L->p;
        L->p++;
    }
    out->text[i]=0;
    if (*L->p == '=') { while (*L->p && *L->p != '\n') L->p++; }
    out->kind = TOK_KEY;
    return TOK_KEY;
}
