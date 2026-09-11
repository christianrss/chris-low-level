#ifndef CLVM_DISASM_H
#define CLVM_DISASM_H
#include <stddef.h>
#include <stdint.h>
#define CLVM_PUSH 0x01
typedef struct { char line[64]; int size; } ClvmInsn;
int decode_push(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out);
int decode_branch(const uint8_t *data, size_t len, size_t offset, ClvmInsn *out);
int disassemble_all(const uint8_t *code, size_t len, char lines[][64], int max_lines);
#endif
