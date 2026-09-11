#include "clvm_disasm.h"
#include <stdio.h>
#include <string.h>
static int is_branch(uint8_t op) {
    return op == 0x09 || op == 0x0A || op == 0x0B || op == 0x13;
}
static const char *op_name(uint8_t op) {
    switch (op) {
    case 0x02: return "ADD"; case 0x03: return "SUB"; case 0x08: return "HALT";
    case 0x09: return "JMP"; case 0x0A: return "JZ"; case 0x0B: return "CALL";
    case 0x13: return "JNZ";
    default: return NULL;
    }
}
int decode_push(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* PEDAGOGY-SOLUTION: CLVM-DIS-01 */
    uint32_t imm;
    if (!data || !out || offset + 5 > len || data[offset] != CLVM_PUSH) return -1;
    imm = (uint32_t)data[offset + 1]
        | ((uint32_t)data[offset + 2] << 8)
        | ((uint32_t)data[offset + 3] << 16)
        | ((uint32_t)data[offset + 4] << 24);
    snprintf(out->line, sizeof out->line, "PUSH %u", imm);
    out->size = 5;
    return 0;
}
int decode_branch(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out) {
    /* PEDAGOGY-SOLUTION: CLVM-DIS-02 */
    uint16_t rel;
    const char *name;
    if (!data || !out || offset + 3 > len || !is_branch(data[offset])) return -1;
    name = op_name(data[offset]);
    rel = (uint16_t)data[offset + 1] | ((uint16_t)data[offset + 2] << 8);
    snprintf(out->line, sizeof out->line, "%s %u", name, rel);
    out->size = 3;
    return 0;
}
int disassemble_all(const uint8_t *code, size_t len, char lines[][64], int max_lines) {
    /* PEDAGOGY-SOLUTION: CLVM-DIS-03 */
    size_t pc = 0;
    int n = 0;
    if (!code || !lines) return -1;
    while (pc < len) {
        ClvmInsn in;
        uint8_t op = code[pc];
        if (n >= max_lines) return -1;
        if (op == CLVM_PUSH) {
            if (decode_push(code, len, pc, &in) != 0) return -1;
        } else if (is_branch(op)) {
            if (decode_branch(code, len, pc, &in) != 0) return -1;
        } else {
            const char *name = op_name(op);
            if (!name) return -1;
            snprintf(in.line, sizeof in.line, "%s", name);
            in.size = 1;
        }
        snprintf(lines[n], 64, "%s", in.line);
        pc += (size_t)in.size;
        n++;
    }
    return n;
}
