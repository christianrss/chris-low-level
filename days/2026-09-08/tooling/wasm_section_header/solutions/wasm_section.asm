option casemap:none
.code
wasm_magic_ok PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-01
    cmp byte ptr [rcx], 00h
    jne fail1
    cmp byte ptr [rcx+1], 61h
    jne fail1
    cmp byte ptr [rcx+2], 73h
    jne fail1
    cmp byte ptr [rcx+3], 6Dh
    jne fail1
    mov eax, 1
    ret
fail1:
    xor eax, eax
    ret
wasm_magic_ok ENDP
wasm_version_is_1 PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-02
    mov eax, dword ptr [rcx+4]
    cmp eax, 1
    jne fail2
    mov eax, 1
    ret
fail2:
    xor eax, eax
    ret
wasm_version_is_1 ENDP
section_class PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-03
    movzx eax, cl
    cmp al, 1
    je one
    cmp al, 2
    jne zero
    mov eax, 2
    ret
one:
    mov eax, 1
    ret
zero:
    xor eax, eax
    ret
section_class ENDP
END
