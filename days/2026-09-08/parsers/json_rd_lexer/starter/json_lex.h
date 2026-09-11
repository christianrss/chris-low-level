#ifndef JSON_LEX_H
#define JSON_LEX_H
enum { TOK_END = 0, TOK_LBRACE = 1, TOK_RBRACE = 2, TOK_NUMBER = 3, TOK_STRING = 4, TOK_COMMA = 5, TOK_COLON = 6 };
typedef struct { int kind; int start; int end; } JsonTok;
int skip_ws(const char *s, int i);
int next_token(const char *s, int i, JsonTok *out);
int lex_count(const char *s);
#endif
