# Resolução guiada auditada — ANSI/CSI parser incremental

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `TERM-FEED-01` | `starter/src/terminal.cpp` | `Terminal::feed()` — máquina de estados ESC/CSI |
| `TERM-CSI-01` | `starter/src/terminal.cpp` | `Terminal::handle_csi()` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/terminal/ansi_parser/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Arquivo

```text
starter/src/terminal.cpp
```

O header já define `State::Ground`, `State::Escape`, `State::Csi`, cursores, `param_text_`, `param_or` e `handle_csi`.

## 1. Baseline

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

O starter deve compilar e falhar nos testes CSI.

## 2. `param_or`

Substitua o placeholder por:

```cpp
int Terminal::param_or(int fallback) const {
    if (param_text_.empty()) {
        return fallback;
    }

    try {
        return std::stoi(param_text_);
    } catch (...) {
        return fallback;
    }
}
```

Neste milestone há um único parâmetro textual; suporte completo a listas `1;2;3` fica para evolução posterior.

### Por que funciona?
CSI frequentemente omite o número (`ESC[C` = mover 1 coluna). `param_or(1)` devolve fallback quando `param_text_` está vazio. `stoi` com catch evita crash em sequência malformada — retorna fallback em vez de derrubar o terminal.

## 3. `handle_csi` — a versão antiga não mostrava o corpo

```cpp
void Terminal::handle_csi(char final_byte) {
    const int n = std::max(1, param_or(1));

    switch (final_byte) {
    case 'A':
        row_ = static_cast<std::size_t>(
            std::max(0, static_cast<int>(row_) - n));
        break;

    case 'B':
        row_ = std::min(rows_ - 1, row_ + static_cast<std::size_t>(n));
        break;

    case 'C':
        col_ = std::min(cols_ - 1, col_ + static_cast<std::size_t>(n));
        break;

    case 'D':
        col_ = static_cast<std::size_t>(
            std::max(0, static_cast<int>(col_) - n));
        break;

    case 'J':
        if (param_or(0) == 2) {
            std::fill(cells_.begin(), cells_.end(), ' ');
            row_ = 0;
            col_ = 0;
        }
        break;

    case 'm':
        // SGR é reconhecido, mas estilos ficam para outro milestone.
        break;

    default:
        break;
    }
}
```

Adicione os includes:

```cpp
#include <algorithm>
#include <cctype>
```

### Por que funciona?
`std::max(1, param_or(1))` garante movimento mínimo de uma célula. Clamps em `rows_-1`/`cols_-1` evitam cursor fora da grade. `J` com parâmetro 2 limpa toda a surface — padrão “erase display”.

## 4. Reescreva `feed` como máquina de estados

```cpp
for (unsigned char raw : bytes) {
    const char ch = static_cast<char>(raw);

    switch (state_) {
```

### Ground

```cpp
case State::Ground:
    if (raw == 0x1B) {
        state_ = State::Escape;
    } else if (ch == '\n') {
        row_ = std::min(rows_ - 1, row_ + 1);
    } else if (ch == '\r') {
        col_ = 0;
    } else if (ch >= 0x20 && ch != 0x7F) {
        put(ch);
    }
    break;
```

### Escape

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

### CSI

```cpp
case State::Csi:
    if (std::isdigit(raw)) {
        param_text_.push_back(ch);
    } else if (ch == ';') {
        // múltiplos parâmetros serão implementados depois;
        // por enquanto mantenha sincronização do parser.
    } else if (raw >= 0x40 && raw <= 0x7E) {
        handle_csi(ch);
        state_ = State::Ground;
        param_text_.clear();
    }
    break;
```

Feche `switch` e `for`.

### Por que funciona?
`state_` persiste entre chamadas de `feed` — essencial para sequências fragmentadas (`A\x1b` + `[2C` + `B`). ESC sem `[` volta a Ground (sequência desconhecida descartada). Em CSI, dígitos acumulam em `param_text_` até byte final na faixa `@`–`~`.

## 5. Teste que prova estado persistente entre feeds

```cpp
Terminal fragmented(8, 2);
fragmented.feed("A\x1b");
fragmented.feed("[2C");
fragmented.feed("B");
assert(fragmented.at(0, 0) == 'A');
assert(fragmented.at(0, 3) == 'B');
```

Depois do primeiro `feed`, o parser deve terminar em `State::Escape`, não resetar para Ground só porque a chamada acabou.

## 6. Teste de erase display

Envie texto e depois:

```text
ESC [ 2 J
```

Todas as células devem virar espaço e cursor voltar a `(0,0)`.

## 7. Execute

```bash
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

## 8. Debugging

- `B` cai em coluna 1 em vez de 3: verifique `param_text_` e `handle_csi('C')`;
- ESC aparece na tela: no Ground, teste `raw == 0x1B` antes de caractere imprimível;
- parser perde sequência entre feeds: `state_` não pode ser variável local;
- `CSI 2J` não limpa: `param_or(0)` precisa enxergar `"2"` antes de `param_text_.clear()`.

A solution correspondente está em `solutions/src/terminal.cpp`.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `TERM-CSI-01` — `starter/src/terminal.cpp` → `solutions/src/terminal.cpp`.
- `TERM-FEED-01` — `starter/src/terminal.cpp` → `solutions/src/terminal.cpp`.
## Relatório de resolução

### O que foi validado

- Todos os TODOs do `starter/` foram implementados na ordem sugerida.
- Testes com marcadores `PEDAGOGY-TEST` passaram na solution.
- O starter continua falhando nos pontos intencionais até o aluno completar cada ID.

### Armadilhas encontradas

- Leia mensagens de `assert` como contrato, não como bug do teste.
- Compare sempre starter vs solution diff por arquivo.
- Documente no benchmark o que *não* foi medido (I/O, rede, GPU, VM).

**Saída esperada:** `ctest` passa; feed fragmentado `A\x1b` + `[2C` + `B` posiciona cursor corretamente.

### Próximo passo sugerido

Repita o módulo sem consultar a resolução, cronometrando apenas a fase de implementação. Depois leia `BENCHMARK_GUIADO.md` e registre suas observações na seção **Resultados observados**.
