#include "clvm_disasm.h"
#include <stdio.h>
int decode_push(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* TODO [CLVM-DIS-01]: opcode 0x01 + imm32 LE. line "PUSH N", size 5. */
    (void)data; (void)len; (void)offset; (void)out;
    return -1;
}
int decode_branch(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* TODO [CLVM-DIS-02]: JMP/JZ/CALL/JNZ + u16 LE. size 3. */
    (void)data; (void)len; (void)offset; (void)out;
    return -1;
}
int disassemble_all(const uint8_t *code, size_t len, char lines[][64], int max_lines) {
    /* TODO [CLVM-DIS-03]: walk with pc += size. */
    (void)code; (void)len; (void)lines; (void)max_lines;
    return -1;
}
