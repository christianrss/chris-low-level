# Exercícios — Assembly x86-64 ABI sum

## Fácil

- **ASM-ABI-01:** liste em papel quais registradores System V carregam os dois primeiros argumentos inteiros e onde fica o retorno.
- **ASM-EMPTY-01:** implemente `asm_sum_u64` que retorna 0 sem ler memória; valide `count=0`.

## Médio

- **ASM-SUM-01:** complete o loop em `starter/src/sum_x86_64.S` e passe o teste `{1,2,3,5,8,13}`.
- **ASM-OVERFLOW-01:** adicione teste com `{UINT64_MAX, 1}` e confirme soma modular zero.

## Difícil

- **ASM-CMP-01:** compile uma versão C com `-O0` e `-O3`; compare disassembly com sua rotina Assembly.
- **ASM-WIN-01:** explique quais registradores mudariam se o mesmo contrato fosse Windows x64.

## Desafio

- **ASM-VEC-01:** esboce (sem implementar) como somar com registradores XMM e redução horizontal.
- **ASM-BENCH-01:** rode o benchmark guiado e explique por que C vetorizado pode vencer Assembly escalar.
