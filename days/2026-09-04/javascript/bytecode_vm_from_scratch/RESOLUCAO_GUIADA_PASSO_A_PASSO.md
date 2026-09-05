# Resolução guiada passo a passo — JavaScript-like bytecode VM do zero

## Mapa exato starter → resolução
- `D2-JS-LEX-NUMBER` → `starter/src/chris_js.cpp` → `Lexer::next`, bloco de números.
- `D2-JS-LEX-IDENT` → `starter/src/chris_js.cpp` → `Lexer::next`, bloco de identificadores/keywords.
- `D2-JS-STMT-LET` → `starter/src/chris_js.cpp` → `Compiler::statement`, branch `Kind::Let`.
- `D2-JS-STMT-PRINT` → `starter/src/chris_js.cpp` → `Compiler::statement`, branch `Kind::Print`.
- `D2-JS-PREC-ADD` → `starter/src/chris_js.cpp` → `Compiler::expression`.
- `D2-JS-PREC-MUL` → `starter/src/chris_js.cpp` → `Compiler::term`.
- `D2-JS-VM-ADD` → `starter/src/chris_js.cpp` → `run`, `case Op::Add`.

Agora o starter é realmente incompleto nesses sete pontos; nenhuma etapa abaixo descreve código que já veio pronto sem avisar.

## 0. Baseline
A partir deste módulo:
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```
O **build deve passar**. O teste deve falhar por comportamento incompleto do lexer/compiler/VM. Isso comprova que o projeto está montado e que o defeito é pedagógico, não de infraestrutura.

## 1. Fácil — `D2-JS-LEX-NUMBER`
Abra `starter/src/chris_js.cpp` e localize `Lexer::next()`. No branch `std::isdigit`, mantenha `start` e substitua o TODO por:
```cpp
std::int64_t value = 0;
while (pos_ < source_.size() &&
       std::isdigit(static_cast<unsigned char>(source_[pos_]))) {
  value = value * 10 + (source_[pos_] - '0');
  ++pos_;
}
return {Kind::Number, source_.substr(start, pos_ - start), value};
```
Trace manual para `123`: `0 → 1 → 12 → 123`. O cast para `unsigned char` antes de `std::isdigit` evita uso indefinido para `char` negativo.

## 2. Fácil — `D2-JS-LEX-IDENT`
No mesmo `Lexer::next()`, depois de construir `text`, substitua o TODO por:
```cpp
if (text == "let") {
  return {Kind::Let, text};
}
if (text == "print") {
  return {Kind::Print, text};
}
return {Kind::Identifier, text};
```
Sem isso, `let` vira um identificador comum e `Compiler::statement()` não consegue iniciar uma declaração.

## 3. Médio — statements reais
### `D2-JS-STMT-LET`
Em `Compiler::statement()`, branch `Kind::Let`, depois de `expect(Kind::Equal)`, digite:
```cpp
expression();
expect(Kind::Semicolon);
emit(Op::StoreGlobal, idx);
return;
```
Fluxo: expressão deixa um valor na stack da VM; `StoreGlobal` consumirá esse valor no runtime.

### `D2-JS-STMT-PRINT`
No branch `Kind::Print`, depois de `expect(Kind::LParen)`, digite:
```cpp
expression();
expect(Kind::RParen);
expect(Kind::Semicolon);
emit(Op::Print);
return;
```
A expressão precisa ser compilada **antes** do `Print`, para que o bytecode deixe o valor no topo da stack.

## 4. Médio/Difícil — precedência
### `D2-JS-PREC-MUL`
Em `Compiler::term()`:
```cpp
factor();
while (current_.kind == Kind::Star) {
  advance();
  factor();
  emit(Op::Mul);
}
```
### `D2-JS-PREC-ADD`
Em `Compiler::expression()`:
```cpp
term();
while (current_.kind == Kind::Plus || current_.kind == Kind::Minus) {
  const auto kind = current_.kind;
  advance();
  term();
  emit(kind == Kind::Plus ? Op::Add : Op::Sub);
}
```
Por que funciona: `expression()` só trata `+/-`, mas cada operando é um `term()` que consome todos os `*` antes. Para `x + y * 2`, `Mul` aparece no bytecode antes de `Add`.

## 5. Difícil — `D2-JS-VM-ADD`
Em `run()`, `case Op::Add`, preserve a ordem dos pops e empilhe o resultado:
```cpp
const auto b = pop();
const auto a = pop();
stack.push_back(a + b);
break;
```
Para `Sub`, a ordem importa ainda mais: deve ser `a - b`, não `b - a`.

## 6. Teste depois de cada grupo
Depois de lexer (1–2), statements (3), precedência (4) e VM (5), repita:
```bash
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```
É normal continuar vermelho até todos os TODOs exigidos pelo teste principal estarem completos. O ponto é observar **como a falha avança**: lexer → parser/compiler → VM.

Ao final, esperado:
```text
chris-js tests passed
100% tests passed
```

## 7. Execute a linguagem própria
```bash
./starter/build/chris_js_cli
```
Esperado no programa demo:
```text
50
```

## Debugging
Coloque breakpoint em `Lexer::next`, `Compiler::statement`, `Compiler::expression`, `Compiler::term` e no loop de `run`.

Para `x + y * 2`, acompanhe `current_.kind`, `program_.code`, `ip`, `ins.op`, `stack` e `globals`. Imediatamente antes de `Op::Add`, a stack deve conter os valores equivalentes a `[10,40]`. Se você vir uma estrutura equivalente a `(10+20)*2`, a fronteira entre `expression()` e `term()` está errada.

## Solução final comentada
Somente depois dos testes verdes, compare `starter/src/chris_js.cpp` com `solutions/src/chris_js.cpp`. Procure os sete marcadores `PEDAGOGY-SOLUTION`. Cada um deve corresponder exatamente a um TODO que você resolveu; o gabarito não contém etapas mágicas adicionais.
