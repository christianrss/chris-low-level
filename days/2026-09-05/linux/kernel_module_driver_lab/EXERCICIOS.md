# Exercícios — Kernel driver lifecycle

## Fácil — KMOD-MODEL-OPEN-01
Implemente `device_open()` com exclusividade: primeiro open retorna 0, segundo retorna -1.

## Médio — KMOD-MODEL-IO-02
Implemente `device_write()` e `device_read()` que retornam -1 quando o dispositivo está fechado.

## Médio — KMOD-MODEL-IO-02
Truncar `count` no write para não ultrapassar 64 bytes; no read, limitar a `length`.

## Difícil — KMOD-SOURCE-REVIEW-03
Liste três melhorias que você faria em `chris_char.c` antes de carregar em kernel real (ex.: `copy_from_user`, logging, tratamento de erro em init).

## Desafio
Adicione teste que escreve 100 bytes e verifica que apenas 64 são aceitos.

## Reflexão
Compare o modelo `is_open` com `struct file` e refcount no VFS Linux.
