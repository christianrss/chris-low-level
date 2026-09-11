# Resolução guiada — ini_rd_lexer

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `PAR-INI-01` | `starter/ini.c` | `ini_lex_init` |
| `PAR-INI-02` | `starter/ini.c` | `ini_lex_next` (section) |
| `PAR-INI-03` | `starter/ini.c` | `ini_lex_next` (key) |

## Baseline

```powershell
cd days/2026-09-11/parsers/ini_rd_lexer/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.

## PAR-INI-01

### Onde colocar (PAR-INI-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ini.c` |
| Função | `ini_lex_init` |
| Substituir | o corpo sob o comentário `TODO [PAR-INI-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Cursor precisa apontar ao src.

### Algoritmo / trace

L->p = src || "".

### Escreva o código

```c
    L->p = src ? src : "";
    /* init */
    /* done */
```

### Por que funciona?

Sem init o next lê lixo.

### Verifique

base para os próximos TODOs.

### Código completo alinhado ao solutions/ (PAR-INI-01)

```c
PEDAGOGY-SOLUTION: PAR-INI-01 */
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
        /* 
```

## PAR-INI-02

### Onde colocar (PAR-INI-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ini.c` |
| Função | `ini_lex_next` |
| Substituir | o corpo sob o comentário `TODO [PAR-INI-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Primeiro token = section core.

### Algoritmo / trace

Se '[', leia até ']'.

### Escreva o código

```c
    size_t i = 0;
    skip_ws(L);
    if (*L->p == '[') {
        L->p++;
        while (*L->p && *L->p != ']' && i + 1 < sizeof out->text) out->text[i++] = *L->p++;
        out->text[i] = 0;
        if (*L->p == ']') L->p++;
        out->kind = TOK_SECTION;
        return TOK_SECTION;
    }
```

### Por que funciona?

Marcadores [ ] delimitam.

### Verifique

text=="core".

### Código completo alinhado ao solutions/ (PAR-INI-02)

```c
PEDAGOGY-SOLUTION: PAR-INI-02 */
        L->p++;
        while (*L->p && *L->p != ']' && i + 1 < sizeof out->text) out->text[i++] = *L->p++;
        out->text[i]=0;
        if (*L->p == ']') L->p++;
        out->kind = TOK_SECTION;
        return TOK_SECTION;
    }
    /* 
```

## PAR-INI-03

### Onde colocar (PAR-INI-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ini.c` |
| Função | `ini_lex_next` |
| Substituir | o corpo sob o comentário `TODO [PAR-INI-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Segundo token = key name.

### Algoritmo / trace

Leia até '=' para o nome; consuma resto da linha.

### Escreva o código

```c
    size_t i = 0;
    while (*L->p && *L->p != '=' && *L->p != '\n' && i + 1 < sizeof out->text) {
        if (!isspace((unsigned char)*L->p)) out->text[i++] = *L->p;
        L->p++;
    }
    out->text[i] = 0;
    if (*L->p == '=') { while (*L->p && *L->p != '\n') L->p++; }
    out->kind = TOK_KEY;
    return TOK_KEY;
```

### Por que funciona?

Lexer não precisa do value neste lab.

### Verifique

text=="name"; depois EOF.

### Código completo alinhado ao solutions/ (PAR-INI-03)

```c
PEDAGOGY-SOLUTION: PAR-INI-03 */
    while (*L->p && *L->p != '=' && *L->p != '\n' && i + 1 < sizeof out->text) {
        if (!isspace((unsigned char)*L->p)) out->text[i++] = *L->p;
        L->p++;
    }
    out->text[i]=0;
    if (*L->p == '=') { while (*L->p && *L->p != '\n') L->p++; }
    out->kind = TOK_KEY;
    return TOK_KEY;
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| key com = | pare no = |

## Relatório de resolução

- TODOs: [ ]
