# Teoria passo a passo

## 1. VM de bytecode
A VM mantém `ip` (instruction pointer), stack e programa. Cada instrução altera estado. Branches são o primeiro passo para sair de uma sequência linear e expressar `if`, loops e controle de fluxo.

## 2. JZ
`JZ target` remove uma condição da stack. Se ela for zero, `ip` vira `target`; caso contrário, avança uma instrução. O erro clássico é sobrescrever `ip` e depois incrementá-lo novamente.

## 3. JMP
`JMP target` é salto incondicional. O target precisa ser interpretado com a mesma convenção usada pelo assembler/programa de teste.

## 4. Trace
Para depurar uma VM, trace `ip`, instrução atual e snapshot da stack. Isso transforma bugs de controle de fluxo em uma sequência observável.

## 5. Evolução
Com branches estáveis podemos adicionar call frames, locals, exceptions, bytecode verifier, inline cache e JIT educacional.