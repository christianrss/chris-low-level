# Tooling - construindo um mini objdump/PE-ELF inspector

## O que você precisa entender antes de começar

Ferramentas como `objdump`, PE-bear, IDA e Ghidra começam lendo bytes. Antes de desenhar gráficos de fluxo ou decompilar, elas precisam saber que formato de arquivo estão lendo, onde estão as sections e quais bytes representam código.

### File offset, virtual address e RVA

- file offset: posição do byte dentro do arquivo no disco;
- virtual address (VA): endereço quando mapeado na memória do processo;
- RVA: endereço relativo à base de carregamento, muito usado em PE.

Não confunda essas coordenadas.

### ELF

Um ELF64 inicia com `0x7F 'E' 'L' 'F'`. O header aponta para a section header table. Cada section header descreve nome, endereço virtual, offset no arquivo e tamanho. Os nomes ficam em uma string table.

### PE

Um PE começa por `MZ`. Em offset `0x3C`, um campo aponta para a assinatura `PE\0\0`. Depois vem o COFF header, optional header e section table. A section `.text` normalmente contém código executável.

### Leitura little-endian segura

Não faça `reinterpret_cast` de bytes arbitrários para structs sem validar alinhamento/tamanho. O laboratório usa funções `read_u16_le`, `read_u32_le` e `read_u64_le` que checam bounds.

### x86-64 é variável

Instruções x86-64 têm tamanho variável. Podem incluir prefixes, opcode, ModR/M, SIB, displacement e immediate. O decoder de hoje reconhece apenas um subconjunto. Quando não entende, emite `db 0xNN` e avança um byte. Isso é melhor que ler bytes além do buffer ou travar.

### CALL/JMP relativos

Para `CALL rel32` e `JMP rel32`, o operando é um deslocamento assinado relativo ao endereço da próxima instrução:

```text
target = next_instruction_address + displacement
```

## Passo a passo guiado

1. Compile `test_target`.
2. Abra o binário em hexadecimal e identifique `ELF` ou `MZ`.
3. Rode `miniobjdump` e confira a lista de sections.
4. Localize `.text` e compare offset no arquivo com endereço virtual/RVA.
5. Leia a função `decode_x86_64` linha a linha.
6. Entenda por que o decoder sempre precisa avançar o PC.
7. Compare a saída com `objdump -d` ou `dumpbin /disasm`.
8. Adicione mais uma instrução simples ao decoder, por exemplo `int3` (`0xCC`) ou `leave` (`0xC9`).
9. Como exercício difícil, marque destinos de `CALL`/`JMP` e comece um mapa de cross-references.

## Exercícios

- Fácil: detectar formato e validar magic/signature.
- Médio: enumerar sections e localizar `.text`.
- Difícil: ampliar o decoder e calcular destinos relativos.
- Desafio principal: começar a separar basic blocks usando entradas, saltos e retornos.
