#include "arena.hpp"
#include <assert.h>
#include <stdio.h>
// PEDAGOGY-TEST: ARENA-TEL-01
// PEDAGOGY-TEST: ARENA-TEL-02
// PEDAGOGY-TEST: ARENA-TEL-03
int main() {
    Arena a; char *p = 0;
    arena_init(&a);
    assert(a.used == 0 && a.allocs == 0);
    assert(arena_alloc(&a, 8, &p) == 0 && a.allocs == 1 && a.used == 8);
    assert(arena_alloc(&a, 60, &p) == -1);
    arena_reset(&a);
    assert(a.used == 0 && a.resets == 1 && a.allocs == 1);
    printf("OK arena\n");
    return 0;
}
