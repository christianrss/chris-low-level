#include "clvm_reloc.h"
#include <stdio.h>
#include <string.h>

static int fail(const char *m) { fprintf(stderr, "FAIL %s\n", m); return 1; }

int main(void) {
    /* PEDAGOGY-TEST: CLVM-RELOC-01 */
    {
        uint8_t buf[] = {0x0A, 0x00, 0xFF};
        uint16_t v = 0;
        if (reloc_read_u16(buf, 3, 0, &v) != 0 || v != 10) return fail("read 10");
        if (reloc_read_u16(buf, 3, 2, &v) == 0) return fail("OOB must fail");
    }
    /* PEDAGOGY-TEST: CLVM-RELOC-02 */
    {
        uint8_t buf[] = {0x09, 0x0A, 0x00, 0x08};
        if (reloc_apply_one(buf, 4, 1, 5) != 0) return fail("apply");
        if (buf[1] != 0x0F || buf[2] != 0x00) return fail("JMP offset 10+5=15");
    }
    /* PEDAGOGY-TEST: CLVM-RELOC-03 */
    {
        uint8_t buf[] = {0x09, 0x02, 0x00, 0x09, 0x04, 0x00};
        size_t sites[] = {1, 4};
        if (reloc_apply_all(buf, 6, sites, 2, 3) != 0) return fail("all");
        if (buf[1] != 5 || buf[4] != 7) return fail("sites 2+3=5 and 4+3=7");
    }
    /* PEDAGOGY-TEST: CLVM-RELOC-04 */
    {
        uint8_t buf[] = {0xFF, 0xFF};
        if (reloc_apply_one(buf, 2, 0, 1) != 0) return fail("wrap");
        if (buf[0] != 0 || buf[1] != 0) return fail("0xFFFF+1 wraps to 0");
    }
    puts("ok");
    return 0;
}
