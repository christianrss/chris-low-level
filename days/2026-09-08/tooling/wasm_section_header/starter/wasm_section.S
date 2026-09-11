/* TODO [TOOL-WASM-01] */
.intel_syntax noprefix
.text
.global wasm_magic_ok
wasm_magic_ok:
    xor eax, eax
    ret
.global wasm_version_is_1
wasm_version_is_1:
    xor eax, eax
    ret
.global section_class
section_class:
    xor eax, eax
    ret
