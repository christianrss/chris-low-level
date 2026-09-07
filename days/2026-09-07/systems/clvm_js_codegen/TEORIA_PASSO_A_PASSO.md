# Teoria passo a passo — CLVM JS codegen (N1)

## 1. O que este lab pede

Você implementa o **codegen** que transforma um subconjunto de JavaScript em assembly CLVM. O lexer e o parser já estão prontos; sua tarefa é percorrer a AST e emitir linhas `.asm` que a VM do Dia 04 executa.

TODOs deste módulo:

| ID | O quê |
|----|--------|
| `CLVM-JS-LET-01` | `let` / `const` → avaliar expr + `STORE` |
| `CLVM-JS-WHILE-01` | `while` → labels + `JZ` / `JMP` |
| `CLVM-JS-CALL-01` | argumentos + `CALL` + prólogo `STORE` dos parâmetros |

### Por que não colocar codegen no Dia 01?

A ISA original não tinha `CALL`, `LOAD` nem `STORE`. Forçar codegen lá misturaria dois objetivos pedagógicos: aprender a VM mínima e aprender a compilar HLL. Este lab assume que você já domina a ISA estendida do Dia 04.

## 2. Pipeline completo

```text
.js → lexer → parser → AST → codegen (VOCÊ) → .asm → assemble.py → .clvm → VM
```

| Etapa | Entrada | Saída |
|-------|---------|-------|
| lexer | texto fonte | tokens |
| parser | tokens | `Program` com `main` + `functions` |
| codegen | AST | lista de strings asm |
| assemble | asm | bytes + checksum FNV-1a32 |
| VM | `.clvm` | stdout / HALT |

O arquivo `starter/js2clvm/codegen.py` é o único que você edita. `parser.py`, `lexer.py`, `assemble.py` e `verify_clvm.py` permanecem intactos.

## 3. Frames estáticos e endereços de slot

Antes de emitir qualquer instrução, `Codegen.generate()` calcula quantos slots cada função precisa e atribui uma **base** de memória:

```text
slot i  →  endereço byte = base + i * 4
```

| slot | base=0 | base=8 |
|------|--------|--------|
| 0 | 0 | 8 |
| 1 | 4 | 12 |
| 2 | 8 | 16 |

`_Frame.alloc(name)` reserva o próximo índice local e devolve o endereço absoluto. `_Frame.addr(name)` recupera o endereço de uma variável já alocada. `reset_alloc()` zera o mapa de nomes no início de cada função — parâmetros e `let` internos competem pelos mesmos índices locais.

### Por que pré-alocar slots em vez de alocar sob demanda global?

A memória da VM tem 256 bytes (64 slots de 4 B). O codegen precisa saber **antes** de emitir se o programa cabe. `_count_lets()` percorre o corpo e conta quantos `let` existem (incluindo dentro de `if`/`while`); soma-se `len(params)` para cada função. Se `slot_cursor > max_slots`, o compilador rejeita com `CodegenError`.

## 4. Convenção STORE — CLVM-JS-LET-01

`let x = expr` segue o mesmo contrato de `mem_demo.asm` do Dia 04:

```text
1. avaliar expr  →  valor no topo da pilha de dados
2. alloc(x)      →  endereço absoluto do slot
3. PUSH addr
4. STORE         →  pop addr, pop value, grava LE32 em mem[addr]
```

Ordem na pilha no momento do `STORE`: **valor embaixo, endereço no topo**. O opcode consome endereço primeiro, depois valor.

`AssignStmt` já faz isso para reatribuições (`i = i + 1` em `loop.js`). `LetStmt` é idêntico, mas chama `alloc` em vez de `addr`, porque o nome ainda não existe no frame.

### Por que reutilizar LOAD/STORE e não “registradores virtuais”?

A VM educacional já expõe memória linear com bounds check. Inventar um segundo modelo (registradores, frame pointer dinâmico) duplicaria conceitos que o Dia 04 consolidou. O codegen só precisa traduzir nomes → endereços.

## 5. while — CLVM-JS-WHILE-01

Um `while (cond) { body }` vira um laço com dois labels:

```text
_head:
    <emitir cond>       # 0 ou 1 no topo
    JZ _end             # sai se cond == 0
    <emitir body>
    JMP _head
_end:
```

`IfStmt` no starter já usa `JZ` + `JMP` para ramificação. O `while` é a variante em que o salto condicional aponta para **fora** do laço e o salto incondicional volta ao cabeçalho.

### Por que JZ e não JNZ?

A condição de comparação (`i < 4`) já produz 1 quando verdadeira e 0 quando falsa — mesmo contrato de `LT` no Dia 04. `JZ` sai quando a condição é falsa; não é preciso inverter com `PUSH 0; EQ` antes do salto.

Paper-trace de `loop.js` (primeiras iterações):

| passo | mem[0] (i) | stack (topo→) | stdout |
|-------|------------|---------------|--------|
| let i=0 | 0 | | |
| cond i<4 | 0 | 1 | |
| print(i) | 0 | | 0 |
| i=i+1 | 1 | | |
| cond i<4 | 1 | 1 | |
| print(i) | 1 | | 1 |
| … | … | … | 0 1 2 3 |

## 6. Chamadas de função — CLVM-JS-CALL-01

### Lado do caller (`Call` em `_expr`)

```text
1. verificar que callee existe em fn_names
2. verificar arity: len(args) == len(fn.params)
3. para cada arg em ordem textual: _expr(arg)   # empilha arg0, depois arg1, …
4. emitir CALL <nome>
```

O último argumento avaliado fica no **topo** da pilha. Isso espelha `add2.asm`: `PUSH 3; PUSH 5; CALL add2` deixa `5` no topo.

### Lado do callee (prólogo em `generate`)

Ao entrar na função, a pilha contém os argumentos (último no topo). O prólogo consome cada um com `STORE`:

```text
for name in reversed(fn.params):
    addr = alloc(name)
    PUSH addr
    STORE
```

`reversed` garante que o primeiro `STORE` pegue o último parâmetro da lista textual — que é o que está no topo da pilha.

Exemplo `function add(a, b) { return a + b; }` chamada como `add(3, 5)`:

| momento | pilha (topo→) | ação |
|---------|---------------|------|
| após PUSH 3, PUSH 5 | 5, 3 | |
| CALL add | (call stack + PC) | pilha de dados: 5, 3 |
| STORE b (reversed[0]) | 3 | b←5 em mem |
| STORE a (reversed[1]) | | a←3 em mem |
| return a+b | | resultado 8 no topo |
| RET | | caller recebe 8 |

### Por que verificar arity no codegen?

A VM não conhece assinaturas. Se o caller empilhar argumentos a mais ou a menos, o prólogo `STORE` consumirá valores errados ou deixará lixo na pilha. Erro em compile-time é mais barato que debug na VM.

## 7. Estrutura de `generate()` — ordem de emissão

```text
1. calcular frames e limites de slots
2. emitir corpo de __main__
3. HALT
4. para cada function:
       label <nome>:
       prólogo params (CALL-01)
       corpo (até primeiro return explícito)
       se sem return: PUSH 0; RET
```

`ReturnStmt` emite `_expr` + `RET`. Funções sem `return` explícito recebem `PUSH 0; RET` como valor padrão.

## 8. Operadores e builtins já implementados

O starter já cobre:

- literais `NumberLit` → `PUSH`
- variáveis `Name` → `PUSH addr; LOAD`
- binários aritméticos e comparações em `_binop`
- `if` / `else` com labels únicos via `_label()`
- `print(expr)` via `PrintStmt` (não é `Call("print")`)
- `return expr` via `ReturnStmt`

Não reimplemente o que não está marcado com `TODO`.

## 9. Limites e erros do compilador

| Limite | Valor | Efeito |
|--------|-------|--------|
| memória VM | 256 B | 64 slots |
| inteiros | i32 | literais fora de range → `CodegenError` |
| recursão | não suportada | mesma função na call stack corrompe convenção |
| `print` como nome de função | proibido | conflito com builtin |

Erros comuns no codegen:

| Sintoma | Causa provável |
|---------|----------------|
| `undefined variable` | `let` sem `alloc` ou ordem errada |
| asm sem `STORE` em `add.js` | LET-01 incompleto |
| loop infinito na VM | `while` sem `JZ` para sair |
| `CALL add` ausente | CALL-01 incompleto |
| valor errado em `add(3,5)` | prólogo sem `reversed` |

## 10. Ligação com dias anteriores

| Dia | Artefato reutilizado |
|-----|---------------------|
| 01 `clvm` | formato `.clvm`, FNV checksum, PUSH/ADD/PRINT/HALT |
| 04 `clvm_extended` | CALL/RET, LOAD/STORE, LT/EQ, JZ/JMP |
| capstone `chris-vm` | mesmo pipeline; `projects/chris-vm/tools/js2clvm/codegen.py` é a versão madura |

O `.asm` gerado aqui é a mesma IR que `assemble.py` do Dia 04 monta. Rodar `verify_clvm.py` confirma header + checksum antes de executar na VM.

## 11. Como depurar sem executar a VM

1. `python -m js2clvm examples/js/add.js` — imprime asm no stdout.
2. Inspecione se `STORE` aparece após cada `let`.
3. Em `loop.js`, confirme par `_whileN:` / `_wendM:` com `JZ` saindo e `JMP` voltando.
4. Em `fn_add.js`, confirme `CALL add` e label `add:` com dois `STORE` no prólogo.
5. Monte `.clvm` com `assemble.py` e passe por `verify_clvm.py`.

### Por que inspecionar asm antes da VM?

O codegen é a camada que você controla. Se o asm está correto e a VM falha, o bug está no runtime ou no assembler — não no seu lowering. Separar as camadas acelera o diagnóstico.

## 12. Goldens de aceite

| Exemplo | Entrada | stdout esperado | asm característico |
|---------|---------|-----------------|-------------------|
| `add.js` | `(7*5)+3` | 38 | `STORE`, `MUL`, `ADD` |
| `loop.js` | `while i<4` | 0 1 2 3 | `JZ`, `JMP`, ciclo de labels |
| `fn_add.js` | `add(3,5)` | 8 | `CALL add`, prólogo com `STORE` |

## 13. Checklist mental antes de codar

1. `STORE`: valor embaixo, endereço no topo?
2. `alloc` só em `let` e no prólogo de params — `addr` em leituras e reatribuições?
3. Labels de `while` são únicos (`_label` incrementa contador)?
4. `JZ` consome a condição da pilha?
5. Args empilhados na ordem textual; prólogo usa `reversed`?
6. `main` termina em `HALT`; funções terminam em `RET`?

## 14. Próximo lab

`clvm_bytecode_verifier` (N2) adiciona verificação estática do bytecode. Strings e heap entram em `clvm_v2_strings` (N4). Este lab N1 cobre apenas inteiros e frames estáticos.

## 15. Síntese

Compilar este subconjunto JS = aplicar três convenções que você já viu em assembly manual:

1. **Variáveis** = slots de memória com `LOAD`/`STORE`.
2. **Laços** = saltos condicionais + incondicionais.
3. **Funções** = caller empilha args + `CALL`; callee faz prólogo `STORE` + `RET`.

Você não inventa uma nova ISA — traduz estruturas de alto nível para os opcodes dos dias anteriores.
