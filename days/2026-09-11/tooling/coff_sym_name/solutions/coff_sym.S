.global coff_name_is_long
.global coff_name_is_short
.global coff_short_name_len
.text
coff_name_is_long:
    # PEDAGOGY-SOLUTION: TOOL-COFF-01
    cmpl $0, (%rdi)
    jne 1f
    movl $1, %eax
    ret
1:
    xor %eax, %eax
    ret
coff_name_is_short:
    # PEDAGOGY-SOLUTION: TOOL-COFF-02
    cmpl $0, (%rdi)
    je 2f
    movl $1, %eax
    ret
2:
    xor %eax, %eax
    ret
coff_short_name_len:
    # PEDAGOGY-SOLUTION: TOOL-COFF-03
    xor %eax, %eax
3:
    cmpl $8, %eax
    jge 4f
    cmpb $0, (%rdi,%rax)
    je 4f
    incl %eax
    jmp 3b
4:
    ret
