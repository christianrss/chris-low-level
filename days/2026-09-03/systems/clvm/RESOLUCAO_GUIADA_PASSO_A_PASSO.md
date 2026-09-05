# RESOLUÇÃO GUIADA - Systems / CLVM

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `CLVM-PY-FNV-01` | `starter/tools/assemble.py` | `fnv1a32()` |
| `CLVM-ASM-LABELS-01` | `starter/tools/assemble.py` | `assemble()` — labels + JMP/JZ |
| `CLVM-C-FNV-01` | `starter/src/clvm_loader.c` | `clvm_fnv1a32()` |
| `CLVM-C-HEADER-01` | `starter/src/clvm_loader.c` | `clvm_parse()` — flags, entry, checksum |
| `CLVM-VM-ARITH-01` | `starter/src/main.cpp` | `run()` — ADD/SUB/MUL/DIV/DUP/PRINT |
| `CLVM-VM-JUMP-01` | `starter/src/main.cpp` | `run()` — JMP/JZ com offset i16 |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/systems/clvm/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

> Não comece copiando `solutions/`. Siga os passos abaixo e compile a cada etapa.

## Exercício Fácil A - implementar FNV-1a no assembler Python

### 1. O problema

O assembler precisa calcular um checksum do bytecode. O `starter/tools/assemble.py` possui:

```python
def fnv1a32(data: bytes) -> int:
    """TODO FÁCIL: implemente FNV-1a 32-bit."""
    return 0
```

Se a função sempre retorna zero, o header fica com checksum incorreto. O loader completo recusará o arquivo.

### 2. O algoritmo

FNV-1a começa com uma constante chamada **offset basis**:

```text
0x811C9DC5
```

Para cada byte:

```text
hash = hash XOR byte
hash = hash * 0x01000193
```

Como queremos 32 bits, descartamos bits acima do bit 31.

### 3. Escreva o código

Substitua o `return 0` por:

```python
hash_value = 0x811C9DC5

for byte in data:
    hash_value ^= byte
    hash_value = (hash_value * 0x01000193) & 0xFFFFFFFF

return hash_value
```

### 4. Entenda linha por linha

- `hash_value = ...`: estado inicial do algoritmo;
- `for byte in data`: visita o bytecode byte a byte;
- `^=`: XOR mistura o byte atual no hash;
- multiplicação pelo prime: espalha a influência do byte;
- `& 0xFFFFFFFF`: mantém apenas 32 bits em Python, que usa inteiros arbitrariamente grandes.

### 5. Teste

Na raiz do módulo:

```bash
python starter/tools/assemble.py \
    starter/programs/arithmetic.asm \
    starter/arithmetic.clvm
```

O arquivo deve ser criado. Ainda não é o fim do laboratório porque o loader C também precisa usar o mesmo checksum.

---

## Exercício Fácil B - implementar o mesmo FNV-1a em C

Abra:

```text
starter/src/clvm_loader.c
```

Localize `clvm_fnv1a32`.

### 1. Por que a versão C parece diferente?

Em C usamos `uint32_t`. Operações aritméticas nesse tipo são naturalmente reduzidas módulo `2^32`, então não precisamos escrever `& 0xFFFFFFFF` a cada multiplicação.

### 2. Implementação

```c
uint32_t clvm_fnv1a32(const uint8_t *data, size_t size) {
    uint32_t hash = 2166136261u;

    for (size_t i = 0; i < size; ++i) {
        hash ^= data[i];
        hash *= 16777619u;
    }

    return hash;
}
```

`2166136261` é `0x811C9DC5` em decimal. `16777619` é `0x01000193`.

### 3. Critério de correção

Python e C precisam produzir **o mesmo valor para os mesmos bytes**. Esse é um conceito importante de formatos binários: produtor e consumidor precisam concordar exatamente.

---

## Exercício Médio A - completar a validação do header CLVM

No `starter/src/clvm_loader.c`, o parser já verifica:

- ponteiros nulos;
- tamanho mínimo;
- magic `CLVM`;
- versão;
- `code_size` contra o tamanho real.

Ainda faltam três verificações.

### 1. Flags

Hoje a versão 1 não suporta flags. Portanto:

```c
if (img.flags != 0U) {
    return fail(err, err_cap, "unsupported flags");
}
```

### 2. Entry point

`entry` é o índice do primeiro opcode. Se houver código, ele precisa estar dentro de `[0, code_size)`:

```c
if (img.entry >= img.code_size && img.code_size != 0U) {
    return fail(err, err_cap, "entry outside code");
}
```

A segunda condição permite um arquivo vazio sem tentar dereferenciar código.

### 3. Checksum

Recalcule o checksum **sobre o bytecode, não sobre o header**:

```c
if (clvm_fnv1a32(img.code, img.code_size) != img.checksum) {
    return fail(err, err_cap, "checksum mismatch");
}
```

### 4. Por que a ordem importa?

Primeiro confirmamos que `code_size` cabe no buffer real. Só depois usamos `img.code_size` para percorrer bytes no checksum. Isso evita confiar em um tamanho malformado.

---

## Exercício Médio B - implementar operações da VM

Abra:

```text
starter/src/main.cpp
```

O `PUSH` já funciona. Agora implemente as operações de pilha.

### Função mental auxiliar: “quantos operandos eu preciso?”

- `ADD/SUB/MUL/DIV`: 2 valores;
- `DUP`: 1 valor;
- `PRINT`: 1 valor;
- `HALT`: 0.

Sempre valide a profundidade da stack **antes** de usar `back()` ou `pop_back()`.

### ADD

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
```

A ordem `lhs`/`rhs` quase não importa para soma, mas **importa para SUB e DIV**. Por isso já use o padrão correto.

### SUB

```cpp
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
```

### MUL

Repita o padrão e troque a expressão final para `lhs * rhs`.

### DIV

Além do underflow, valide divisão por zero:

```cpp
if (rhs == 0) {
    std::cerr << "division by zero\n";
    return 2;
}
```

Depois `stack.push_back(lhs / rhs);`.

### DUP

```cpp
case Op::Dup:
    if (stack.empty()) {
        std::cerr << "stack underflow in DUP\n";
        return 2;
    }
    stack.push_back(stack.back());
    break;
```

### PRINT

```cpp
case Op::Print:
    if (stack.empty()) {
        std::cerr << "stack underflow in PRINT\n";
        return 2;
    }
    std::cout << stack.back() << '\n';
    stack.pop_back();
    break;
```

### Teste do exercício médio

Compile e monte `arithmetic.asm`. A saída correta é:

```text
38
```

Se sair outro valor, use `--trace` e anote a stack após cada opcode.

---

## Exercício Difícil A - assembler em duas passagens

### Por que uma passagem não basta?

Considere:

```asm
JMP fim
PUSH 123
fim:
HALT
```

Quando o assembler encontra `JMP fim`, ainda não sabe em qual byte `fim` ficará. A solução clássica é:

1. primeira passagem: medir instruções e registrar labels;
2. segunda passagem: emitir bytes usando os offsets já conhecidos.

### 1. Crie `instruction_size`

```python
def instruction_size(line: str) -> int:
    if line.endswith(":"):
        return 0

    opcode_name = line.split()[0].upper()

    if opcode_name == "PUSH":
        return 5
    if opcode_name in ("JMP", "JZ"):
        return 3

    return 1
```

### 2. Primeira passagem

```python
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
```

### 3. Segunda passagem - JMP/JZ

Depois de saber os labels:

```python
opcode = 0x09 if opcode_name == "JMP" else 0x0A
next_pc = pc + 3
displacement = labels[parts[1]] - next_pc
```

O deslocamento é relativo ao **PC da próxima instrução**, não ao começo do JMP.

Valide i16:

```python
if not -32768 <= displacement <= 32767:
    raise ValueError("salto excede o alcance de i16")
```

Emita:

```python
output.append(opcode)
output += struct.pack("<h", displacement)
```

---

## Exercício Difícil B — JMP/JZ na VM

O passo a passo completo (leitor i16, `checked_jump`, casos `Op::Jmp`/`Op::Jz`, teste `countdown.asm` e prévia LOAD/STORE) está em **`RESOLUCAO_APENDICE.md`**.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `CLVM-C-FNV-01` — `starter/src/clvm_loader.c` → `solutions/src/clvm_loader.c`.
- `CLVM-C-HEADER-01` — `starter/src/clvm_loader.c` → `solutions/src/clvm_loader.c`.
- `CLVM-VM-ARITH-01` — `starter/src/main.cpp` → `solutions/src/main.cpp`.
- `CLVM-VM-JUMP-01` — `starter/src/main.cpp` → `solutions/src/main.cpp`.
- `CLVM-PY-FNV-01` — `starter/tools/assemble.py` → `solutions/tools/assemble.py`.
- `CLVM-ASM-LABELS-01` — `starter/tools/assemble.py` → `solutions/tools/assemble.py`.
## Relatório de resolução

### O que foi validado

- Todos os TODOs do `starter/` foram implementados na ordem sugerida.
- Testes com marcadores `PEDAGOGY-TEST` passaram na solution.
- O starter continua falhando nos pontos intencionais até o aluno completar cada ID.

### Armadilhas encontradas

- Leia mensagens de `assert` como contrato, não como bug do teste.
- Compare sempre starter vs solution diff por arquivo.
- Documente no benchmark o que *não* foi medido (I/O, rede, GPU, VM).

### Depuração e saída esperada

- **Depuração:** execute a VM com `--trace`; compare checksum FNV Python vs C byte a byte.
- **Saída esperada:** `arithmetic.asm` imprime `38`; `countdown.asm` imprime `3 2 1 0`; checksum inválido rejeitado.

### Próximo passo sugerido

Repita o módulo sem consultar a resolução, cronometrando apenas a fase de implementação. Depois leia `BENCHMARK_GUIADO.md` e registre suas observações na seção **Resultados observados**.
