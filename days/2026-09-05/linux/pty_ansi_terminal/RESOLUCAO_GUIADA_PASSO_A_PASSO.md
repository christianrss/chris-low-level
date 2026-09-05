# Resolução guiada passo a passo — Linux terminal: ANSI parser como preparação para PTY/TTY

Abra `starter/ansi.py`. Em `feed`, percorra caracteres. Quando encontrar `[`, leia até um byte final `m` ou `H`. Para `m`, converta parâmetros; `0` reseta fg=7, `31` fg=1. Para `H`, parseie `row;col`, default 1,1, e grave `row-1,col-1`. Texto normal é acumulado em `screen_text`.

Use helper `_apply_csi(params, final)` para manter o parser testável. Debug: imprima `repr(seq)`, `params`, `final` sem imprimir ESC diretamente no seu terminal.

## Mapa de consistência auditada
- `TERM-ANSI-SGR-01` — starter → resolução → teste → solution.
- `TERM-CURSOR-02` — starter → resolução → teste → solution.
