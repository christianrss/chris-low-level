#include "peephole.hpp"
int match_push0_add(const uint8_t *code, size_t len, size_t pc) {
    // TODO [CLVM-PEEP-01]
    (void)code; (void)len; (void)pc; return 0;
}
int fold_const_add(const uint8_t *code, size_t len, size_t pc, uint8_t *out, size_t out_cap, size_t *out_len) {
    // TODO [CLVM-PEEP-02]
    (void)code; (void)len; (void)pc; (void)out; (void)out_cap; (void)out_len; return 0;
}
int saved_bytes(const uint8_t *code, size_t len) {
    // TODO [CLVM-PEEP-03]
    (void)code; (void)len; return 0;
}
