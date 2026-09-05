# Teoria passo a passo — CLVM: formato binário, assembler, loader e VM

## 1. O que estamos construindo

Uma máquina virtual educacional com arquivo `.clvm`, assembler Python, loader C e interpreter C++ — o mesmo ciclo fetch/decode/execute de ISAs reais, em escala reduzida.

## 2. Por que VM antes de emulador completo

Reúne: endianness, checksum, validação de header, bytecode, stack machine, saltos relativos e testes de integração — sem a superfície de x86.

## 3. Header de 16 bytes (tabela de offsets)

```text
offset | tamanho | campo
-------|---------|--------
0x00   | 4       | magic "CLVM"
0x04   | 1       | version
0x05   | 1       | flags (deve ser 0)
0x06   | 2       | entry (u16 LE)
0x08   | 4       | code_size (u32 LE)
0x0C   | 4       | checksum FNV-1a do bytecode
```

Exemplo: `code_size=10`, checksum calculado sobre bytes `[0..9]` do payload.

## 4. Fluxo interno

```text
.asm -> assemble.py -> .clvm
                         |
                    clvm_loader.c (valida header + checksum)
                         |
                    main.cpp VM (PC, stack, opcodes)
```

## 5. Stack machine — exemplo numérico

Programa `7 + 5`:

```text
PUSH 7    stack [7]
PUSH 5    stack [7, 5]
ADD       stack [12]
PRINT     stdout: 12
HALT
```

`countdown.asm` usa `JMP`/`JZ` com offset i16 relativo ao PC após o operando.

## 6. FNV-1a 32-bit (CLVM-PY-FNV-01 / CLVM-C-FNV-01)

```text
hash = 0x811C9DC5
para cada byte b:
  hash = (hash XOR b) * 16777619  (mod 2^32)
```

Alterar um byte do código → checksum mismatch → loader rejeita (`CLVM-C-HEADER-01`).

## 7. Saltos (CLVM-VM-JUMP-01)

```text
dest = PC_after_operand + signed_offset_i16
```

Destino fora de `[0, code_size)` deve falhar.

## 8. Aritmética (CLVM-VM-ARITH-01)

`ADD/SUB/MUL/DIV` consomem dois operandos da stack; `DIV` por zero é erro; `DUP` duplica topo; `PRINT` remove e imprime.

## 9. Labels (CLVM-ASM-LABELS-01)

Assembler em duas passagens:

1. coletar endereços de labels;
2. emitir bytecode resolvendo `JMP label` / `JZ label`.

## 10. Invariantes

- `flags == 0`, `entry < code_size`, checksum confere.
- Stack não underflow em operações binárias.
- PC sempre dentro do bytecode durante execução.
- Mesmo FNV em Python e C (bit a bit).

## 11. Complexidade

- Assemble: O(n) linhas + O(n) bytes emitidos.
- Load/validate: O(code_size).
- Execute: O(instruções até HALT ou limite).

## 12. Bugs comuns

- FNV com overflow errado (usar `& 0xFFFFFFFF` em Python).
- Confundir entry absoluto com offset de arquivo (entry é offset no bytecode).
- JMP relativo calculado do PC errado.
- `code_size` do header maior que buffer real.
- Labels forward reference não resolvidas na passagem 1.

## 13. Comparação com produção

| CLVM | JVM / WASM / Lua VM |
|------|---------------------|
| header 16 B | tabelas extensas |
| stack ops | stack ou register |
| FNV toy | SHA/signatures |
| inteiros i32 | tipos ricos, GC |

O pipeline assembler→loader→interpreter é o mesmo padrão industrial.

## 14. Passo a passo guiado

1. FNV em `assemble.py` e `clvm_loader.c`.
2. Header validation (`CLVM-C-HEADER-01`).
3. VM aritmética + saltos em `main.cpp`.
4. Labels em assembler.
5. `integration_test.py` com `arithmetic.asm` → imprime `38`.

## 15. Como saber se está correto

`arithmetic` → `38`; `countdown` → `3 2 1 0`; checksum corrupto rejeitado; salto inválido rejeitado.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
