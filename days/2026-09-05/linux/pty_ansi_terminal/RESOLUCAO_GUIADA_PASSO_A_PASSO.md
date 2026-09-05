# Resolução guiada passo a passo — Linux — ANSI Parser

## Mapa exato starter → resolução

- `TERM-ANSI-SGR-01` → `starter/ansi.py` (`_apply_csi` final `m`, `feed` loop CSI)
- `TERM-CURSOR-02` → `starter/ansi.py` (`_apply_csi` final `H`)

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/linux/pty_ansi_terminal/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

```bash
cd days/2026-09-05/linux/pty_ansi_terminal/starter
python test_ansi.py
```

Baseline: `NotImplementedError` em `feed` ou `_apply_csi`. Os testes devem falhar até implementar os TODOs.

## Exercício médio — `TERM-ANSI-SGR-01` em `_apply_csi`

### Arquivo

Abra `starter/ansi.py`, localize `_apply_csi`.

Substitua o corpo por:

```python
values = (
    [int(x) if x else 0 for x in params.split(";")]
    if params
    else [0]
)

if final == "m":
    for value in values:
        if value == 0:
            self.fg = 7
        elif value == 31:
            self.fg = 1
```

Deixe `elif final == "H":` para o próximo TODO (ou implemente stub vazio temporariamente).

### Por que funciona?

- `params.split(";")` decompõe `"31"` → `["31"]` e `"0"` → `["0"]`.
- `int(x) if x else 0` trata segmentos vazios em sequências como `31;;1`.
- SGR não altera `screen_text` — apenas estado `fg`.
- `0` restaura o default 7 exigido pelo teste após `\x1b[0m`.

### Trace no papel

`_apply_csi("31", "m")`:

```text
values = [31]
value 31 → fg = 1
```

`_apply_csi("0", "m")`:

```text
values = [0]
value 0 → fg = 7
```

## Exercício médio — `TERM-CURSOR-02` em `_apply_csi`

No mesmo método, após o bloco `m`, adicione:

```python
elif final == "H":
    row = values[0] if values and values[0] else 1
    col = values[1] if len(values) > 1 and values[1] else 1
    self.row = row - 1
    self.col = col - 1
```

### Por que funciona?

- ANSI usa coordenadas 1-based; os testes comparam com índices 0-based.
- `\x1b[H` tem `params=""` → `values=[0]` → `values[0]` é 0 (falsy) → default row=1 → `self.row=0`.
- Coluna omitida (`\x1b[3H`) usa default col=1 → `self.col=0`.

### Trace no papel

`_apply_csi("10;20", "H")`:

```text
values = [10, 20]
row = 10, col = 20
self.row = 9, self.col = 19
```

`_apply_csi("", "H")`:

```text
values = [0]
row default 1 → self.row = 0
col default 1 → self.col = 0
```

## Exercício difícil — `feed` (ambos os IDs)

Localize `feed` e implemente o loop:

```python
index = 0
while index < len(text):
    if (
        text[index] == "\x1b"
        and index + 1 < len(text)
        and text[index + 1] == "["
    ):
        cursor = index + 2
        while cursor < len(text) and text[cursor] not in "mH":
            cursor += 1
        if cursor >= len(text):
            raise ValueError("incomplete CSI")
        self._apply_csi(text[index + 2 : cursor], text[cursor])
        index = cursor + 1
    else:
        self.screen_text += text[index]
        index += 1
```

### Por que funciona?

- Detecta início CSI com ESC + `[` sem consumir bytes prematuramente.
- O inner `while` acumula params até `m` ou `H` — os únicos finals deste lab.
- `cursor >= len(text)` sem final → `ValueError` conforme TESTES_GUIADOS.
- Caracteres fora de CSI vão para `screen_text` um a um.

### Trace do teste `test_sgr_and_cursor`

Entrada `"A\x1b[31mB\x1b[10;20HC\x1b[0m"`:

```text
'A' → screen_text="A"
CSI 31m → fg=1
'B' → screen_text="AB"
CSI 10;20H → row=9,col=19
'C' → screen_text="ABC"
CSI 0m → fg=7
```

## Rode os testes novamente

```bash
python test_ansi.py
```

Saída esperada:

```text
OK ansi
```

## Como depurar se falhar

- **`screen_text` com escapes visíveis:** o branch CSI não está sendo tomado; verifique `\x1b` e `[`.
- **`row == 10` em vez de 9:** você esqueceu de subtrair 1 (ANSI é 1-based).
- **`\x1b[H` não vai para (0,0):** trate `values[0]==0` como "usar default 1", não como linha 0.
- **`ValueError: invalid literal` em split:** use `int(x) if x else 0`.
- **Import `Terminal`:** a classe deve se chamar `AnsiParser`.

Teste manual rápido no REPL:

```python
from ansi import AnsiParser
p = AnsiParser()
p.feed("\x1b[3;5H")
print(p.row, p.col)  # 2 4
```

## Solução final comentada

Compare com `solutions/ansi.py`. Você deve explicar: separação literal vs CSI, conversão 1-based→0-based, e por que SGR não toca `screen_text`.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| TERM-ANSI-SGR-01 | `ansi.py` | `\x1b[31m` → fg=1; `\x1b[0m` → fg=7; literais em `screen_text` |
| TERM-CURSOR-02 | `ansi.py` | `\x1b[10;20H` → (9,19); `\x1b[H` → (0,0) |

Critério de aceite: `python test_ansi.py` imprime `OK ansi`. Se `screen_text != "ABC"` no teste principal, revise se caracteres dentro de CSI estão sendo concatenados por engano.
