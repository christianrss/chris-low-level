#ifndef WASM_API_H
#define WASM_API_H
int wasm_magic_ok(const unsigned char *p);
int wasm_version_is_1(const unsigned char *p);
int section_class(unsigned char id);
#endif
