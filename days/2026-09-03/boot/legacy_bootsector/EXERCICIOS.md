# Exercícios — legacy boot sector

## Fácil

- **BOOT-READ-01:** desenhe o mapa de 512 bytes marcando código, padding e assinatura.
- **BOOT-IMAGE-01:** implemente `build_image()` em `starter/tools/build_minimal.py`.

## Médio

- **BOOT-ASM-01:** explique cada instrução em `starter/src/bootsector.asm` e relacione com os bytes hex.
- **BOOT-TEST-01:** faça `test_boot.py` passar sem modificar os asserts.

## Difícil

- **BOOT-QEMU-01:** monte com NASM e execute em QEMU; descreva o que aparece na tela.
- **BOOT-DIFF-01:** compare bytes gerados por Python vs `nasm -f bin` (se disponível).

## Desafio

- **BOOT-EXT-01:** altere o caractere impresso para `'!' ` sem quebrar tamanho/assinatura; documente mudança de bytes.
- **BOOT-UEFI-01:** escreva um parágrafo comparando este fluxo com boot UEFI/GPT.
