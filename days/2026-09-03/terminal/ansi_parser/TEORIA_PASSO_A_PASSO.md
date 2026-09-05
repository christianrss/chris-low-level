# Teoria passo a passo — terminal como máquina de estados ANSI/CSI

## 1. O que estamos construindo

Um terminal em memória que consome bytes (não “linhas prontas”) e interpreta caracteres imprimíveis, CR/LF e sequências CSI iniciadas por `ESC [`.

## 2. Por que parser incremental

Uma leitura de socket ou PTY pode cortar no meio de `\x1b[2C`. O estado (`Ground`, `Escape`, `Csi`) deve persistir entre chamadas a `feed()`.

```text
feed("A\x1b")   -> estado Escape
feed("[2C")      -> move cursor +2 colunas
feed("B")         -> imprime B na posição correta
```

## 3. Diagrama de estados

```text
        +--------------------------------+
        |            Ground              |
        +--------------------------------+
          | 0x1B          | \n / \r / printable
          v               v
    +-----------+    atualiza grid/cursor
    |  Escape   |
    +-----------+
          | '['
          v
    +-----------+
    |    CSI    |-- dígitos -> param_text_
    +-----------+
          | final 0x40-0x7E
          v
      handle_csi()
          |
          v
        Ground
```

## 4. Sequências suportadas (milestone)

| Sequência | Efeito |
|-----------|--------|
| `CSI n A` | cursor up n (default 1) |
| `CSI n B` | cursor down n |
| `CSI n C` | cursor right n |
| `CSI n D` | cursor left n |
| `CSI 2 J` | erase display |
| `CSI ... m` | SGR reconhecido, estilo não aplicado |

## 5. Exemplo numérico

Grid 10×4, cursor (0,3), feed `\x1b[2D!`:

```text
param n=2, final 'D' -> col = max(0, 3-2) = 1
'!' em (0,1)
```

## 6. Implementação interna

- `param_or(fallback)`: converte `param_text_` ou usa default.
- `handle_csi` (`TERM-CSI-01`): switch no byte final.
- `feed` (`TERM-FEED-01`): loop char a char com `state_` membro.

## 7. Invariantes

- `row_ < rows_`, `col_ < cols_` após movimentos.
- Caracteres de controle `< 0x20` (exceto CR/LF) não imprimem em Ground.
- Após CSI completo, `param_text_` limpo e estado Ground.
- `ESC` sem `[` retorna a Ground (sequência desconhecida ignorada).

## 8. Complexidade

- `feed` de n bytes: O(n).
- `CSI 2 J` clear: O(rows*cols) — aceitável em grid pequeno do lab.

## 9. Bugs comuns

- Resetar estado a Ground no fim de cada `feed`.
- Tratar `\n` como printable.
- `param_text_` limpo antes de `handle_csi` ler o parâmetro.
- Confundir `CSI 2 J` (erase) com `CSI 2 K` (erase line).
- ESC impresso na tela porque testou char antes de byte 0x1B.

## 10. Comparação com produção

| Lab | xterm / Windows Terminal / VT |
|-----|-------------------------------|
| subset CSI | centenas de sequências |
| grid char | Unicode, grapheme clusters |
| sem PTY | kernel + driver + font shaping |
| SGR noop | 256/truecolor, hyperlinks |

O núcleo — máquina de estados incremental — é idêntico.

## 11. Passo a passo guiado

1. Implemente `param_or` e `handle_csi`.
2. Reescreva `feed` com três estados.
3. Teste fragmentação `A\x1b` + `[2C` + `B`.
4. Teste `CSI 2 J` após texto.
5. `ctest --test-dir starter/build`.

## 12. Como saber se está correto

Todos os asserts em `starter/tests/test_terminal.cpp` passam; cursor e células batem com roteiro manual.
## 1. O que estamos construindo

Um terminal textual mínimo que consome bytes e mantém uma grade de caracteres mais cursor. Não é um emulador completo: suportamos subset de CSI para movimento e limpeza.

## 2. Por que parser incremental

Dados chegam em chunks arbitrários. Um `ESC` pode ser o último byte do chunk; o próximo chunk completa `[` e inicia CSI.

```text
chunk1: "Hello\x1b"
chunk2: "[2JWorld"
```

## 3. Diagrama de estados

```text
        printable
Ground ---------> escreve célula
  |  ESC
  v
Escape --- '[' --> Csi --- final byte --> handle_csi --> Ground
```

## 4. CSI suportados

| Sequência | Efeito |
|-----------|--------|
| CSI n A | cursor up n |
| CSI n B | cursor down n |
| CSI n C | cursor right n |
| CSI n D | cursor left n |
| CSI 2 J | clear screen |

## 5. Parâmetros default

`ESC [ A` equivale a `n=1`. `param_or(1)` implementa esse default.

## 6. Invariantes

- Cursor clamped aos limites da grade.
- Estado preservado entre `feed()` calls.
- SGR reconhecido mas não aplicado (milestone futuro).

## 7. Bugs comuns

- Resetar estado a cada `feed()`.
- Tratar `\n` como newline sem política explícita.
- `stoi` sem fallback em parâmetro inválido.

## 8. Complexidade

O(bytes) por `feed`; CSI O(1) por sequência completa.

## 9. Comparação com produção

| Este lab | xterm / VT220 |
|----------|---------------|
| 5 CSI | dezenas de modos |
| sem UTF-8 | decode multibyte |
| grid fixa | scrollback, alt screen |

## 10. Passo a passo

1. Implemente `param_or`.
2. Complete `handle_csi` para A/B/C/D/J.
3. Máquina de estados em `feed()` (`TERM-FEED-01`).
4. Testes parciais com feed dividido.

## 11. Exemplo manual

```text
feed("Hi\x1b[2J") -> tela limpa, cursor (0,0)
feed("\x1b[5C") -> coluna 5
```

## 12. Como validar

`ctest` no starter/build; todos os `PEDAGOGY-TEST` devem passar na solution.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
