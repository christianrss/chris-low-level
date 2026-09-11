#include "uevent.h"
#include <string.h>
int uevent_parse_line(const char *line, UeventKV *out) {
    /* TODO [LIN-UEVENT-01]: split KEY=value; reject empty key or missing '=' */
    (void)line; (void)out; return -1;
}
int uevent_parse_block(const char *block, UeventKV *table, int cap, int *out_n) {
    /* TODO [LIN-UEVENT-02]: parse newline-separated lines into table */
    (void)block; (void)table; (void)cap; (void)out_n; return -1;
}
const char *uevent_get(const UeventKV *table, int n, const char *key) {
    /* TODO [LIN-UEVENT-03]: linear search; NULL if missing */
    (void)table; (void)n; (void)key; return NULL;
}
