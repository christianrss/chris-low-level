#include "clvm_disasm.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* PEDAGOGY-TEST: CLVM-DIS-01 */
/* PEDAGOGY-TEST: CLVM-DIS-02 */
/* PEDAGOGY-TEST: CLVM-DIS-03 */
int main(void) {
    uint8_t push42[] = {0x01, 0x2A, 0x00, 0x00, 0x00};
    uint8_t jmp10[] = {0x09, 0x0A, 0x00};
    uint8_t prog[] = {0x01, 0x2A, 0x00, 0x00, 0x00, 0x02, 0x08};
    ClvmInsn in;
    char lines[8][64];
    int n;
    assert(decode_push(push42, 5, 0, &in) == 0);
    assert(strcmp(in.line, "PUSH 42") == 0 && in.size == 5);
    assert(decode_branch(jmp10, 3, 0, &in) == 0);
    assert(strcmp(in.line, "JMP 10") == 0 && in.size == 3);
    n = disassemble_all(prog, sizeof prog, lines, 8);
    assert(n == 3);
    assert(strcmp(lines[0], "PUSH 42") == 0);
    assert(strcmp(lines[1], "ADD") == 0);
    assert(strcmp(lines[2], "HALT") == 0);
    assert(disassemble_all((const uint8_t *)"\xff", 1, lines, 8) < 0);
    printf("OK clvm_disasm\n");
    return 0;
}
