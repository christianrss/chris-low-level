#include "trace.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* PEDAGOGY-TEST: CLVM-TRACE-01 */
/* PEDAGOGY-TEST: CLVM-TRACE-02 */
/* PEDAGOGY-TEST: CLVM-TRACE-03 */
int main(void) {
    uint32_t c[16];
    uint8_t code[] = {0x02, 0x02, 0x08};
    memset(c, 0, sizeof c);
    note_op(c, 0x02); note_op(c, 0x02); note_op(c, 0x08);
    assert(c[0x02] == 2 && c[0x08] == 1);
    assert(hottest(c) == 0x02);
    memset(c, 0, sizeof c);
    assert(profile_code(code, 3, c) == 3);
    assert(hottest(c) == 0x02);
    printf("OK trace\n");
    return 0;
}
