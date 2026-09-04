.text
.globl asm_sum_u64
.type asm_sum_u64, @function
asm_sum_u64:
    # TODO: preserve the ABI contract and implement the loop.
    xor %rax, %rax
    ret
.size asm_sum_u64, .-asm_sum_u64
