# Systems - CLVM: formato binário, assembler, loader e máquina virtual

## O que você precisa entender antes de começar

Este laboratório começa por uma máquina virtual pequena porque ela reúne várias ideias que reaparecem em sistemas operacionais, emuladores, compiladores, bancos de dados e debuggers.

Um computador real executa **instruções de máquina** definidas por uma ISA (Instruction Set Architecture), como x86-64 ou RISC-V. Cada instrução é representada por bytes. Uma máquina virtual faz algo parecido em software: ela define seu próprio conjunto de opcodes e interpreta esses bytes.

### Bits, bytes e hexadecimal

- bit: um valor 0 ou 1;
- byte: 8 bits;
- hexadecimal: representação em base 16; cada dígito hexadecimal representa 4 bits;
- `0x01` é um byte com valor decimal 1;
- `0xFF` é um byte com valor decimal 255.

### Little-endian

Quando um inteiro ocupa vários bytes, precisamos definir a ordem dos bytes. Na CLVM, inteiros são little-endian. O inteiro de 32 bits `0x12345678` aparece no arquivo como `78 56 34 12`.

### Header e payload

O arquivo `.clvm` possui duas partes:

1. header de 16 bytes: metadados usados para validar e localizar o código;
2. bytecode: instruções que a VM executa.

O header contém magic `CLVM`, version, flags, entry, code_size e checksum. Nunca confie em `code_size` antes de comparar com o tamanho real do buffer.

### Assembler, loader e interpreter

Fluxo do laboratório:

```text
programa.asm
    |
    v
assemble.py  ->  programa.clvm
                    |
                    v
             clvm_loader.c
                    |
                    v
                 main.cpp
              fetch/decode/execute
```

O assembler converte mnemonics como `PUSH 7` em bytes. O loader valida o arquivo. O interpreter mantém um `PC` (program counter), lê o opcode, decodifica a operação e executa.

### Stack machine

A CLVM é uma stack machine. Operandos ficam em uma pilha LIFO. Para calcular `7 + 5`:

```text
PUSH 7    stack = [7]
PUSH 5    stack = [7, 5]
ADD       stack = [12]
PRINT     imprime 12 e remove o valor
HALT      encerra
```

Isso é diferente de RISC-V, que usa registradores explícitos, mas o ciclo fetch/decode/execute é a mesma ideia central.

### Checksum FNV-1a

O checksum detecta corrupção acidental dos bytes. Ele não é criptografia. Para cada byte:

```text
hash = hash XOR byte
hash = hash * 16777619 (mod 2^32)
```

Se um byte do código mudar, o loader recalcula o checksum e deve rejeitar o arquivo.

### Saltos relativos

`JMP` e `JZ` carregam um deslocamento assinado de 16 bits. O destino é calculado a partir do PC logo depois do operando. Isso torna o bytecode relocável dentro do arquivo.

## Passo a passo guiado

1. Leia `docs/FORMAT.md` e desenhe o header de 16 bytes em papel.
2. Abra `starter/tools/assemble.py` e encontre a função de checksum.
3. Implemente FNV-1a no Python e em `starter/src/clvm_loader.c`.
4. Gere `arithmetic.clvm`.
5. Abra o arquivo com `starter/tools/inspect_clvm.py` ou um hex editor e localize `43 4C 56 4D`, que é `CLVM` em ASCII.
6. Compile o loader/VM.
7. Rode com `--trace` e observe `pc`, opcode e stack.
8. Corrompa um byte e confirme que o loader recusa o arquivo antes da execução.
9. Implemente/estude `JMP` e `JZ` e execute `countdown.asm`.
10. Compare o loop da CLVM com o primeiro passo de um emulador RISC-V: buscar bytes, decodificar e atualizar PC.

## Exercícios

- Fácil: checksum + inspeção hexadecimal.
- Médio: parser seguro + programa aritmético.
- Difícil: labels, `JMP`, `JZ` e countdown.
- Desafio: explique como você adicionaria um opcode `LOAD` sem quebrar a validação de limites.

## Como saber se está correto

- `arithmetic.asm` deve imprimir `38`;
- `countdown.asm` deve imprimir `3 2 1 0`;
- arquivo corrompido deve produzir `checksum mismatch`;
- um salto para fora do código deve ser rejeitado.
