# Teoria — CLVM JS codegen (N1)

## 1. Por que este lab existe

No chris-vm o `js2clvm` já funciona. Aqui você **reconstrói o codegen** com a mão: o salto pedagógico é “sei baixar AST → opcodes”, não só rodar o CLI.

### Por que não stubs no Dia 01?

A ISA do Dia 01 não tem CALL/LOAD/STORE. Colocar codegen lá atrapalharia exercícios já resolvidos e forçaria opcodes cedo demais.

## 2. O que não muda

- Formato CLVM **v1** (Dia 01)
- ISA estendida CALL/LOAD/STORE (Dia 04)
- Lexer/parser deste lab (já fornecidos)

## 3. Pipeline

```text
.js → lexer → parser → AST → codegen (VOCÊ) → .asm → assemble.py → .clvm
```

| Etapa | Artefato |
|-------|----------|
| lexer | tokens |
| parser | AST |
| codegen | linhas asm |
| assemble | bytes + FNV |

## 4. Locais = memória linear

`let x = 7` aloca slot de 4 bytes, avalia a expressão, `PUSH addr`, `STORE`.

### Por que STORE e não “registradores virtuais”?

A VM educacional já tem LOAD/STORE (Dia 04). Reusar a ISA evita inventar frame pointer no v1.

## 5. while = saltos

```text
head:  <cond>  JZ end  <body>  JMP head  end:
```

## 6. function = CALL/RET + prólogo

Caller empurra args. Callee faz `STORE` de cada param (`reversed`).

### Por que reversed?

Pilha: último arg no topo — o primeiro `STORE` do prólogo consome o último parâmetro.

## 7. Limites

256 B mem → 64 slots; sem recursão na mesma função; sem strings (N4).

## 8. Ligação Dia 01

O `.asm` é a mesma IR. Checksum FNV no `assemble.py`.

## 9. Ligação Dia 04

Sem STORE/CALL o codegen de let/function não existe.

## 10. Capstone

Compare com `projects/chris-vm/tools/js2clvm/codegen.py`.

## 11. Erros comuns

- Esquecer STORE após let
- Ordem dos params
- Labels duplicados

## 12. Checklist mental

1. STORE: value embaixo, addr no topo?
2. JZ consome a condição?
3. CALL não remove args sozinho?
4. Main termina em HALT?

## 13. Como saber se está certo

Goldens: add→38, loop→0..3, fn_add→8.

## 14. Síntese

Compilar = convenções → opcodes.

## 15. Próximo lab

N2 verifier.

## 16. Papel do assembler

Dois passes de labels; codegen só emite nomes.

## 17. Por que asm no meio

Diff legível; `--emit-clvm` é atalho do capstone.

## 18. chris-js

Opcodes diferentes — não misture.

## 19. Frames estáticos

Bases calculadas antes de emitir.

## 20. print builtin

`PrintStmt`, não `Call("print")`.

## 21. return implícito

`PUSH 0; RET` se faltar return.

## 22. Como depurar

dump-asm, verify, disasm, clvm --trace.

## 23. Portfólio

Relatório com evidência do integration_test.

## 24. Uma frase

Você traduz HLL na ISA de pilha dos dias anteriores.

## 25. Offset mental do slot

| slot i | endereço byte |
|--------|---------------|
| 0 | base+0 |
| 1 | base+4 |
| 2 | base+8 |

## 26–30. Reforço

Leia `add2.asm` antes do CALL TODO. Paper-trace de `let a=1; print(a)`. Não edite Dia 01. Use solutions só depois de tentar. Rode starter esperando FAIL. Celebre PASS no solutions.
