# Teoria passo a passo — chris-vm (até JS → CLVM)

Este capstone fecha a trilha **3a** ([`docs/LEARNING_PATHS.md`](../../docs/LEARNING_PATHS.md)): Dia 01 construiu formato + VM; Dia 04 acrescentou CALL/mem/cmp; aqui você **lê e opera** o frontend que emite o mesmo bytecode.

## 1. De onde você veio

| Lab | O que você já sabe |
|-----|-------------------|
| Dia 01 `systems/clvm` | Header 16 B, FNV-1a, assembler, stack, JMP/JZ |
| Dia 04 `clvm_extended` | CALL/RET, LOAD/STORE (256 B), EQ/LT/JNZ |

Sem isso, o compilador JS não tem para onde baixar.

## 2. Arquitetura do capstone

```text
.js subset  →  js2clvm (lexer → parser → AST → codegen)
                 ↓
               .asm (IR legível)
                 ↓
            assemble.py → .clvm
                 ↓
         clvm_parse (C) → main.cpp (VM)
```

Atalho: `--emit-clvm` monta o `.clvm` sem gravar `.asm` no disco (mesmo `assemble.assemble` por baixo).

## 3. Por que um subset de JavaScript?

Objetivo pedagógico: ver **uma** linguagem de alto nível virar os opcodes que você implementou — não clonar o V8.

Inclui: `let`/`const`, aritmética, `if`/`while`, `function`/`return`, `print(n)`.

Não inclui: strings, objetos, arrays, closures, GC, `typeof`. Detalhe: [`docs/JS_SUBSET.md`](docs/JS_SUBSET.md).

## 4. Mapeamento mental (JS → ISA)

| Conceito JS | Mecanismo CLVM |
|-------------|----------------|
| literal | `PUSH` |
| `+ - * /` | `ADD`…`DIV` |
| local | `STORE` / `LOAD` em slot de 4 B |
| `if` / `while` | labels + `JZ` / `JMP` (+ `EQ`/`LT`) |
| chamada | args na pilha + `CALL` / `RET` |
| `print` | `PRINT` |
| fim do main | `HALT` |

## 5. Frames estáticos (limite didático)

Cada função (e o main) recebe uma **base fixa** na mem 256 B. Locais = `base + índice * 4`.

- Máx. 64 slots (`256/4`).
- Chamadas entre funções **diferentes** OK se o total de slots couber.
- Recursão profunda na **mesma** função não é suportada no v1 (precisaria de frame pointer dinâmico / nova ISA).

A VM ainda limita call stack (256), data stack (1024) e passos (1e6).

## 6. Pipeline interno do `js2clvm`

1. **Lexer** — tokens (`let`, números, `==`, `{`, …).
2. **Parser** — AST (`LetStmt`, `WhileStmt`, `Function`, …).
3. **Codegen** — percorre AST, emite linhas asm; aloca slots; gera labels `_while1`, etc.
4. **Assembler** — resolve labels → bytes + header FNV.

## 7. Ferramentas de inspeção

- `disasm_clvm.py` — volta do binário para mnemônicos (confira o que o codegen inventou).
- `verify_clvm.py` — magic/checksum + walk + underflow conservador na pilha.

## 8. Trilha paralela (chris-js)

`projects/chris-js` também compila um JS minúsculo, mas para **outra** ISA in-memory. Não compartilham bytecode. Síntese: o que é comum (pilha, dispatch) vs o que é formato (CLVM file).

## 9. Como saber se está no objetivo

```powershell
$env:PYTHONPATH = "tools"
python -m js2clvm examples/js/add.js --emit-clvm -o out.clvm
# clvm.exe out.clvm  →  38
ctest --test-dir build_ci -C Release   # inclui goldens JS
```

Goldens: `add.js` → `38`; `loop.js` → `0\n1\n2\n3`; `fn_add.js` → `8`.

## 10. Próximo passo de estudo

Abra [`RESOLUCAO_GUIADA_PASSO_A_PASSO.md`](RESOLUCAO_GUIADA_PASSO_A_PASSO.md) e siga as seções **Onde colocar** — é leitura guiada do código já existente, na ordem do pipeline.
