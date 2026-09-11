.intel_syntax noprefix
.text
.global wasm_magic_ok
wasm_magic_ok:
    cmp byte ptr [rdi], 0
    jne 1f
    cmp byte ptr [rdi+1], 0x61
    jne 1f
    cmp byte ptr [rdi+2], 0x73
    jne 1f
    cmp byte ptr [rdi+3], 0x6d
    jne 1f
    mov eax, 1
    ret
1:
    xor eax, eax
    ret
.global wasm_version_is_1
wasm_version_is_1:
    mov eax, dword ptr [rdi+4]
    cmp eax, 1
    jne 2f
    mov eax, 1
    ret
2:
    xor eax, eax
    ret
.global section_class
section_class:
    movzx eax, dil
    cmp al, 1
    je 3f
    cmp al, 2
    jne 4f
    mov eax, 2
    ret
3:
    mov eax, 1
    ret
4:
    xor eax, eax
    ret
