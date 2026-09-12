#include "session.hpp"

#include <algorithm>
#include <iomanip>
#include <sstream>
#include <string>

namespace {

constexpr std::size_t kMaxStack = 1024;
constexpr std::size_t kMaxCall = 256;
constexpr std::size_t kMaxSteps = 1'000'000;
constexpr std::size_t kMemSize = 256;

enum class Op : std::uint8_t {
    Push = 0x01,
    Add = 0x02,
    Sub = 0x03,
    Mul = 0x04,
    Div = 0x05,
    Dup = 0x06,
    Print = 0x07,
    Halt = 0x08,
    Jmp = 0x09,
    Jz = 0x0A,
    Call = 0x0B,
    Ret = 0x0C,
    Load = 0x0D,
    Store = 0x0E,
    Drop = 0x0F,
    Swap = 0x10,
    Eq = 0x11,
    Lt = 0x12,
    Jnz = 0x13,
};

std::int32_t read_i32_le(const std::uint8_t* bytes) {
    const std::uint32_t value =
        static_cast<std::uint32_t>(bytes[0]) |
        (static_cast<std::uint32_t>(bytes[1]) << 8U) |
        (static_cast<std::uint32_t>(bytes[2]) << 16U) |
        (static_cast<std::uint32_t>(bytes[3]) << 24U);
    return static_cast<std::int32_t>(value);
}

std::int16_t read_i16_le(const std::uint8_t* bytes) {
    const std::uint16_t value =
        static_cast<std::uint16_t>(bytes[0]) |
        (static_cast<std::uint16_t>(bytes[1]) << 8U);
    return static_cast<std::int16_t>(value);
}

bool pop_value(std::vector<std::int32_t>& stack, std::int32_t& value) {
    if (stack.empty()) {
        return false;
    }
    value = stack.back();
    stack.pop_back();
    return true;
}

bool mem_in_bounds(std::int32_t addr) {
    return addr >= 0 && static_cast<std::size_t>(addr) + 4 <= kMemSize;
}

const char* status_name(DbgStatus status) {
    switch (status) {
        case DbgStatus::Ready:
            return "ready";
        case DbgStatus::Halted:
            return "halted";
        case DbgStatus::Breakpoint:
            return "breakpoint";
        case DbgStatus::Error:
            return "error";
    }
    return "error";
}

std::size_t operand_bytes(Op op) {
    if (op == Op::Push) {
        return 4;
    }
    if (op == Op::Jmp || op == Op::Jz || op == Op::Call || op == Op::Jnz) {
        return 2;
    }
    return 0;
}

const char* mnemonic(Op op) {
    switch (op) {
        case Op::Push:
            return "PUSH";
        case Op::Add:
            return "ADD";
        case Op::Sub:
            return "SUB";
        case Op::Mul:
            return "MUL";
        case Op::Div:
            return "DIV";
        case Op::Dup:
            return "DUP";
        case Op::Print:
            return "PRINT";
        case Op::Halt:
            return "HALT";
        case Op::Jmp:
            return "JMP";
        case Op::Jz:
            return "JZ";
        case Op::Call:
            return "CALL";
        case Op::Ret:
            return "RET";
        case Op::Load:
            return "LOAD";
        case Op::Store:
            return "STORE";
        case Op::Drop:
            return "DROP";
        case Op::Swap:
            return "SWAP";
        case Op::Eq:
            return "EQ";
        case Op::Lt:
            return "LT";
        case Op::Jnz:
            return "JNZ";
    }
    return "?";
}

std::string hex_byte(std::uint8_t value) {
    std::ostringstream out;
    out << std::uppercase << std::hex << std::setw(2) << std::setfill('0')
        << static_cast<unsigned>(value);
    return out.str();
}

std::string hex_offset(std::size_t value) {
    std::ostringstream out;
    out << std::uppercase << std::hex << std::setw(4) << std::setfill('0') << value;
    return out.str();
}

std::string format_i32_list(const std::vector<std::int32_t>& values) {
    std::ostringstream out;
    out << '[';
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i != 0) {
            out << ',';
        }
        out << values[i];
    }
    out << ']';
    return out.str();
}

std::string format_size_list(const std::vector<std::size_t>& values) {
    std::ostringstream out;
    out << '[';
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i != 0) {
            out << ',';
        }
        out << values[i];
    }
    out << ']';
    return out.str();
}

}  // namespace

// PEDAGOGY-SOLUTION: XDBG-LOAD-01
bool Session::load(const std::uint8_t* data, std::size_t n) {
    file.assign(data, data + n);
    mem.fill(0);
    data_stack.clear();
    call_stack.clear();
    prints.clear();
    breaks.clear();
    steps = 0;
    status = DbgStatus::Ready;
    last_error.clear();
    loaded = false;

    char error[128]{};
    if (!clvm_parse(file.data(), file.size(), &image, error, sizeof(error))) {
        last_error = error;
        status = DbgStatus::Error;
        return false;
    }
    pc = image.entry;
    loaded = true;
    return true;
}

// PEDAGOGY-SOLUTION: XDBG-HEX-01
std::string Session::hex_dump() const {
    if (file.empty()) {
        return {};
    }
    std::ostringstream out;
    for (std::size_t offset = 0; offset < file.size(); offset += 16) {
        out << hex_offset(offset) << "  ";
        const std::size_t line_end = std::min(offset + 16, file.size());
        for (std::size_t i = offset; i < line_end; ++i) {
            if (i != offset) {
                out << ' ';
            }
            out << hex_byte(file[i]);
        }
        const char* region = offset < CLVM_HEADER_SIZE ? "header" : "code";
        out << "  " << region << '\n';
    }
    return out.str();
}

// PEDAGOGY-SOLUTION: XDBG-DISASM-01
std::string Session::disasm() const {
    if (!loaded || pc >= image.code_size) {
        std::ostringstream out;
        out << "pc=" << pc << " <end>";
        return out.str();
    }
    const Op op = static_cast<Op>(image.code[pc]);
    const std::size_t extra = operand_bytes(op);
    std::ostringstream out;
    out << "pc=" << pc << ' ' << mnemonic(op);
    if (extra == 4) {
        if (pc + 1 + extra > image.code_size) {
            out << " <truncated>";
        } else {
            out << ' ' << read_i32_le(image.code + pc + 1);
        }
    } else if (extra == 2) {
        if (pc + 1 + extra > image.code_size) {
            out << " <truncated>";
        } else {
            const std::int16_t rel = read_i16_le(image.code + pc + 1);
            out << ' ' << std::showpos << rel;
        }
    }
    return out.str();
}

// PEDAGOGY-SOLUTION: XDBG-REGS-01
std::string Session::regs() const {
    std::ostringstream out;
    out << "pc=" << pc << '\n';
    out << "status=" << status_name(status) << '\n';
    out << "data=" << format_i32_list(data_stack) << '\n';
    out << "call=" << format_size_list(call_stack) << '\n';
    out << "prints=" << format_i32_list(prints) << '\n';
    out << "steps=" << steps << '\n';
    if (status == DbgStatus::Error && !last_error.empty()) {
        out << "error=" << last_error << '\n';
    }
    return out.str();
}

// PEDAGOGY-SOLUTION: XDBG-MEM-01
std::string Session::mem_view(std::size_t addr, std::size_t len) const {
    if (addr >= kMemSize) {
        return {};
    }
    if (len > kMemSize - addr) {
        len = kMemSize - addr;
    }
    std::ostringstream out;
    for (std::size_t offset = 0; offset < len; offset += 16) {
        out << hex_offset(addr + offset) << "  ";
        const std::size_t line_end = std::min(offset + 16, len);
        for (std::size_t i = offset; i < line_end; ++i) {
            if (i != offset) {
                out << ' ';
            }
            out << hex_byte(mem[addr + i]);
        }
        out << '\n';
    }
    return out.str();
}

bool Session::set_break(std::size_t at) {
    breaks.insert(at);
    return true;
}

namespace {

DbgStatus fail(Session& session, const char* message) {
    session.last_error = message;
    session.status = DbgStatus::Error;
    return session.status;
}

}  // namespace

// PEDAGOGY-SOLUTION: XDBG-ERR-01
// PEDAGOGY-SOLUTION: XDBG-STEP-01
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

// PEDAGOGY-SOLUTION: XDBG-BREAK-01
DbgStatus Session::cont() {
    if (status == DbgStatus::Breakpoint) {
        status = DbgStatus::Ready;
    }
    bool first = true;
    while (status == DbgStatus::Ready) {
        if (!first && breaks.count(pc) != 0) {
            status = DbgStatus::Breakpoint;
            return status;
        }
        first = false;
        step();
    }
    return status;
}
