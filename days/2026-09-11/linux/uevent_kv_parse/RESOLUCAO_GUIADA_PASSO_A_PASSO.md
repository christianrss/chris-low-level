# Resolução guiada — uevent_kv_parse

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `LIN-UEVENT-01` | `starter/uevent.c` | `uevent_parse_line` |
| `LIN-UEVENT-02` | `starter/uevent.c` | `uevent_parse_block` |
| `LIN-UEVENT-03` | `starter/uevent.c` | `uevent_get` |

## Baseline

```powershell
cd days/2026-09-11/linux/uevent_kv_parse/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.

## LIN-UEVENT-01

### Onde colocar (LIN-UEVENT-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/uevent.c` |
| Função | `uevent_parse_line` |
| Substituir | o corpo sob o comentário `TODO [LIN-UEVENT-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Stub retorna -1; precisa KEY=value.

### Algoritmo / trace

strchr '='; copie key/val com bounds.

### Escreva o código

```c
    const char *eq; size_t klen, vlen;
    if (!line || !out) return -1;
    eq = strchr(line, '=');
    if (!eq || eq == line) return -1;
    klen = (size_t)(eq - line); vlen = strlen(eq + 1);
    if (klen >= UEVENT_KEY || vlen >= UEVENT_VAL) return -1;
    memcpy(out->key, line, klen); out->key[klen] = 0;
    memcpy(out->val, eq + 1, vlen + 1);
    return 0;
```

### Por que funciona?

eq==line significa chave vazia.

### Verifique

ACTION/add; rejeita =x.

### Código completo alinhado ao solutions/ (LIN-UEVENT-01)

```c
PEDAGOGY-SOLUTION: LIN-UEVENT-01 */
    const char *eq; size_t klen, vlen;
    if (!line || !out) return -1;
    eq = strchr(line, '=');
    if (!eq || eq == line) return -1;
    klen = (size_t)(eq - line); vlen = strlen(eq + 1);
    if (klen >= UEVENT_KEY || vlen >= UEVENT_VAL) return -1;
    memcpy(out->key, line, klen); out->key[klen] = 0;
    memcpy(out->val, eq + 1, vlen + 1);
    return 0;
}
int uevent_parse_block(const char *block, UeventKV *table, int cap, int *out_n) {
    /* 
```

## LIN-UEVENT-02

### Onde colocar (LIN-UEVENT-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/uevent.c` |
| Função | `uevent_parse_block` |
| Substituir | o corpo sob o comentário `TODO [LIN-UEVENT-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Duas linhas devem virar n=2.

### Algoritmo / trace

Quebre por \n; parse cada linha não vazia.

### Escreva o código

```c
    int n = 0;
    /* walk lines into buf; parse_line into table[n++] */
    *out_n = n;
    return 0;
```

### Por que funciona?

Linhas vazias são ignoradas; erro em qualquer linha aborta.

### Verifique

n==2 para o bloco do teste.

### Código completo alinhado ao solutions/ (LIN-UEVENT-02)

```c
PEDAGOGY-SOLUTION: LIN-UEVENT-02 */
    char buf[256]; const char *p; int n = 0;
    if (!block || !table || !out_n || cap <= 0) return -1;
    p = block;
    while (*p && n < cap) {
        size_t i = 0;
        while (p[i] && p[i] != '\n' && i + 1 < sizeof buf) { buf[i] = p[i]; i++; }
        buf[i] = 0;
        if (i > 0) {
            if (uevent_parse_line(buf, &table[n]) != 0) return -1;
            n++;
        }
        p += i; if (*p == '\n') p++;
    }
    *out_n = n; return 0;
}
const char *uevent_get(const UeventKV *table, int n, const char *key) {
    /* 
```

## LIN-UEVENT-03

### Onde colocar (LIN-UEVENT-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/uevent.c` |
| Função | `uevent_get` |
| Substituir | o corpo sob o comentário `TODO [LIN-UEVENT-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Lookup linear da chave.

### Algoritmo / trace

strcmp key; retorne val ou NULL.

### Escreva o código

```c
    int i;
    for (i = 0; i < n; i++)
        if (strcmp(table[i].key, key) == 0) return table[i].val;
    return NULL;
```

### Por que funciona?

Contrato simples sem hash.

### Verifique

DEVNAME→sda; MISSING→NULL.

### Código completo alinhado ao solutions/ (LIN-UEVENT-03)

```c
PEDAGOGY-SOLUTION: LIN-UEVENT-03 */
    int i;
    if (!table || !key) return NULL;
    for (i = 0; i < n; i++) if (strcmp(table[i].key, key) == 0) return table[i].val;
    return NULL;
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| aceita =x | eq==line → -1 |
| n=1 | avance após \n |

## Relatório de resolução

- TODOs: [ ]
