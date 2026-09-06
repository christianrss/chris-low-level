# Exercícios — CLVM extended

## Fácil

1. Paper-trace `add2.asm`: desenhe data stack e call stack a cada opcode.
2. Qual o maior `addr` válido para LOAD/STORE de i32 numa mem de 256 B?

## Médio

3. Implemente `CLVM-EXT-01` e monte `add2.asm` — confira checksum impresso.
4. Faça `bad_ret.asm` falhar com a mensagem exata do enunciado.
5. Escreva um `min.asm` que imprime o menor de dois PUSH usando `LT`/`JNZ`/`SWAP`/`DROP`.

## Difícil

6. Loop que soma 1+2+…+n com contador em `mem[0]` e acumulador em `mem[4]`.
7. Procedure recursiva `fact` com CALL/RET (cuidado com limite de call stack).
