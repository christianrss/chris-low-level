#include "json_lex.h"
int skip_ws(const char *s, int i) {
    /* PEDAGOGY-SOLUTION: PAR-JSON-LEX-01 */
    while (s[i] == ' ' || s[i] == '\n' || s[i] == '\t') i++;
    return i;
}
int next_token(const char *s, int i, JsonTok *out) {
    /* PEDAGOGY-SOLUTION: PAR-JSON-LEX-02 */
    if (!s || !out) return -1;
    i = skip_ws(s, i);
    out->start = i;
    if (s[i] == 0) { out->kind = TOK_END; out->end = i; return i; }
    if (s[i] == '{') { out->kind = TOK_LBRACE; out->end = i + 1; return i + 1; }
    if (s[i] == '}') { out->kind = TOK_RBRACE; out->end = i + 1; return i + 1; }
    if (s[i] == ',') { out->kind = TOK_COMMA; out->end = i + 1; return i + 1; }
    if (s[i] == ':') { out->kind = TOK_COLON; out->end = i + 1; return i + 1; }
    if (s[i] == '"') {
        int j = i + 1;
        while (s[j] && s[j] != '"') j++;
        if (s[j] != '"') return -1;
        out->kind = TOK_STRING; out->end = j + 1; return j + 1;
    }
    if (s[i] >= '0' && s[i] <= '9') {
        int j = i;
        while (s[j] >= '0' && s[j] <= '9') j++;
        out->kind = TOK_NUMBER; out->end = j; return j;
    }
    return -1;
}
int lex_count(const char *s) {
    /* PEDAGOGY-SOLUTION: PAR-JSON-LEX-03 */
    int i = 0, n = 0;
    if (!s) return -1;
    while (s[i]) {
        JsonTok t;
        int ni = next_token(s, i, &t);
        if (ni < 0 || t.kind == TOK_END) break;
        n++;
        i = ni;
    }
    return n;
}
