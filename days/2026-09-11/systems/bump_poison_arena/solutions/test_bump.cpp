#include "bump.hpp"
#include <cstdio>
static int fail(const char *m) { std::fprintf(stderr, "FAIL %s\n", m); return 1; }
int main() {
    BumpArena a{};
    /* PEDAGOGY-TEST: SYS-BUMP-01 */
    arena_reset(a);
    if (a.used != 0) return fail("used");
    for (std::size_t i = 0; i < ARENA_CAP; ++i) if (a.buf[i] != POISON) return fail("poison");
    /* PEDAGOGY-TEST: SYS-BUMP-02 */
    void *p = arena_alloc(a, 8);
    if (!p || a.used != 9 || a.buf[8] != CANARY) return fail("alloc8");
    if (arena_alloc(a, 56) != nullptr) return fail("full");
    /* PEDAGOGY-TEST: SYS-BUMP-03 */
    if (arena_check_canary(a, p, 8) != 0) return fail("canary ok");
    a.buf[8] = 0;
    if (arena_check_canary(a, p, 8) == 0) return fail("canary broken");
    std::puts("ok"); return 0;
}
