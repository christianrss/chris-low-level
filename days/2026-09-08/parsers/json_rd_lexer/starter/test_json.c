#include "json_lex.h"
#include <assert.h>
#include <stdio.h>
/* PEDAGOGY-TEST: PAR-JSON-LEX-01 */
/* PEDAGOGY-TEST: PAR-JSON-LEX-02 */
/* PEDAGOGY-TEST: PAR-JSON-LEX-03 */
int main(void) {
    JsonTok t;
    assert(skip_ws("  {", 0) == 2);
    assert(next_token("{", 0, &t) == 1 && t.kind == TOK_LBRACE);
    assert(next_token("42", 0, &t) == 2 && t.kind == TOK_NUMBER && t.end == 2);
    assert(next_token("\"ab\"", 0, &t) == 4 && t.kind == TOK_STRING);
    assert(lex_count("{\"a\":1}") == 5);
    printf("OK json lex\n");
    return 0;
}
