# RESOLUÇÃO GUIADA - Systems / CLVM

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

## Exercício Difícil B - executar JMP/JZ na VM

Você precisará ler um `i16` little-endian. Crie uma função parecida com `read_i32_le`, porém com dois bytes e conversão para `int16_t`.

### 1. Crie o leitor de i16

```cpp
std::int16_t read_i16_le(const std::uint8_t* bytes) {
    const std::uint16_t value =
        static_cast<std::uint16_t>(bytes[0]) |
        (static_cast<std::uint16_t>(bytes[1]) << 8U);

    return static_cast<std::int16_t>(value);
}
```

### 2. Crie um helper para salto validado

O `pc` precisa já apontar para a próxima instrução quando somamos o deslocamento:

```cpp
const auto checked_jump = [&](std::int16_t relative) -> bool {
    const std::int64_t base = static_cast<std::int64_t>(pc);
    const std::int64_t target =
        base + static_cast<std::int64_t>(relative);

    if (target < 0 ||
        target >= static_cast<std::int64_t>(image.code_size)) {
        return false;
    }

    pc = static_cast<std::size_t>(target);
    return true;
};
```

### 3. JMP completo

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
```

### 4. JZ completo

Na semântica deste laboratório, JZ consome o valor do topo:

```cpp
case Op::Jz: {
    if (!need(2)) {
        std::cerr << "error: truncated JZ\n";
        return 2;
    }

    const std::int16_t relative = read_i16_le(image.code + pc);
    pc += 2;

    if (!pop_value(stack, lhs)) {
        std::cerr << "error: stack underflow\n";
        return 2;
    }

    if (lhs == 0 && !checked_jump(relative)) {
        std::cerr << "error: jump outside code\n";
        return 2;
    }
    break;
}
```

A ordem é importante: primeiro consumimos os dois bytes do imediato, depois calculamos o destino relativo ao PC seguinte.

### Teste

Monte e execute `countdown.asm`. Saída:

```text
3
2
1
0
```

---

## Desafio - como adicionar LOAD/STORE

Este desafio não exige copiar uma solução pronta; ele ensina design de ISA.

### 1. Adicione memória linear à VM

```cpp
std::vector<std::int32_t> memory(256, 0);
```

### 2. Defina opcodes

Por exemplo:

```text
0x0B LOAD  u8_index
0x0C STORE u8_index
```

### 3. LOAD

- lê o índice imediato;
- valida `index < memory.size()`;
- empilha `memory[index]`.

### 4. STORE

- lê o índice;
- valida índice;
- valida stack não vazia;
- remove topo e grava em `memory[index]`.

### 5. Atualize o assembler

`instruction_size` deve retornar 2 para LOAD/STORE. Na emissão, use `struct.pack("<B", index)`.

### 6. Atualize o validador

O validador Rust precisa reconhecer que LOAD/STORE consomem um byte de imediato. Essa é a principal lição: **quando o formato muda, todos os produtores e consumidores precisam mudar juntos**.
