# Exercícios — PTY / ANSI terminal

## Fácil — TERM-ANSI-SGR-01
Explique o que `\x1b[31m` faz no modelo didático (`fg=1`).

## Médio — TERM-ANSI-SGR-01
Implemente SGR em `_apply_csi`: `0m` reseta, `31m` vermelho.

## Médio — TERM-CURSOR-02
Implemente cursor `H` com conversão 1-based → 0-based.

## Difícil
Implemente `feed()` completo separando literais de CSI; trate CSI incompleto com `ValueError`.

## Desafio
Adicione suporte a `J` (erase display) que limpa `screen_text`.

## Reflexão
Por que terminais reais precisam de grid 2D em vez de apenas `screen_text` linear?
