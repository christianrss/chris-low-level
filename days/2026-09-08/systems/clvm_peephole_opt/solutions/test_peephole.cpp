#include "peephole.hpp"
#include <assert.h>
#include <stdio.h>
// PEDAGOGY-TEST: CLVM-PEEP-01
// PEDAGOGY-TEST: CLVM-PEEP-02
// PEDAGOGY-TEST: CLVM-PEEP-03
int main() {
    uint8_t z[] = {0x01, 0,0,0,0, 0x02};
    uint8_t add[] = {0x01, 2,0,0,0, 0x01, 3,0,0,0, 0x02};
    uint8_t out[8];
    size_t n = 0;
    assert(match_push0_add(z, 6, 0) == 1);
    assert(fold_const_add(add, 11, 0, out, 8, &n) == 1);
    assert(n == 5 && out[0] == 0x01 && out[1] == 5);
    assert(saved_bytes(z, 6) == 6);
    printf("OK peephole\n");
    return 0;
}
