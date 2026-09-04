# Pesquisa guiada — CPU mínima, ISA e fetch/decode/execute

## Objetivo
Relacionar o simulador do exercício a conceitos reais de ISA sem transformar o toy CPU em uma cópia de uma arquitetura existente.

## Fontes de referência
1. RISC-V Unprivileged ISA Specification — formato e semântica de instruções como exemplo de ISA documentada.
2. Intel/AMD manuals — apenas para comparar endianness, registradores e instruções reais.
3. Textos de arquitetura sobre ciclo fetch/decode/execute.

## Termos de busca
- `instruction set architecture fetch decode execute`
- `little endian immediate encoding`
- `program counter branch relative absolute`

## Perguntas
1. Quem avança o PC e em qual momento?
2. Qual é a diferença entre opcode e operandos?
3. Por que `lo | (hi << 8)` reconstrói um `u16` little-endian?
4. O que um branch precisa definir sobre o destino e o estado do PC?
5. Que erro deve ocorrer para opcode ou registrador inválido?

Não copie encodings de RISC-V/x86; use-os apenas para entender como uma ISA real especifica comportamento verificável.
