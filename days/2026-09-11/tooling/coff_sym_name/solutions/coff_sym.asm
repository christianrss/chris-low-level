option casemap:none
.code
coff_name_is_long PROC
    ; PEDAGOGY-SOLUTION: TOOL-COFF-01
    cmp dword ptr [rcx], 0
    jne L0
    mov eax, 1
    ret
L0:
    xor eax, eax
    ret
coff_name_is_long ENDP
coff_name_is_short PROC
    ; PEDAGOGY-SOLUTION: TOOL-COFF-02
    cmp dword ptr [rcx], 0
    je S0
    mov eax, 1
    ret
S0:
    xor eax, eax
    ret
coff_name_is_short ENDP
coff_short_name_len PROC
    ; PEDAGOGY-SOLUTION: TOOL-COFF-03
    xor eax, eax
    mov rdx, rcx
L1:
    cmp eax, 8
    jge L2
    cmp byte ptr [rdx+rax], 0
    je L2
    inc eax
    jmp L1
L2:
    ret
coff_short_name_len ENDP
END
