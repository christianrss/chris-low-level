# Exercícios — ELF64 triage (Ehdr → Phdr → Shdr → Dynsym)

## Fácil

- **D2-ELF-STRINGS:** implemente scanner de runs ASCII 0x20..0x7E com sentinela NUL.
- Liste offsets em `b"Hello\x00World"` com `minimum=4` e `minimum=5`.

## Médio

- **D2-ELF-HEADER:** valide magic, class, endian e version; leia machine/entry/phoff/shoff/contagens.
- Desenhe o mapa dos primeiros 64 bytes com os offsets usados.

## Médio-Difícil

- **D2-ELF-PHDR:** parseie a tabela Phdr (56 B): type, offset, vaddr, filesz, memsz.
- Explique quando `memsz > filesz` aparece em um binário real.

## Difícil

- **D2-ELF-SHDR:** parseie Shdr (64 B) e resolva nomes via `e_shstrndx`.
- **D2-ELF-DYNSYM:** liste `(name, st_value)` a partir de `.dynsym`/`.dynstr` no fixture sintético.
- Compile `lab_target.c` e compare Phdr/Shdr com `readelf -l -S` como oracle externo (Linux).

## Desafio

- Rode o benchmark da pipeline header→phdr→shdr→dynsym e discuta custo vs `readelf` completo.
- Invente um fixture com `shstrndx` inválido e garanta `ValueError` (sem crash).
- Escreva duas strings que *parecem* suspeitas mas são benignas em contexto de lab/CTF.
