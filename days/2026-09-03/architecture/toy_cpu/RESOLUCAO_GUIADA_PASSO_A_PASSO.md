# Resolução guiada auditada — Tiny CPU

## 0. Arquivos exatos

Edite somente:

```text
starter/src/cpu.cpp
starter/tests/test_cpu.cpp   # apenas quando a etapa pedir teste adicional
```

A enumeração dos opcodes já existe em `starter/include/cpu.hpp`.

## 1. Baseline

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

O build deve passar e o teste deve falhar quando `MOVI` for executado, porque `step()` ainda cai no TODO.

## 2. Fetch — já implementado, mas você precisa entendê-lo

Abra `starter/src/cpu.cpp` e localize `TinyCpu::fetch8` e `TinyCpu::fetch16`.

`fetch8` valida `pc_`, lê `memory_[pc_]` e só então incrementa o PC:

```cpp
return memory_[pc_++];
```

`fetch16` consome low byte e high byte:

```cpp
const std::uint16_t lo = fetch8();
const std::uint16_t hi = fetch8();
return static_cast<std::uint16_t>(lo | (hi << 8));
```

Não reescreva essas funções: neste starter elas já são infraestrutura para o exercício de decode/execute.

## 3. MOVI

Em `TinyCpu::step()`, depois de `case Op::Nop`, troque o `return true` por `break` e adicione:

```cpp
case Op::MovI: {
    const auto dst = checked_reg(fetch8());
    regs_[dst] = fetch16();
    break;
}
```

Por que `checked_reg`: o byte seguinte vem do programa e não é confiável; `4` ou maior não pode indexar `regs_`.

Teste mental do programa:

```text
10 00 05 00 FF
|  |  |----|  |
|  |   imm16  HALT
|  R0
MOVI
```

Depois compile/teste. O primeiro programa ainda falhará em `ADD`, o que é esperado.

## 4. ADD

Ainda em `step()`:

```cpp
case Op::Add: {
    const auto dst = checked_reg(fetch8());
    const auto src = checked_reg(fetch8());
    regs_[dst] = static_cast<std::uint16_t>(regs_[dst] + regs_[src]);
    break;
}
```

Agora o primeiro bloco de `starter/tests/test_cpu.cpp` deve passar: `R0=5`, `R1=7`, `ADD R0,R1` → `R0=12`.

## 5. STORE — este trecho faltava na resolução antiga

Formato desta ISA:

```text
STORE src:u8 address:u16-le
```

Adicione:

```cpp
case Op::Store: {
    const auto src = checked_reg(fetch8());
    const auto addr = fetch16();
    if (static_cast<std::size_t>(addr) + 1 >= memory_.size()) {
        throw std::out_of_range("store outside memory");
    }

    memory_[addr] = static_cast<std::uint8_t>(regs_[src] & 0xFFu);
    memory_[addr + 1] = static_cast<std::uint8_t>((regs_[src] >> 8) & 0xFFu);
    break;
}
```

Para `0x1234`, memória little-endian deve virar:

```text
[0x0100] = 0x34
[0x0101] = 0x12
```

## 6. LOAD — também faltava o código exato

Formato:

```text
LOAD dst:u8 address:u16-le
```

Adicione:

```cpp
case Op::Load: {
    const auto dst = checked_reg(fetch8());
    const auto addr = fetch16();
    if (static_cast<std::size_t>(addr) + 1 >= memory_.size()) {
        throw std::out_of_range("load outside memory");
    }

    regs_[dst] = static_cast<std::uint16_t>(
        memory_[addr] | (memory_[addr + 1] << 8));
    break;
}
```

Rode os testes. O segundo bloco deve confirmar `R3 == 0x1234` e os dois bytes na RAM.

## 7. JNZ — a resolução antiga só dizia para implementar; agora está completo

Formato:

```text
JNZ src:u8 target:u16-le
```

Adicione:

```cpp
case Op::Jnz: {
    const auto src = checked_reg(fetch8());
    const auto target = fetch16();
    if (target >= memory_.size()) {
        throw std::out_of_range("jump target outside memory");
    }

    if (regs_[src] != 0) {
        pc_ = target;
    }
    break;
}
```

O target é absoluto neste toy ISA. Não trate como deslocamento relativo.

### Teste manual para JNZ

Adicione temporariamente a `test_cpu.cpp`:

```cpp
{
    TinyCpu cpu;
    std::vector<std::uint8_t> program = {
        op(TinyCpu::Op::MovI), 0, 1, 0,
        op(TinyCpu::Op::Jnz), 0, 11, 0,
        op(TinyCpu::Op::MovI), 1, 99, 0,
        op(TinyCpu::Op::Halt),
    };
    cpu.load_program(program);
    cpu.run();
    assert(cpu.reg(1) == 0);
}
```

Conte os offsets antes de copiar o target. Se mudar o programa, recalcule-o.

## 8. HALT, opcode desconhecido e retorno de `step`

Mantenha:

```cpp
case Op::Halt:
    halted_ = true;
    return false;
```

Troque o TODO do `default` por:

```cpp
default:
    throw std::runtime_error("unknown opcode");
```

E, depois do `switch`, adicione:

```cpp
return true;
```

Sem esse retorno, caminhos como MOVI/ADD/LOAD/STORE/JNZ não devolvem corretamente que a CPU pode continuar.

## 9. Validação final

```bash
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Esperado:

```text
100% tests passed
```

## 10. Debugging

- `TODO: opcode not implemented`: você ainda cai no `default` antigo.
- `invalid register index`: inspecione o byte em `memory_[pc_]` antes de `checked_reg`.
- LOAD devolve `0x3412`: você inverteu endianness.
- `step limit exceeded`: provavelmente criou um JNZ que volta para si mesmo com registrador não zero.
- jump errado: coloque breakpoint no `case Op::Jnz` e observe `pc_`, `src`, `target` e `regs_[src]`.

## 11. Solução

Somente depois dos testes, compare com `solutions/src/cpu.cpp`. Todos os opcodes exigidos pelo TODO do starter estão implementados lá.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `CPU-STEP-01` — `starter/src/cpu.cpp` → `solutions/src/cpu.cpp`.
