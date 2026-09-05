# Teoria passo a passo

## 1. Da linguagem ao CIL
C# normalmente compila para Common Intermediate Language (CIL), armazenado em assemblies. O CLR carrega metadados e executa/JIT-compila métodos. Hoje construímos um decoder minúsculo para visualizar o nível abaixo do C#.

## 2. Stream de opcodes
O decoder percorre um `byte[]` com índice `i`. Cada instrução registra offset, mnemonic e operand opcional. Alguns opcodes ocupam um byte; outros exigem operand.

## 3. `ldc.i4.s`, `add`, `ret`
`ldc.i4.s` (`0x1F`) consome um operando `int8` assinado. `add` (`0x58`) e `ret` (`0x2A`) não consomem operand adicional. O detalhe crítico é avançar `i` corretamente.

## 4. Bounds e sinal
Antes de ler o operand, cheque `i >= code.Length`. O cast para `sbyte` preserva valores negativos. Parsers de bytecode precisam tratar truncamento como erro, não como dado zero.

## 5. Próxima evolução
Depois podemos ler method bodies reais de PE/CLI metadata, construir stack-effect analysis e um interpretador educacional.