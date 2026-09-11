#include "uevent.h"
#include <stdio.h>
#include <string.h>
static int fail(const char *m) { fprintf(stderr, "FAIL %s\n", m); return 1; }
int main(void) {
    UeventKV one, table[8]; int n = 0;
    /* PEDAGOGY-TEST: LIN-UEVENT-01 */
    if (uevent_parse_line("ACTION=add", &one) != 0) return fail("line");
    if (strcmp(one.key, "ACTION") || strcmp(one.val, "add")) return fail("kv");
    if (uevent_parse_line("=x", &one) == 0) return fail("empty key");
    /* PEDAGOGY-TEST: LIN-UEVENT-02 */
    if (uevent_parse_block("ACTION=add\nDEVNAME=sda\n", table, 8, &n) != 0) return fail("block");
    if (n != 2) return fail("n=2");
    /* PEDAGOGY-TEST: LIN-UEVENT-03 */
    if (!uevent_get(table, n, "DEVNAME") || strcmp(uevent_get(table, n, "DEVNAME"), "sda")) return fail("get");
    if (uevent_get(table, n, "MISSING") != NULL) return fail("miss");
    puts("ok"); return 0;
}
