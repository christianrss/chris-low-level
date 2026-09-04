# PEDAGOGY-SOLUTION: ASM-SUM-01

.text
.globl asm_sum_u64
.type asm_sum_u64, @function
asm_sum_u64:
    xor %rax, %rax
    test %rsi, %rsi
    je .done
.loop:
    add (%rdi), %rax
    add $8, %rdi
    dec %rsi
    jne .loop
.done:
    ret
.size asm_sum_u64, .-asm_sum_u64
