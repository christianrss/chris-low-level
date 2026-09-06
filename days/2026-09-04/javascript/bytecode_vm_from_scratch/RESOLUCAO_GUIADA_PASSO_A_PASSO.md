# RESOLUÇÃO GUIADA — JavaScript / Bytecode VM from scratch

## Mapa exato starter → resolução

| TODO ID | Starter | Área |
|---------|---------|------|
| `D2-JS-LEX-NUMBER` | `starter/src/chris_js.cpp` | `Lexer::next` dígitos |
| `D2-JS-LEX-IDENT` | `starter/src/chris_js.cpp` | keywords `let`/`print` |
| `D2-JS-STMT-LET` | `starter/src/chris_js.cpp` | `Compiler::statement` Let |
| `D2-JS-STMT-PRINT` | `starter/src/chris_js.cpp` | `Compiler::statement` Print |
| `D2-JS-PREC-ADD` | `starter/src/chris_js.cpp` | `Compiler::expression` |
| `D2-JS-PREC-MUL` | `starter/src/chris_js.cpp` | `Compiler::term` |
| `D2-JS-VM-ADD` | `starter/src/chris_js.cpp` | `run` / `Op::Add` |

Cada ID: `TODO` / `PEDAGOGY-SOLUTION` / `PEDAGOGY-TEST`. Starter incompleto nesses sete pontos.

> Trabalhe em `days/2026-09-04/javascript/bytecode_vm_from_scratch/starter/`.  
> Traces longos e sessão de debug: `RESOLUCAO_APENDICE.md`.

API já pronta (não reescreva): `expect`, `emit`, `factor`, `name_index`, `Op::Sub`/`Mul`/`StoreGlobal`/`Print`.

---

## Baseline

```bash
cmake -S starter -B starter/build && cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Build OK; testes falham por comportamento incompleto (não por CMake).

---

## Camada 1 — Lexer

### Exercício Fácil A — `D2-JS-LEX-NUMBER`

#### 1. O problema

O starter já avança `pos_` pelos dígitos, mas devolve `value=0`:

```cpp
return {Kind::Number, source_.substr(start, pos_ - start), 0};
```

Literais `10`/`20` viram constantes 0 → programa demo imprime lixo.

#### 2. O algoritmo

Antes do loop (ou no lugar do loop+return), acumule:

```text
value = 0
enquanto dígito: value = value*10 + (c-'0'); ++pos_
return Number(text, value)
```

#### 3. Escreva o código

Substitua o TODO (mantenha `start`; o loop stub pode ser substituído pelo bloco completo):

```cpp
std::int64_t value = 0;
while (pos_ < source_.size() &&
       std::isdigit(static_cast<unsigned char>(source_[pos_]))) {
  value = value * 10 + (source_[pos_] - '0');
  ++pos_;
}
return {Kind::Number, source_.substr(start, pos_ - start), value};
```

#### 4. Por que funciona

Horner decimal. Cast `unsigned char` evita UB de `isdigit` com `char` negativo. Trace `123`: `0→1→12→123`.

#### 5. Verifique

Ainda vermelho (idents/VM); confira mentalmente que `10` não fica 0.

---

### Exercício Fácil B — `D2-JS-LEX-IDENT`

#### 1. O problema

Após montar `text`, o starter sempre devolve `Identifier`. `let`/`print` nunca viram `Kind::Let`/`Print` → `statement()` não entra nos branches.

#### 2. O algoritmo

```text
se text == "let" → Kind::Let
se text == "print" → Kind::Print
senão → Identifier
```

#### 3. Escreva o código

```cpp
if (text == "let") {
  return {Kind::Let, text};
}
if (text == "print") {
  return {Kind::Print, text};
}
return {Kind::Identifier, text};
```

#### 4. Por que funciona

Keywords reservadas no lexer — o parser só olha `Kind`, não a string. `letter` permanece Identifier.

#### 5. Verifique

Tokenize `let x = 1;` → Let, Ident, Equal, Number, Semicolon.

---

## Camada 2 — Statements

O starter, após `expect(Kind::Equal)` / `expect(Kind::LParen)`, **lança** TODO. Você completa expressão + pontuação + emit.

### Exercício Médio A — `D2-JS-STMT-LET`

#### 1. O problema

`idx` já calculado; falta compilar RHS, consumir `;`, emitir `StoreGlobal`.

#### 2. O algoritmo

```text
expression()           # deixa valor na stack (em runtime)
expect(Semicolon)
emit(StoreGlobal, idx) # VM: pop → globals[idx]
return
```

#### 3. Escreva o código

```cpp
expression();
expect(Kind::Semicolon);
emit(Op::StoreGlobal, idx);
return;
```

#### 4. Por que funciona

Ordem do bytecode: primeiro a expressão (PushConst/Load…), depois Store. Se emitir Store antes, a stack estará vazia no runtime.

#### 5. Verifique

`let x = 10;` → constantes/globals coerentes no dump (ver apêndice).

---

### Exercício Médio B — `D2-JS-STMT-PRINT`

#### 1. O problema

Após `(`, falta expressão, `)`, `;`, `Print`.

#### 2. O algoritmo

```text
expression(); expect(RParen); expect(Semicolon); emit(Print); return
```

#### 3. Escreva o código

```cpp
expression();
expect(Kind::RParen);
expect(Kind::Semicolon);
emit(Op::Print);
return;
```

#### 4. Por que funciona

`Print` consome o topo. Expressão **antes** do opcode. Esquecer `)` dessincroniza o parser.

#### 5. Verifique

Compile `print(1);` — deve emitir PushConst + Print (+ Halt no fim do programa).

---

## Camada 3 — Precedência

Starters de `expression`/`term` só chamam o nível inferior uma vez — sem loops de operadores.

### Exercício Médio/Difícil A — `D2-JS-PREC-MUL`

#### 1. O problema

`term()` só faz `factor()` — `y * 2` vira só `y`.

#### 2. O algoritmo

```text
factor()
enquanto Star: advance; factor; emit Mul
```

#### 3. Escreva o código

```cpp
factor();
while (current_.kind == Kind::Star) {
  advance();
  factor();
  emit(Op::Mul);
}
```

#### 4. Por que funciona

Associatividade esquerda: `a*b*c` → Mul, Mul. Cada Mul consome dois valores já empilhados pelos factors.

#### 5. Verifique

`2*3*4` → três PushConst + dois Mul.

---

### Exercício Médio/Difícil B — `D2-JS-PREC-ADD`

#### 1. O problema

`expression()` só chama `term()` — `x + y` ignora o `+`.

#### 2. O algoritmo

```text
term()
enquanto Plus|Minus:
  kind = current; advance; term()
  emit Add ou Sub
```

#### 3. Escreva o código

```cpp
term();
while (current_.kind == Kind::Plus || current_.kind == Kind::Minus) {
  const auto kind = current_.kind;
  advance();
  term();
  emit(kind == Kind::Plus ? Op::Add : Op::Sub);
}
```

#### 4. Por que funciona

Cada operando é um `term` completo — portanto todos os `*` daquele operando já foram emitidos. Para `x + y * 2`, bytecode: Load x, Load y, Push 2, **Mul**, **Add**.

Armadilha: colocar `*` no loop de `expression` inverte a árvore.

#### 5. Verifique

Compare dumps de `x+y*2` vs `(x+y)*2` (apêndice).

---

## Camada 4 — VM

### Exercício Difícil — `D2-JS-VM-ADD`

#### 1. O problema

Starter faz `pop b`, `pop a`, mas empilha **só `a`** — descarte de `b`:

```cpp
stack.push_back(a);
(void)b;
```

Com `x=10`, `y*2=40`, Add deixa 10 no topo → print **10** em vez de **50**.

#### 2. O algoritmo

Mesma ordem de Sub/Mul já corretos: `push(a + b)`.

#### 3. Escreva o código

```cpp
stack.push_back(a + b);
```

(remova o `(void)b` e o push só de `a`).

#### 4. Por que funciona

Pilha: `[10, 40]` → pop b=40, pop a=10 → push 50. Ordem importa para Sub (`a-b`); para Add é comutativo em int, mas a disciplina é a mesma.

#### 5. Verifique

```bash
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
./starter/build/chris_js_cli   # esperado: 50
```

`chris-js tests passed`.

---

## Ordem de ataque se travar

1. Lexer (números + keywords) — senão o parser nem vê statements.  
2. Statements — senão não há Store/Print.  
3. Precedência Mul depois Add — senão árvore errada.  
4. VM Add — senão aritmética mentirosa.

Falhas “avançam” de camada: observe a mensagem mudar de unexpected token → stack → valor errado.

## Checkpoint no papel (obrigatório)

Antes de declarar vitória:

1. Tokenize `let x = 10;` — cinco tokens, Number com value **10**.  
2. Árvore de `x + y * 2` — `*` mais fundo que `+`.  
3. Stack imediatamente antes de `Add`: `[10, 40]` → depois `[50]`.  
4. Se o CLI imprimir `10`, o bug está no `Op::Add` (só empilha `a`), não na precedência.

## Debugging (resumo)

Breakpoints: `Lexer::next`, `statement`, `expression`/`term`, loop `run`.  
Se a estrutura parecer `(10+20)*2`, a fronteira expression/term está errada.  
Traces longos, dumps e contrastes com parênteses: **`RESOLUCAO_APENDICE.md`**.

## Mapa de consistência

Sete `PEDAGOGY-SOLUTION` em `solutions/src/chris_js.cpp`. Atenção: o gabarito pode marcar só o `emit` final em statements se `expression`/`expect` já estiverem acima do marcador — no **starter** você escreve o bloco completo do TODO.

## Relatório

| ID | Aceite |
|----|--------|
| LEX-NUMBER/IDENT | valor Int64; keywords |
| STMT-LET/PRINT | StoreGlobal / Print após expressão |
| PREC-ADD/MUL | Mul antes de Add em `x+y*2` |
| VM-ADD | demo imprime `50` |

Aceite: `chris-js tests passed` + CLI `50`. Registre no benchmark o tempo Release do programa demo.

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Paper-trace feito? Sim/Não
- Portei para projects/? Sim/Não — evidência: ___
