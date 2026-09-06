# RESOLUÇÃO GUIADA — Systems / CLVM (Dia 01)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Âncora no starter (o que procurar) |
|---------|---------|-------------------------------------|
| `CLVM-PY-FNV-01` | `starter/tools/assemble.py` | função `fnv1a32` — docstring `TODO [CLVM-PY-FNV-01]` |
| `CLVM-ASM-LABELS-01` | `starter/tools/assemble.py` | função `assemble` — `raise NotImplementedError(...CLVM-ASM-LABELS-01...)` |
| `CLVM-C-FNV-01` | `starter/src/clvm_loader.c` | função `clvm_fnv1a32` — comentário `TODO [CLVM-C-FNV-01]` |
| `CLVM-C-HEADER-01` | `starter/src/clvm_loader.c` | dentro de `clvm_parse`, após `size mismatch` — `TODO [CLVM-C-HEADER-01]` |
| `CLVM-VM-ARITH-01` | `starter/src/main.cpp` | em `run()`, `switch` — `TODO [CLVM-VM-ARITH-01]` (cases Add…Print) |
| `CLVM-VM-JUMP-01` | `starter/src/main.cpp` | `TODO [CLVM-VM-JUMP-01]` + `default:` (JMP/JZ caem no default hoje) |

> Raiz do trabalho: `days/2026-09-03/systems/clvm/starter/`. Não copie `solutions/` no começo.

Cada seção abaixo tem **Onde colocar** (arquivo + função + o que substituir) antes do código.

Paper-trace longo: `RESOLUCAO_APENDICE.md` (opcional).

---

## Baseline

```powershell
cd days/2026-09-03/systems/clvm/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

Esperado: FAIL até completar os TODOs (em especial labels + JMP/JZ).

Ordem: PY-FNV → C-FNV → HEADER → ASM-LABELS → VM-ARITH → VM-JUMP.

---

## CLVM-PY-FNV-01 — FNV-1a no assembler

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/tools/assemble.py` |
| **Função** | `fnv1a32` (logo após o dict `OPS`) |
| **Substituir** | o **corpo inteiro** da função (o que está sob `TODO [CLVM-PY-FNV-01]`). Não mude a assinatura. |
| **Não mexer** | `main()`, `parse_lines`, `OPS` |

### 1. O problema

Sem FNV correto, o campo checksum do header fica errado e o loader C rejeita o `.clvm`.

### 2. O algoritmo

```text
hash = 0x811C9DC5
para cada byte: hash ^= byte; hash = (hash * 0x01000193) & 0xFFFFFFFF
```

### 3. Escreva o código

Cole isto **como corpo** de `fnv1a32` (pode manter o docstring TODO ou atualizá-lo):

```python
    hash_value = 0x811C9DC5
    for byte in data:
        hash_value ^= byte
        hash_value = (hash_value * 0x01000193) & 0xFFFFFFFF
    return hash_value
```

### 4. Por que funciona

XOR + prime FNV; `& 0xFFFFFFFF` corta a 32 bits em Python.

### 5. Verifique

```powershell
python tools/assemble.py programs/arithmetic.asm out.clvm
```

(a partir de `starter/`). Esperado: arquivo criado. O header usa `fnv1a32(code)` em `main()` — não precisa editar `main`.

---

## CLVM-C-FNV-01 — mesmo FNV em C

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/clvm_loader.c` |
| **Função** | `clvm_fnv1a32` (primeira função exportada do arquivo, ~linha 9) |
| **Substituir** | corpo sob `/* TODO [CLVM-C-FNV-01]: ... */` |
| **Não mexer** | `read_u16_le` / `read_u32_le` / `fail` |

### 1. O problema

Python e C precisam do **mesmo** hash para os mesmos bytes.

### 2. O algoritmo

Iguais constantes; `uint32_t` já faz wrap em `2^32`.

### 3. Escreva o código

Corpo de `clvm_fnv1a32`:

```c
    uint32_t hash = 2166136261u; /* 0x811C9DC5 */
    for (size_t i = 0; i < size; ++i) {
        hash ^= data[i];
        hash *= 16777619u; /* 0x01000193 */
    }
    return hash;
```

### 4. Por que funciona

Mesmas constantes do Python em decimal; sem máscara explícita.

### 5. Verifique

Critério: valor idêntico ao de `fnv1a32` em Python para o mesmo buffer. Depure comparando os dois se o parse falhar com `checksum mismatch`.

---

## CLVM-C-HEADER-01 — validação do header

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/clvm_loader.c` |
| **Função** | `clvm_parse` |
| **Posição** | **depois** de `if((size_t)img.code_size!=file_size-16) ...` e **antes** de `*out=img; return 1;` |
| **Âncora** | comentário `/* TODO [CLVM-C-HEADER-01]: ... */` |
| **Inserir** | os três `if` abaixo **no lugar desse TODO** (não no topo do parse) |

### 1. O problema

Magic/versão/tamanho já existem; faltam flags, entry e checksum.

### 2. O algoritmo

flags≠0; entry fora do código; FNV(`img.code`, `code_size`) ≠ `img.checksum`.

### 3. Escreva o código

Cole **exatamente nesse ponto** de `clvm_parse`:

```c
    if (img.flags != 0U) {
        return fail(err, err_cap, "unsupported flags");
    }
    if (img.entry >= img.code_size && img.code_size != 0U) {
        return fail(err, err_cap, "entry outside code");
    }
    if (clvm_fnv1a32(img.code, img.code_size) != img.checksum) {
        return fail(err, err_cap, "checksum mismatch");
    }
```

### 4. Por que funciona

Só após validar `code_size` vs arquivo real é seguro varrer o bytecode no FNV.

### 5. Verifique

Integração: arquivo com byte final xorado → stderr com `checksum mismatch`. Mensagens esperadas: `unsupported flags`, `entry outside code`, `checksum mismatch`.

---

## CLVM-ASM-LABELS-01 — assembler em duas passagens

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/tools/assemble.py` |
| **Função a reescrever** | `assemble` (a que hoje faz um `for` simples e dá `NotImplementedError` em label/JMP/JZ) |
| **Helper já existente** | `instruction_size` está **abaixo** de `assemble` no mesmo arquivo — **use-o**; não duplique. Pode mover `instruction_size` para **acima** de `assemble` se preferir ler na ordem. |
| **Substituir** | o **corpo inteiro** de `assemble` (do `output = bytearray()` até o `return bytes(output)`), removendo o `raise NotImplementedError` |
| **Não mexer** | `OPS`, `fnv1a32`, `parse_lines`, `main` |

### 1. O problema

Labels à frente exigem duas passagens; o starter aborta em `JMP`/`JZ`/labels.

### 2. O algoritmo

Passagem 1: `labels[nome]=pc`. Passagem 2: emitir; `displacement = labels[alvo] - (pc+3)`.

### 3. Escreva o código

**Substitua a função `assemble` inteira** por:

```python
def assemble(text: str) -> bytes:
    lines = parse_lines(text)
    labels: dict[str, int] = {}
    pc = 0

    for line in lines:
        if line.endswith(":"):
            label = line[:-1].strip()
            if not label or label in labels:
                raise ValueError(f"label inválido ou duplicado: {label}")
            labels[label] = pc
        else:
            pc += instruction_size(line)

    output = bytearray()
    pc = 0
    for line in lines:
        if line.endswith(":"):
            continue
        parts = line.split()
        opcode_name = parts[0].upper()

        if opcode_name == "PUSH":
            if len(parts) != 2:
                raise ValueError("PUSH precisa de um inteiro i32")
            output.append(0x01)
            output += struct.pack("<i", int(parts[1], 0))
        elif opcode_name in OPS:
            if len(parts) != 1:
                raise ValueError(f"{opcode_name} não recebe operando")
            output.append(OPS[opcode_name])
        elif opcode_name in ("JMP", "JZ"):
            if len(parts) != 2 or parts[1] not in labels:
                raise ValueError(f"{opcode_name} precisa de um label conhecido")
            opcode = 0x09 if opcode_name == "JMP" else 0x0A
            next_pc = pc + 3
            displacement = labels[parts[1]] - next_pc
            if not -32768 <= displacement <= 32767:
                raise ValueError("salto excede o alcance de i16")
            output.append(opcode)
            output += struct.pack("<h", displacement)
        else:
            raise ValueError(f"instrução desconhecida: {opcode_name}")

        pc += instruction_size(line)

    return bytes(output)
```

Confirme que `instruction_size` no mesmo arquivo já trata label→0, PUSH→5, JMP/JZ→3, resto→1. Se estiver incompleta, complete **só** essa função, não outra cópia.

### 4. Por que funciona

`pc+3` = endereço após o i16 — igual à VM após consumir o operando.

### 5. Verifique

```powershell
python tools/assemble.py programs/countdown.asm countdown.clvm
```

Esperado: sem `NotImplementedError` / `ValueError`.

---

## CLVM-VM-ARITH-01 — aritmética e PRINT

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/main.cpp` |
| **Função** | `run` (anonymous namespace) |
| **Posição** | dentro do `switch (static_cast<Op>(opcode))`, **depois** de `case Op::Halt` e **antes** do comentário `TODO [CLVM-VM-JUMP-01]` |
| **Âncora** | `// TODO [CLVM-VM-ARITH-01]: ...` |
| **Substituir / completar** | os `case Op::Add` … `case Op::Print` sob esse TODO (já podem existir stubs — alinhe underflow, ordem lhs/rhs e DIV por zero) |
| **Não mexer ainda** | `default:` (isso é o JUMP) |

### 1. O problema

Sem ADD…PRINT corretos, `arithmetic.asm` não imprime `38`.

### 2. O algoritmo

Pop **rhs** (topo), depois **lhs**. DIV: `rhs==0` → erro.

### 3. Escreva o código

Nos cases sob `TODO [CLVM-VM-ARITH-01]` em `run()`:

```cpp
            case Op::Add: {
                if (stack.size() < 2) {
                    std::cerr << "stack underflow in ADD\n";
                    return 2;
                }
                const std::int32_t rhs = stack.back();
                stack.pop_back();
                const std::int32_t lhs = stack.back();
                stack.pop_back();
                stack.push_back(lhs + rhs);
                break;
            }
            case Op::Sub: {
                if (stack.size() < 2) {
                    std::cerr << "stack underflow in SUB\n";
                    return 2;
                }
                const std::int32_t rhs = stack.back();
                stack.pop_back();
                const std::int32_t lhs = stack.back();
                stack.pop_back();
                stack.push_back(lhs - rhs);
                break;
            }
            case Op::Mul: {
                if (stack.size() < 2) {
                    std::cerr << "stack underflow in MUL\n";
                    return 2;
                }
                const std::int32_t rhs = stack.back();
                stack.pop_back();
                const std::int32_t lhs = stack.back();
                stack.pop_back();
                stack.push_back(lhs * rhs);
                break;
            }
            case Op::Div: {
                if (stack.size() < 2) {
                    std::cerr << "stack underflow in DIV\n";
                    return 2;
                }
                const std::int32_t rhs = stack.back();
                stack.pop_back();
                const std::int32_t lhs = stack.back();
                stack.pop_back();
                if (rhs == 0) {
                    std::cerr << "division by zero\n";
                    return 2;
                }
                stack.push_back(lhs / rhs);
                break;
            }
            case Op::Dup:
                if (stack.empty()) {
                    std::cerr << "stack underflow in DUP\n";
                    return 2;
                }
                stack.push_back(stack.back());
                break;
            case Op::Print:
                if (stack.empty()) {
                    std::cerr << "stack underflow in PRINT\n";
                    return 2;
                }
                std::cout << stack.back() << '\n';
                stack.pop_back();
                break;
```

### 4. Por que funciona

Ordem lhs/rhs importa em SUB/DIV. Checar tamanho antes de `back()` evita UB.

### 5. Verifique

Monte `programs/arithmetic.asm`, rode `clvm`. Saída esperada: `38`. Debug: `clvm ... --trace`.

---

## CLVM-VM-JUMP-01 — JMP/JZ na VM

### Onde colocar (três edições no mesmo arquivo)

**Arquivo:** `starter/src/main.cpp`

1. **Helper `read_i16_le`** — no anonymous namespace, **logo após** a função `read_i32_le` (antes de `int run(...)`). Função **nova**; o starter não tem.

2. **Helpers locais em `run`** — no início de `run`, **depois** de `std::size_t pc = image.entry;` e **antes** do `while (pc < image.code_size)`, adicione:
   - lambda/`need` (se ainda não houver) para `pc + n <= image.code_size`
   - lambda `checked_jump` como abaixo  
   Também declare `std::int32_t lhs = 0;` (e use no JZ) no escopo do loop/switch se ainda não existir.

3. **Cases no `switch`** — **substitua** o bloco que hoje é só:
   ```cpp
   // TODO [CLVM-VM-JUMP-01]: ...
   default:
       std::cerr << "unimplemented/unknown opcode ...
   ```
   por: `case Op::Jmp: { ... }` + `case Op::Jz: { ... }` + **depois** o `default:` (opcodes desconhecidos continuam no default).

**Não coloque** JMP/JZ dentro de `main()`; só em `run()`.

### 1. O problema

Hoje `Jmp`/`Jz` caem no `default` → `unimplemented/unknown opcode`. `countdown.asm` não roda.

### 2. O algoritmo

Ler i16; `pc += 2`; JMP sempre salta; JZ dá pop e salta se `== 0`.

### 3. Escreva o código

**(A)** Após `read_i32_le`:

```cpp
std::int16_t read_i16_le(const std::uint8_t* bytes) {
    const std::uint16_t value =
        static_cast<std::uint16_t>(bytes[0]) |
        (static_cast<std::uint16_t>(bytes[1]) << 8U);
    return static_cast<std::int16_t>(value);
}
```

**(B)** No início de `run`, após `pc = image.entry`:

```cpp
    const auto need = [&](std::size_t byte_count) {
        return pc + byte_count <= image.code_size;
    };
    const auto checked_jump = [&](std::int16_t relative) -> bool {
        const std::int64_t base = static_cast<std::int64_t>(pc);
        const std::int64_t target = base + static_cast<std::int64_t>(relative);
        if (target < 0 || target >= static_cast<std::int64_t>(image.code_size)) {
            return false;
        }
        pc = static_cast<std::size_t>(target);
        return true;
    };
```

**(C)** No `switch`, no lugar do TODO JUMP (antes do `default`):

```cpp
            case Op::Jmp: {
                if (!need(2)) {
                    std::cerr << "error: truncated JMP\n";
                    return 2;
                }
                const std::int16_t relative = read_i16_le(image.code + pc);
                pc += 2;
                if (!checked_jump(relative)) {
                    std::cerr << "error: jump outside code\n";
                    return 2;
                }
                break;
            }
            case Op::Jz: {
                if (!need(2)) {
                    std::cerr << "error: truncated JZ\n";
                    return 2;
                }
                const std::int16_t relative = read_i16_le(image.code + pc);
                pc += 2;
                if (stack.empty()) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                const std::int32_t cond = stack.back();
                stack.pop_back();
                if (cond == 0 && !checked_jump(relative)) {
                    std::cerr << "error: jump outside code\n";
                    return 2;
                }
                break;
            }
            default:
                std::cerr << "unimplemented/unknown opcode at pc="
                          << opcode_pc << '\n';
                return 2;
```

### 4. Por que funciona

`pc` já passou do opcode; após `pc += 2` o base do salto = `next_pc` do assembler. JZ sempre consome a condição.

### 5. Verifique

`countdown.asm` → stdout esperado:

```text
3
2
1
0
```

Trace: `RESOLUCAO_APENDICE.md`. Debug: `clvm countdown.clvm --trace`.

---

## Desafio opcional

`CLVM-TOOL-01` (EXERCICIOS) — fora do TODO_MAP; arquivo novo à sua escolha (ex. `starter/tools/disassemble.py`).

## Relatório

| ID | Onde (resumo) | Aceite |
|----|---------------|--------|
| PY-FNV | `assemble.py` → `fnv1a32` | header com checksum |
| C-FNV | `clvm_loader.c` → `clvm_fnv1a32` | = Python |
| HEADER | `clvm_parse` após size check | `checksum mismatch` |
| ASM-LABELS | substituir `assemble()` | monta countdown |
| VM-ARITH | cases sob TODO ARITH | `38` |
| VM-JUMP | `read_i16_le` + cases antes do `default` | `3 2 1 0` |

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Depuração (`--trace` / checksum): ___
- Dúvidas: ___

Próximo: Dia 04 `systems/clvm_extended`. Benchmark: `BENCHMARK_GUIADO.md` → **Resultados observados**.
