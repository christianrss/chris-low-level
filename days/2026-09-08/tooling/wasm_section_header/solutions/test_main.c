#include "api.h"
#include <assert.h>
#include <stdio.h>
/* PEDAGOGY-TEST: TOOL-WASM-01 */
/* PEDAGOGY-TEST: TOOL-WASM-02 */
/* PEDAGOGY-TEST: TOOL-WASM-03 */
int main(void) {
    unsigned char ok[] = {0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00};
    unsigned char bad[] = {0x00, 0x61, 0x73, 0x00, 0x01, 0x00, 0x00, 0x00};
    assert(wasm_magic_ok(ok) == 1);
    assert(wasm_magic_ok(bad) == 0);
    assert(wasm_version_is_1(ok) == 1);
    assert(section_class(1) == 1);
    assert(section_class(2) == 2);
    assert(section_class(9) == 0);
    printf("OK wasm asm\n");
    return 0;
}
