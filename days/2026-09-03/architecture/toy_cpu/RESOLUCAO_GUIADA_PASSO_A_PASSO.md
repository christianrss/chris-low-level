# Resolucao guiada

1. Implemente `fetch8`: leia o byte no PC e avance o PC. Valide limites antes de ler.
2. Implemente `fetch16` combinando byte baixo e alto. Explique por que `lo | hi<<8` e little-endian.
3. Implemente `MOVI`; teste antes de continuar.
4. Implemente `ADD`; crie um programa que coloca 5 em R0, 7 em R1 e termina com R0=12.
5. Adicione STORE/LOAD e um teste que grave 0x1234 em 0x0100 e leia de volta.
6. Adicione erro para opcode desconhecido. Esse e um teste negativo importante para um decoder.
7. Rode o benchmark de instrucoes/segundo. Depois mude o dispatch `switch` em outro dia e compare metodologicamente.

## Etapa de código 1 - fetch

```cpp
std::uint8_t TinyCpu::fetch8() {
    if (pc_ >= memory_.size()) {
        throw std::out_of_range("program counter outside memory");
    }
    return memory_[pc_++];
}
```

Depois componha 16 bits little-endian:

```cpp
std::uint16_t TinyCpu::fetch16() {
    const std::uint16_t lo = fetch8();
    const std::uint16_t hi = fetch8();
    return static_cast<std::uint16_t>(lo | (hi << 8));
}
```

## Etapa de código 2 - MOVI

```cpp
case Op::MovI: {
    const auto dst = checked_reg(fetch8());
    regs_[dst] = fetch16();
    break;
}
```

Escreva um teste que executa apenas `MOVI R0, 5` + `HALT` antes de implementar ADD.

## Etapa de código 3 - ADD

```cpp
case Op::Add: {
    const auto dst = checked_reg(fetch8());
    const auto src = checked_reg(fetch8());
    regs_[dst] = static_cast<std::uint16_t>(regs_[dst] + regs_[src]);
    break;
}
```

## Teste de integração mínimo

```cpp
std::vector<std::uint8_t> program = {
    op(TinyCpu::Op::MovI), 0, 5, 0,
    op(TinyCpu::Op::MovI), 1, 7, 0,
    op(TinyCpu::Op::Add), 0, 1,
    op(TinyCpu::Op::Halt),
};
```

Depois implemente LOAD/STORE/JNZ uma instrução por commit. A solução final está em `solutions/src/cpu.cpp`.

