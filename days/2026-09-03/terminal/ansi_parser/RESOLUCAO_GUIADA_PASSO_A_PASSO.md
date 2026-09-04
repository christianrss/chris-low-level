# Resolucao guiada

1. Construa uma grade linear `rows*cols` inicializada com espacos.
2. Implemente o estado Ground: caracteres imprimiveis escrevem na celula; CR zera coluna; LF avanca linha.
3. Ao receber ESC, mude para Escape; se o proximo byte for `[`, entre em CSI.
4. Acumule digitos de parametro. Quando chegar um final byte 0x40..0x7E, aplique o comando e volte ao Ground.
5. Escreva um teste fragmentado: envie `A ESC`, depois `[2C`, depois `B`. Se funcionar, seu parser realmente e incremental.
6. Benchmarke MiB/s de parsing, mas mantenha correctness/golden tests como criterio principal.

## Etapa de código 1 - estado Ground

Implemente primeiro texto normal, CR e LF. Só então adicione ESC.

```cpp
if (raw == 0x1B) {
    state_ = State::Escape;
} else if (ch == '\n') {
    row_ = std::min(rows_ - 1, row_ + 1);
} else if (ch == '\r') {
    col_ = 0;
} else if (ch >= 0x20 && ch != 0x7F) {
    put(ch);
}
```

## Etapa de código 2 - ESC e CSI

```cpp
case State::Escape:
    if (ch == '[') {
        param_text_.clear();
        state_ = State::Csi;
    } else {
        state_ = State::Ground;
    }
    break;
```

Dentro de CSI, acumule dígitos e só execute quando chegar o final byte.

## Teste que prova incrementalidade

```cpp
Terminal fragmented(8, 2);
fragmented.feed("A\x1b");
fragmented.feed("[2C");
fragmented.feed("B");
assert(fragmented.at(0, 0) == 'A');
assert(fragmented.at(0, 3) == 'B');
```

Se esse teste falhar, você provavelmente tratou cada `feed()` como mensagem completa. A solução final está em `solutions/src/terminal.cpp`.

