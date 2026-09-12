# Apêndice — `Session::step` completo

## XDBG-STEP-01 — um opcode observável

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `Session::step` — `TODO [XDBG-STEP-01]` |
| **Substituir** | o stub que grava `not implemented` |
| **Não mexer** | `host/main.cpp` (já chama `step` / `cont`) |

### O problema

`step` que internamente corre até HALT torna hex/disasm/break inúteis.
O e2e de add2 precisa de sete opcodes visíveis, não de um `run()`.

### Algoritmo / trace

Fetch `code[pc++]`. PUSH: `need(4)` então `pc += 4`. CALL: lê i16,
empilha o PC já avançado, soma o displacement. PRINT empurra para
`prints`. HALT só muda `status`. LOAD/STORE passam por `mem_in_bounds`.

Paper-trace: PC 0→5→10→15→16→13→14 com `prints=[8]` no PRINT.

### Escreva o código

Cole o switch inteiro. Helpers no mesmo arquivo: `read_i32_le`,
`read_i16_le`, `pop_value`, `mem_in_bounds`, `fail`.

```cpp
DbgStatus Session::step() {
    if (status == DbgStatus::Halted || status == DbgStatus::Error) {
        return status;
    }
    if (!loaded) {
        return fail(*this, "not loaded");
    }
    if (++steps > kMaxSteps) {
        return fail(*this, "step limit exceeded");
    }
    if (pc >= image.code_size) {
        return fail(*this, "execution reached end without HALT");
    }

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

    const Op op = static_cast<Op>(image.code[pc++]);
    std::int32_t lhs = 0;
    std::int32_t rhs = 0;
    status = DbgStatus::Ready;

    switch (op) {
        case Op::Push:
            if (!need(4) || data_stack.size() >= kMaxStack) {
                return fail(*this, "truncated");
            }
            data_stack.push_back(read_i32_le(image.code + pc));
            pc += 4;
            break;
        case Op::Add:
        case Op::Sub:
        case Op::Mul:
        case Op::Div:
            if (!pop_value(data_stack, rhs) || !pop_value(data_stack, lhs)) {
                return fail(*this, "stack underflow");
            }
            if (op == Op::Div && rhs == 0) {
                return fail(*this, "division by zero");
            }
            if (op == Op::Add) {
                data_stack.push_back(lhs + rhs);
            } else if (op == Op::Sub) {
                data_stack.push_back(lhs - rhs);
            } else if (op == Op::Mul) {
                data_stack.push_back(lhs * rhs);
            } else {
                data_stack.push_back(lhs / rhs);
            }
            break;
        case Op::Dup:
            if (data_stack.empty() || data_stack.size() >= kMaxStack) {
                return fail(*this, "stack underflow");
            }
            data_stack.push_back(data_stack.back());
            break;
        case Op::Print:
            if (!pop_value(data_stack, lhs)) {
                return fail(*this, "stack underflow");
            }
            prints.push_back(lhs);
            break;
        case Op::Halt:
            status = DbgStatus::Halted;
            break;
        case Op::Jmp: {
            if (!need(2)) {
                return fail(*this, "truncated");
            }
            const std::int16_t relative = read_i16_le(image.code + pc);
            pc += 2;
            if (!checked_jump(relative)) {
                return fail(*this, "jump outside code");
            }
            break;
        }
        case Op::Jz: {
            if (!need(2)) {
                return fail(*this, "truncated");
            }
            const std::int16_t relative = read_i16_le(image.code + pc);
            pc += 2;
            if (!pop_value(data_stack, lhs)) {
                return fail(*this, "stack underflow");
            }
            if (lhs == 0 && !checked_jump(relative)) {
                return fail(*this, "jump outside code");
            }
            break;
        }
        case Op::Call: {
            if (!need(2) || call_stack.size() >= kMaxCall) {
                return fail(*this, "truncated");
            }
            const std::int16_t relative = read_i16_le(image.code + pc);
            pc += 2;
            call_stack.push_back(pc);
            if (!checked_jump(relative)) {
                return fail(*this, "call outside code");
            }
            break;
        }
        case Op::Ret: {
            if (call_stack.empty()) {
                return fail(*this, "return stack underflow");
            }
            pc = call_stack.back();
            call_stack.pop_back();
            break;
        }
        case Op::Store: {
            std::int32_t addr = 0;
            std::int32_t value = 0;
            if (!pop_value(data_stack, addr) || !pop_value(data_stack, value)) {
                return fail(*this, "stack underflow");
            }
            if (!mem_in_bounds(addr)) {
                return fail(*this, "memory out of bounds");
            }
            const auto u = static_cast<std::uint32_t>(value);
            mem[static_cast<std::size_t>(addr) + 0] = static_cast<std::uint8_t>(u & 0xFF);
            mem[static_cast<std::size_t>(addr) + 1] = static_cast<std::uint8_t>((u >> 8) & 0xFF);
            mem[static_cast<std::size_t>(addr) + 2] = static_cast<std::uint8_t>((u >> 16) & 0xFF);
            mem[static_cast<std::size_t>(addr) + 3] = static_cast<std::uint8_t>((u >> 24) & 0xFF);
            break;
        }
        case Op::Load: {
            std::int32_t addr = 0;
            if (!pop_value(data_stack, addr)) {
                return fail(*this, "stack underflow");
            }
            if (!mem_in_bounds(addr)) {
                return fail(*this, "memory out of bounds");
            }
            if (data_stack.size() >= kMaxStack) {
                return fail(*this, "stack overflow");
            }
            data_stack.push_back(read_i32_le(mem.data() + static_cast<std::size_t>(addr)));
            break;
        }
        case Op::Drop:
            if (!pop_value(data_stack, lhs)) {
                return fail(*this, "stack underflow");
            }
            break;
        case Op::Swap:
            if (!pop_value(data_stack, rhs) || !pop_value(data_stack, lhs)) {
                return fail(*this, "stack underflow");
            }
            data_stack.push_back(rhs);
            data_stack.push_back(lhs);
            break;
        case Op::Eq:
        case Op::Lt:
            if (!pop_value(data_stack, rhs) || !pop_value(data_stack, lhs)) {
                return fail(*this, "stack underflow");
            }
            if (op == Op::Eq) {
                data_stack.push_back(lhs == rhs ? 1 : 0);
            } else {
                data_stack.push_back(lhs < rhs ? 1 : 0);
            }
            break;
        case Op::Jnz: {
            if (!need(2)) {
                return fail(*this, "truncated");
            }
            const std::int16_t relative = read_i16_le(image.code + pc);
            pc += 2;
            if (!pop_value(data_stack, lhs)) {
                return fail(*this, "stack underflow");
            }
            if (lhs != 0 && !checked_jump(relative)) {
                return fail(*this, "jump outside code");
            }
            break;
        }
        default:
            return fail(*this, "unknown opcode");
    }
    return status;
}
```

### Por que funciona

Um único ponto de fetch. Operandos medidos **depois** do byte de
opcode. Call stack e data stack não se misturam. Bounds de memória são
o mesmo predicado para LOAD e STORE — o mutante NO-BOUNDS quebra o
caso 14.

### Verifique

```powershell
ctest --test-dir days/2026-09-12/systems/clvm_xdbg/starter/build_ci -R xdbg_session --output-on-failure
```

Esperado após este TODO: casos 5, 6 e 10 PASS (e2e `prints=[8]`).
Checkpoint intermediário: três `step` + `regs` → `call=[13]`.
