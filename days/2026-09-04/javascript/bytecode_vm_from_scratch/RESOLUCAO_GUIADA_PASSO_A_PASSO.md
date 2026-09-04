# Resolução guiada passo a passo

## 1. Fácil — lexer
Abra `starter/src/chris_js.cpp` e localize `Lexer::next()`.

Para inteiros, acumule dígitos:
```cpp
std::int64_t value = 0;
while (pos_ < source_.size() && std::isdigit(static_cast<unsigned char>(source_[pos_]))) {
    value = value * 10 + (source_[pos_] - '0');
    ++pos_;
}
```
Para identifiers, reconheça `let` e `print` como keywords; os demais viram `Identifier`.

## 2. Médio — precedência
Localize `expression`, `term`, `factor`.

`expression`:
```cpp
term();
while (current_.kind == Kind::Plus || current_.kind == Kind::Minus) {
    auto kind = current_.kind;
    advance();
    term();
    emit(kind == Kind::Plus ? Op::Add : Op::Sub);
}
```
`term` deve consumir `factor` e emitir `Mul` para `*`. Assim multiplicação entra no bytecode antes da soma.

## 3. Médio — statements
Para `let name = expression;`, compile a expressão e depois:
```cpp
emit(Op::StoreGlobal, idx);
```
Para `print(expression);`:
```cpp
emit(Op::Print);
```

## 4. Difícil — VM
Localize `run`. Para uma operação binária:
```cpp
case Op::Add: {
    auto b = pop();
    auto a = pop();
    stack.push_back(a + b);
    break;
}
```
Para `Sub`, preserve a ordem `a-b`. Para `StoreGlobal`, `pop()` o valor e grave no índice do operand.

## 5. Build/test
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```
Esperado:
```text
chris-js tests passed
100% tests passed
```

## 6. Execute linguagem própria
```bash
./starter/build/chris_js_cli
```
Esperado:
```text
50
```

## Debugging
Coloque breakpoint no loop da VM e acompanhe `ip`, `ins.op`, `stack` e `globals`. Para `x + y * 2`, antes do `Add` a stack deve conter `[10,40]`. Se contiver `[30,2]`, sua precedência está errada.
