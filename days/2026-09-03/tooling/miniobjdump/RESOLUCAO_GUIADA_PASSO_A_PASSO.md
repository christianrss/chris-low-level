# RESOLUÇÃO GUIADA - Tooling / MiniObjdump

## Exercício Fácil - ler inteiros little-endian com segurança

Abra:

```text
starter/src/main.cpp
```

### read_u16_le

Dois bytes `b0 b1` representam:

```text
valor = b0 + (b1 << 8)
```

Implemente:

```cpp
return static_cast<std::uint16_t>(data[offset]) |
       (static_cast<std::uint16_t>(data[offset + 1]) << 8U);
```

A checagem `offset + 2 > data.size()` já evita leitura fora do vetor.

### read_u32_le

```cpp
return static_cast<std::uint32_t>(data[offset]) |
       (static_cast<std::uint32_t>(data[offset + 1]) << 8U) |
       (static_cast<std::uint32_t>(data[offset + 2]) << 16U) |
       (static_cast<std::uint32_t>(data[offset + 3]) << 24U);
```

### Por que fazer cast antes do shift?

Para garantir que o deslocamento ocorra em um tipo grande o suficiente e com semântica unsigned previsível.

---

## Exercício Médio A - detectar e navegar ELF64

### 1. Verifique magic

```cpp
if (data.size() < 64 ||
    data[0] != 0x7FU || data[1] != 'E' ||
    data[2] != 'L' || data[3] != 'F') {
    return false;
}
```

### 2. Restrinja o escopo do primeiro parser

Hoje suporte apenas:

```text
ELFCLASS64 = 2
ELFDATA2LSB = 1
```

Assim você não finge entender ELF32 ou big-endian.

### 3. Leia metadados da section table

No ELF64:

```cpp
section_table      = read_u64_le(data, 40);
section_entry_size = read_u16_le(data, 58);
section_count      = read_u16_le(data, 60);
string_index       = read_u16_le(data, 62);
```

Esses offsets vêm da especificação do ELF64 header.

### 4. Localize a section string table

Cada section header ELF64 possui 64 bytes. O header indicado por `string_index` informa onde está o bloco de nomes das sections.

Leia:

```cpp
const std::uint64_t strings_header =
    section_table +
    static_cast<std::uint64_t>(string_index) * section_entry_size;

const std::uint64_t strings_offset = read_u64_le(data, strings_header + 24);
const std::uint64_t strings_size = read_u64_le(data, strings_header + 32);
```

### 5. Itere pelas sections

Para cada índice:

```cpp
header = section_table + index * section_entry_size
```

Leia:

- `sh_name` em `+0`;
- virtual address em `+16`;
- file offset em `+24`;
- size em `+32`.

O nome real é `strings_offset + name_offset`.

### 6. Quando o nome for `.text`

Chame seu decoder com:

```text
offset físico + tamanho + virtual address
```

---

## Exercício Médio B - navegar PE

### 1. Verifique MZ

```cpp
if (data.size() < 0x40 || data[0] != 'M' || data[1] != 'Z') {
    return false;
}
```

### 2. Leia e_lfanew

Offset `0x3C` do DOS header contém um `u32` para o PE header:

```cpp
const std::uint32_t pe_offset = read_u32_le(data, 0x3C);
```

### 3. Valide `PE\0\0`

```cpp
if (std::memcmp(data.data() + pe_offset, "PE\0\0", 4) != 0) {
    throw std::runtime_error("MZ file without PE signature");
}
```

### 4. Section table

No COFF header:

```cpp
section_count = read_u16_le(data, pe_offset + 6);
optional_size = read_u16_le(data, pe_offset + 20);
section_table = pe_offset + 24 + optional_size;
```

Cada PE section header possui 40 bytes.

Leia nome (8 bytes), RVA (`+12`), raw size (`+16`) e raw offset (`+20`).

---

## Exercício Difícil - decoder x86-64 mínimo

### Princípio mais importante

Um decoder jamais deve entrar em loop infinito nem ler além do fim. Portanto, toda iteração precisa consumir pelo menos um byte.

### 1. Estrutura do loop

```cpp
std::size_t pc = offset;
const std::size_t end = std::min(data.size(), offset + size);

while (pc < end) {
    const std::size_t instruction_offset = pc;
    const std::uint8_t opcode = data[pc++];

    // decode...

    if (pc <= instruction_offset) {
        throw std::runtime_error("decoder made no progress");
    }
}
```

### 2. Opcodes simples

```cpp
if (opcode == 0x55U) {
    std::cout << "push rbp";
} else if (opcode == 0xC3U) {
    std::cout << "ret";
} else if (opcode == 0x90U) {
    std::cout << "nop";
}
```

### 3. MOV RBP,RSP específico

A sequência:

```text
48 89 E5
```

pode ser reconhecida didaticamente:

```cpp
else if (opcode == 0x48U && pc + 2 <= end &&
         data[pc] == 0x89U && data[pc + 1] == 0xE5U) {
    pc += 2;
    std::cout << "mov rbp, rsp";
}
```

Isso **não é um decoder geral de MOV**. É apenas um primeiro caso concreto antes de estudar ModR/M.

### 4. CALL/JMP rel32

`E8` = CALL rel32 e `E9` = JMP rel32.

```cpp
const std::int32_t displacement =
    static_cast<std::int32_t>(read_u32_le(data, pc));
pc += 4;

const std::uint64_t next_address =
    virtual_address + (pc - offset);

const std::uint64_t target = static_cast<std::uint64_t>(
    static_cast<std::int64_t>(next_address) + displacement
);
```

A conversão para `int64_t` antes da soma preserva deslocamentos negativos.

### 5. Fallback

```cpp
else {
    std::cout << "db 0x";
    print_hex_byte(opcode);
}
```

É melhor admitir “não sei decodificar” do que inventar uma instrução errada.

---

## Extensão resolvida - adicionar INT3 e LEAVE

Antes do fallback:

```cpp
else if (opcode == 0xCCU) {
    std::cout << "int3";
} else if (opcode == 0xC9U) {
    std::cout << "leave";
}
```

`INT3` será importante quando construirmos nosso debugger, porque software breakpoints x86 usam esse opcode.

---

## Prévia de próximo milestone — basic blocks e cross-references (não é TODO obrigatório do starter de hoje)

Esta seção é uma **prévia de design**, não uma implementação exigida para concluir o Day 01. O starter atual não contém TODO para CFG/xrefs e a solution do Day 01 não afirma implementá-los.

Um **basic block** é uma sequência linear de instruções com uma entrada principal e sem branch no meio.

### Algoritmo didático

1. decodifique todas as instruções e guarde `address`, `size`, `kind`, `target`;
2. crie um conjunto `leaders`;
3. adicione o entry point como leader;
4. para cada CALL/JMP/Jcc, adicione o target quando estiver dentro da section;
5. para branches condicionais, adicione também a instrução seguinte;
6. para JMP incondicional e RET, encerre o bloco;
7. ordene leaders e forme intervalos.

Estrutura sugerida:

```cpp
struct DecodedInstruction {
    std::uint64_t address;
    std::uint8_t size;
    enum class Kind { Normal, Call, Jump, ConditionalJump, Return } kind;
    std::uint64_t target;
};
```

Cross-reference pode começar como:

```cpp
std::unordered_map<std::uint64_t, std::vector<std::uint64_t>> xrefs;
```

onde `xrefs[target]` contém os endereços que apontam para `target`.

Isso é a semente de uma visão gráfica estilo IDA/Ghidra.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `OBJDUMP-U16-01` — `starter/src/main.cpp` → `solutions/src/main.cpp`.
- `OBJDUMP-U32-01` — `starter/src/main.cpp` → `solutions/src/main.cpp`.
- `OBJDUMP-PARSE-01` — `starter/src/main.cpp` → `solutions/src/main.cpp`.
