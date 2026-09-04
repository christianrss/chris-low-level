#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>

uint64_t asm_sum_u64(const uint64_t* values, size_t count);

static uint64_t c_sum_u64(const uint64_t* values, size_t count) {
    uint64_t sum = 0;
    for (size_t i = 0; i < count; ++i) sum += values[i];
    return sum;
}

static double seconds_since(clock_t start, clock_t end) {
    return (double)(end - start) / (double)CLOCKS_PER_SEC;
}

int main(void) {
    enum { N = 4096, R = 20000 };
    static uint64_t values[N];
    for (size_t i = 0; i < N; ++i) values[i] = (uint64_t)i;
    volatile uint64_t sink = 0;
    clock_t a = clock();
    for (int i = 0; i < R; ++i) sink ^= c_sum_u64(values, N);
    clock_t b = clock();
    for (int i = 0; i < R; ++i) sink ^= asm_sum_u64(values, N);
    clock_t c = clock();
    printf("c_seconds=%.6f asm_seconds=%.6f sink=%llu\n",
           seconds_since(a, b), seconds_since(b, c), (unsigned long long)sink);
    return 0;
}
