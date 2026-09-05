# Exercícios — Bytecode branch VM

## Fácil — JSVM-JZ-01
Desenhe o trace de IP para `makeProgram(0)` e `makeProgram(1)`.

## Médio — JSVM-JZ-01
Implemente `JZ` com pop e salto condicional.

## Médio — JSVM-JMP-02
Implemente `JMP` incondicional sem incrementar `ip` depois.

## Difícil
Adicione opcode `ADD` que pop dois valores, push soma, e teste programa aritmético.

## Desafio
Implemente loop com `JZ` + `JMP` que soma 1..10 na stack.

## Reflexão
Como um bytecode verifier detectaria `JMP` para meio de instrução multi-byte?
