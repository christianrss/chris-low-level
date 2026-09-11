#ifndef INI_H
#define INI_H
typedef enum { TOK_SECTION, TOK_KEY, TOK_EOF, TOK_ERR } IniTok;
typedef struct { IniTok kind; char text[64]; } IniToken;
typedef struct { const char *p; } IniLex;
void ini_lex_init(IniLex *L, const char *src);
IniTok ini_lex_next(IniLex *L, IniToken *out);
#endif
