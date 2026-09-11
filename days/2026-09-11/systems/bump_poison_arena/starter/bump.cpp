#include "bump.hpp"
#include <cstring>
void arena_reset(BumpArena &a) {
    /* TODO [SYS-BUMP-01]: used=0; fill buf with POISON */
    (void)a;
}
void *arena_alloc(BumpArena &a, std::size_t n) {
    /* TODO [SYS-BUMP-02]: bump n+1 bytes; last byte CANARY; NULL if full */
    (void)a; (void)n; return nullptr;
}
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n) {
    /* TODO [SYS-BUMP-03]: return 0 if byte after n is CANARY else -1 */
    (void)a; (void)p; (void)n; return -1;
}
