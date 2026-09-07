# Exercícios — ELF64 program headers

## Fácil — offsets no papel (`D5-ELF-HEADER`)

**Enunciado:** No fixture do teste (`phoff=64`, `phentsize=56`, `phnum=2`), calcule offset inicial de cada PHDR e o byte final da tabela.

**Arquivo-alvo:** caderno; confira com `len(parse_program_headers(make()))`.

**Critério de aceite:** entrada 0 em 64, entrada 1 em 120, tabela termina em 176.

## Médio — decode de campos (`D5-ELF-PHDR`)

**Enunciado:** Implemente o loop de decode e imprima `type`, `offset`, `filesz`, `memsz` da primeira entrada. Identifique o segmento PT_LOAD.

**Arquivo-alvo:** `starter/elf_phdr.py`.

**Critério de aceite:** `type==1`, `offset==200`, `filesz==16`, `memsz==32` no fixture oficial.

## Difícil — bounds defensivos (`D5-ELF-RANGE`)

**Enunciado:** Rejeite binário truncado (`phoff+ents*num > len`) e segmento com `p_offset+p_filesz > len`. Crie mutação local além do teste.

**Arquivo-alvo:** `starter/elf_phdr.py`.

**Critério de aceite:** mutação do teste levanta `ValueError`; fixture válido passa.

## Desafio — flags como metadado

**Enunciado:** Estenda saída com campo `readable=(flags & 4) != 0` sem alterar validação existente. Documente flag PF_R da ABI.

**Arquivo-alvo:** extensão em `starter/elf_phdr.py`.

**Critério de aceite:** fixture com `flags=5` marca readable; testes originais intactos.
