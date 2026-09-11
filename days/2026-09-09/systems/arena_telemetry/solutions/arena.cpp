#include "arena.hpp"
void arena_init(Arena *a) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-01
    a->used = 0; a->allocs = 0; a->resets = 0;
}
int arena_alloc(Arena *a, size_t n, char **out) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-02
    if (!a || !out || a->used + n > 64) return -1;
    *out = a->buf + a->used;
    a->used += n;
    a->allocs++;
    return 0;
}
void arena_reset(Arena *a) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-03
    if (!a) return;
    a->used = 0;
    a->resets++;
}
