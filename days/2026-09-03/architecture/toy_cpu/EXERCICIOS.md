# Exercícios — CPU toy

## Fácil

- **CPU-READ-01:** decodifique manualmente `10 00 05 00 01` e preveja `R0` e estado de `halted`.
- **CPU-MOVI-01:** implemente apenas `MOVI` em `starter/src/cpu.cpp` e confirme que o primeiro fetch funciona.

## Médio

- **CPU-STEP-01:** complete `ADD`, `STORE`, `LOAD` e `JNZ` no mesmo `step()`.
- **CPU-ENDIAN-01:** explique por escrito por que `0x1234` vira bytes `34 12` na memória.

## Difícil

- **CPU-JNZ-01:** escreva um programa de loop que decrementa R0 até zero usando `JNZ`; calcule o target absoluto no papel antes de codificar.
- **CPU-TRACE-01:** adicione logs temporários de `pc_` e registradores a cada `step()` e compare com sua simulação manual.

## Desafio

- **CPU-ISA-01:** proponha um opcode `SUB` sem quebrar programas existentes; defina encoding e semântica.
- **CPU-CMP-01:** compare este ISA com RV32I: quais instruções têm equivalente direto?
