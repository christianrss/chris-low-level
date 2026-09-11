#pragma once
#include <cstddef>
struct Arena { char buf[64]; size_t used; int allocs; int resets; };
void arena_init(Arena *a);
int arena_alloc(Arena *a, size_t n, char **out);
void arena_reset(Arena *a);
