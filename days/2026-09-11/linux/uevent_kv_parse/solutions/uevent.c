#include "uevent.h"
#include <string.h>
int uevent_parse_line(const char *line, UeventKV *out) {
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-01 */
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
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-02 */
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
    /* PEDAGOGY-SOLUTION: LIN-UEVENT-03 */
    int i;
    if (!table || !key) return NULL;
    for (i = 0; i < n; i++) if (strcmp(table[i].key, key) == 0) return table[i].val;
    return NULL;
}
