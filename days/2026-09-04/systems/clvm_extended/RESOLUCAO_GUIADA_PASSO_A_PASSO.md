# RESOLUÇÃO GUIADA — CLVM extended

## Mapa exato starter → resolução

| TODO ID | Starter | Função / foco |
|---------|---------|---------------|
| `CLVM-EXT-01` | `starter/tools/assemble.py` | OPS + BRANCH (CALL/JNZ/…) |
| `CLVM-EXT-02` | `starter/src/main.cpp` | `Op::Call` / `Op::Ret` |
| `CLVM-EXT-03` | `starter/src/main.cpp` | `mem_in_bounds` / Load / Store |
| `CLVM-EXT-04` | `starter/src/main.cpp` | DROP/SWAP/EQ/LT/JNZ + `max_loop.asm` |

> Trabalhe em `days/2026-09-04/systems/clvm_extended/starter/`. Compare `solutions/` só depois.

---

## Baseline

```powershell
cmake -S starter -B starter/build_ci -A x64
cmake --build starter/build_ci --config Release
ctest --test-dir starter/build_ci -C Release --output-on-failure
```

Esperado: build OK, teste FAIL (assembler ainda não conhece CALL). Isso prova CMake saudável.

Ordem: EXT-01 → EXT-02 → EXT-03 → EXT-04.

---

## CLVM-EXT-01 — assembler

### 1. O problema

`add2.asm` / `max_loop.asm` levantam `instrução desconhecida`.

### 2. O algoritmo

Preencher `OPS` e `BRANCH` com os hex de `docs/FORMAT.md`. Branches medem 3 bytes (opcode + i16).

### 3. Escreva o código

```python
OPS = { ..., "RET": 0x0C, "LOAD": 0x0D, "STORE": 0x0E,
        "DROP": 0x0F, "SWAP": 0x10, "EQ": 0x11, "LT": 0x12 }
BRANCH = { "JMP": 0x09, "JZ": 0x0A, "CALL": 0x0B, "JNZ": 0x13 }
```

### 4. Por que funciona

Dois passes: labels → PC, depois displacement = `label - (pc+3)`. Igual JMP do Dia 01.

### 5. Verifique

```powershell
python starter/tools/assemble.py starter/programs/add2.asm out.clvm
```

Saída esperada: linha `wrote ... checksum=...`.

---

## CLVM-EXT-02 — CALL/RET

### 1. O problema

`CALL not implemented` / `RET not implemented`.

### 2. O algoritmo

CALL: ler i16, avançar PC, push return-PC, jump. RET: pop ou `return stack underflow`.

### 3. Escreva o código

```cpp
pc += 2;
call_stack.push_back(pc);
if (!checked_jump(relative)) { /* erro */ }
```

### 4. Por que funciona

Return-PC é o endereço **após** o operando — mesmo contrato do assembler.

### 5. Verifique

`clvm add2.clvm` → stdout `8`. `bad_ret` → stderr com underflow. Debug: `--trace` e olhe `call_depth`.

---

## CLVM-EXT-03 — memória

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/main.cpp` |
| **Função / âncora** | comentário `TODO [CLVM-EXT-03]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [CLVM-EXT-03]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |

### 1. O problema

STORE/LOAD stubs; OOB não detectado.

### 2. O algoritmo

`addr >= 0 && addr + 4 <= 256`; STORE escreve LE32; LOAD lê LE32.

### 3. Escreva o código

```cpp
bool mem_in_bounds(std::int32_t addr) {
    return addr >= 0 && static_cast<std::size_t>(addr) + 4 <= kMemSize;
}
```

### 4. Por que funciona

i32 precisa de 4 bytes contíguos; `@254` estoura 256 → mensagem esperada `memory out of bounds`.

### 5. Verifique

`mem_demo` → `42`. `bad_mem` falha. Depure com PRINT intermediário se o valor lido for lixo.

---

## CLVM-EXT-04 — cmp / stack / loop

### 1. O problema

`extended opcode not implemented`; `max_loop` não roda.

### 2. O algoritmo

DROP pop; SWAP troca; EQ/LT empurram 0/1; JNZ salta se `cond != 0`.

### 3. Escreva o código

```cpp
if (lhs != 0 && !checked_jump(relative)) { /* erro */ }
```

### 4. Por que funciona

`while (i < 4)` vira `LT` + `JNZ`. SWAP/DROP/EQ no epílogo só exercitam a ISA.

### 5. Verifique

Stdout esperado:

```text
0
1
2
3
1
```

---

## Relatório

| ID | Aceite |
|----|--------|
| EXT-01 | monta add2/max_loop |
| EXT-02 | add2=8; bad_ret underflow |
| EXT-03 | mem_demo=42; bad_mem OOB |
| EXT-04 | max_loop 0..3 + 1 |

Critério final: `clvm_extended integration tests passed` em `solutions/`.

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Dúvidas abertas: ___
