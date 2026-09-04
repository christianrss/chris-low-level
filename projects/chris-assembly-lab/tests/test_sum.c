#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

uint64_t asm_sum_u64(const uint64_t* values, size_t count);

int main(void) {
    const uint64_t values[] = {1, 2, 3, 5, 8, 13};
    assert(asm_sum_u64(values, 6) == 32);
    assert(asm_sum_u64(values, 0) == 0);
    const uint64_t max_pair[] = {UINT64_MAX, 1};
    assert(asm_sum_u64(max_pair, 2) == 0); /* intentional modulo-2^64 overflow */
    puts("assembly ABI tests passed");
    return 0;
}
