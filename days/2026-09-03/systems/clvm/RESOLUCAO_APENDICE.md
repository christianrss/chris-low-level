# CLVM — apêndice da resolução guiada

> Continuação de `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` (JMP/JZ na VM e extensões futuras).

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

Monte e execute `countdown.asm`. Saída esperada:

```text
3
2
1
0
```

---

## Prévia de próximo milestone — LOAD/STORE

Esta seção é uma **prévia de design**, não exigida para o Day 01.

### 1. Adicione memória linear à VM

```cpp
std::vector<std::int32_t> memory(256, 0);
```

### 2. Defina opcodes

```text
0x0B LOAD  u8_index
0x0C STORE u8_index
```

### 3. LOAD / STORE

LOAD empilha `memory[index]`; STORE grava o topo na memória após validar índice e stack.

### 4. Atualize assembler e validador

Quando o formato muda, **todos** os produtores e consumidores precisam mudar juntos.
