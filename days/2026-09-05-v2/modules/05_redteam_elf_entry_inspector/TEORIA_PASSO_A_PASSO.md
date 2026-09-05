# Teoria passo a passo

## 1. Escopo seguro
Este módulo é análise estática de formato ELF. Ele não executa o arquivo, não injeta código e não altera binários. O objetivo é aprender parsing defensivo de um formato real.

## 2. ELF ident
Os 16 primeiros bytes contêm magic `0x7f ELF`, classe e endianness. O laboratório aceita apenas ELF64 little-endian. Validar tamanho antes de ler impede acesso fora do buffer.

## 3. Header ELF64
Depois do ident, campos como `e_type`, `e_machine`, `e_version` e `e_entry` aparecem em ordem definida pelo ABI. `e_entry` é o endereço virtual do entry point, não um offset simples dentro do arquivo.

## 4. Parsing robusto
Nunca faça unpack antes de conferir o comprimento mínimo. Rejeite formatos não suportados explicitamente; comportamento silencioso em parser binário é fonte de bugs e vulnerabilidades.

## 5. Próximos passos
A trilha pode evoluir para program headers, section headers, símbolos, relocations e disassembly em fixtures próprias.