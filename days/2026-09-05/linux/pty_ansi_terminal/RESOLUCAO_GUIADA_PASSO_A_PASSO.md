# RESOLUÇÃO GUIADA — Linux / ANSI CSI parser

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `TERM-ANSI-SGR-01` | `starter/ansi.py` | `_apply_csi` final `m` + loop `feed` |
| `TERM-CURSOR-02` | `starter/ansi.py` | `_apply_csi` final `H` + loop `feed` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_ansi.py`.

> Trabalhe em `days/2026-09-05/linux/pty_ansi_terminal/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Rode `python test_ansi.py` após cada bloco.

---

## TERM-ANSI-SGR-01 — SGR (`m`) e tokenização em `feed`

### 1. O problema (starter stub)

```python
def _apply_csi(self, params: str, final: str) -> None:
    # TODO [TERM-ANSI-SGR-01] / [TERM-CURSOR-02]
    raise NotImplementedError

def feed(self, text: str) -> None:
    # TODO [TERM-ANSI-SGR-01] [TERM-CURSOR-02]
    raise NotImplementedError
```

Sem `feed`, literais e CSI nunca entram. Sem `m`, `fg` fica 7 e o teste falha em `\x1b[31m` → `fg=1`.

### 2. O algoritmo

```text
_apply_csi(params, final):
  values ← [int(x) ou 0] de params.split(";") ; se params vazio → [0]
  se final == "m":
    para v em values: 0 → fg=7 ; 31 → fg=1
  (H fica para o próximo TODO)

feed(text):
  index ← 0
  enquanto index < len(text):
    se text[index:index+2] == ESC+"[":
      cursor ← index+2; avançar até char em "mH"
      se fim sem final → ValueError("incomplete CSI")
      _apply_csi(params, final); index ← após final
    senão: screen_text += text[index]; index += 1
```

### 3. Código completo

Em `starter/ansi.py`, substitua `_apply_csi` e `feed` (deixe o branch `H` para o próximo TODO ou implemente já):

```python
def _apply_csi(self, params: str, final: str) -> None:
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
    elif final == "H":
        row = values[0] if values and values[0] else 1
        col = values[1] if len(values) > 1 and values[1] else 1
        self.row = row - 1
        self.col = col - 1

def feed(self, text: str) -> None:
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

### 4. Por que funciona?

- `params.split(";")` + `int(x) if x else 0`: `"31"` → `[31]`; `""` → `[0]`; `31;;1` não quebra em `int('')`.
- SGR só muta `fg` — escapes nunca entram em `screen_text`.
- `0` → `fg=7` é o default do teste após `\x1b[0m`.
- ESC+`[` + scan até `m`/`H`: tokeniza CSI sem consumir literais; incompleto → `ValueError`.

### 5. Verificação parcial

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-05\linux\pty_ansi_terminal\starter
python test_ansi.py
```

Com SGR+`feed` e `H` ainda stub vazio, asserts de cursor falham. Trace SGR no papel:

```text
_apply_csi("31","m") → values=[31] → fg=1
_apply_csi("0","m")  → values=[0]  → fg=7
```

---

## TERM-CURSOR-02 — Cursor Position (`H`)

### 1. O problema

O branch `elif final == "H"` no stub acima ainda precisa dos defaults 1-based e da conversão 0-based. Sem isso, `\x1b[10;20H` deixa `row=0` e `\x1b[H` pode ir a (−1,−1).

### 2. O algoritmo

```text
se final == "H":
  row ← values[0] se truthy senão 1
  col ← values[1] se existe e truthy senão 1
  self.row ← row - 1
  self.col ← col - 1
```

### 3. Código completo

O bloco `H` já está no código da seção anterior — confirme que está assim:

```python
elif final == "H":
    row = values[0] if values and values[0] else 1
    col = values[1] if len(values) > 1 and values[1] else 1
    self.row = row - 1
    self.col = col - 1
```

### 4. Por que funciona?

- ANSI é 1-based; o lab compara índices 0-based (`10;20` → `(9,19)`).
- `values[0]==0` (params vazios) é falsy → default row/col = 1 → home `(0,0)`.
- Coluna omitida (`\x1b[3H`) → `len(values)==1` → col default 1 → `self.col=0`.

### 5. Verificação

```powershell
python test_ansi.py
```

Esperado: `OK ansi`.

Trace do teste principal `"A\x1b[31mB\x1b[10;20HC\x1b[0m"`:

```text
'A' → screen_text="A"
CSI 31m → fg=1
'B' → "AB"
CSI 10;20H → row=9,col=19
'C' → "ABC"
CSI 0m → fg=7
```

REPL rápido:

```python
from ansi import AnsiParser
p = AnsiParser()
p.feed("\x1b[3;5H")
print(p.row, p.col)  # 2 4
```

---

## Como depurar se falhar

- Escapes em `screen_text`: branch CSI não dispara — confira `\x1b` e `[`.
- `row == 10`: esqueceu `row - 1`.
- `\x1b[H` ≠ `(0,0)`: trate `0` como “usar default 1”.
- `int('')`: use `int(x) if x else 0`.
- Import/`Terminal`: a classe deve ser `AnsiParser`.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| TERM-ANSI-SGR-01 | `ansi.py` | `\x1b[31m` → fg=1; `\x1b[0m` → fg=7; literais em `screen_text` |
| TERM-CURSOR-02 | `ansi.py` | `\x1b[10;20H` → (9,19); `\x1b[H` → (0,0) |

Critério de aceite: `python test_ansi.py` imprime `OK ansi`. Se `screen_text != "ABC"`, caracteres dentro de CSI estão sendo concatenados por engano.
