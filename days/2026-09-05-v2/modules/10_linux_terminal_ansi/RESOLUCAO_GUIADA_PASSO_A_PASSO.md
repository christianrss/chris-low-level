# Resolução guiada passo a passo

Abra `starter/ansi.py`.

## `_apply_csi`
Para final `m`, converta parâmetros vazios para 0. Em `0`, defina `fg=7`; em `31`, `fg=1`. Isso fecha `TERM-ANSI-SGR-01`.

Para final `H`, parseie `row;col`, usando default 1. Grave `self.row=row-1` e `self.col=col-1`. Isso fecha `TERM-CURSOR-02`.

## `feed`
Percorra o texto. Ao encontrar o prefixo `\x1b[`, avance até final `m` ou `H`, separe `params` e chame `_apply_csi`. Caso contrário, acrescente o caractere em `screen_text`.

Teste:
```bash
python3 starter/test_ansi.py
```

Debug seguro: `print(repr(seq), params, final)`. Não use `print(seq)` porque a sequência pode mover o cursor do terminal real.

## Mapa de consistência auditada
- `TERM-ANSI-SGR-01` - starter -> resolução -> teste -> solution.
- `TERM-CURSOR-02` - starter -> resolução -> teste -> solution.
