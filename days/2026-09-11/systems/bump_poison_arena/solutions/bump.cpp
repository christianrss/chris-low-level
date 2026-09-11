#include "bump.hpp"
#include <cstring>
void arena_reset(BumpArena &a) {
    /* PEDAGOGY-SOLUTION: SYS-BUMP-01 */
    a.used = 0; std::memset(a.buf, POISON, ARENA_CAP);
}
void *arena_alloc(BumpArena &a, std::size_t n) {
    /* PEDAGOGY-SOLUTION: SYS-BUMP-02 */
    if (n == 0 || a.used + n + 1 > ARENA_CAP) return nullptr;
    void *p = a.buf + a.used; a.used += n + 1; a.buf[a.used - 1] = CANARY; return p;
}
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n) {
    /* PEDAGOGY-SOLUTION: SYS-BUMP-03 */
    if (!p || n == 0) return -1;
    const auto *b = static_cast<const std::uint8_t *>(p);
    if (b < a.buf || b + n >= a.buf + ARENA_CAP) return -1;
    return b[n] == CANARY ? 0 : -1;
}
