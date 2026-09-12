#include "clvm_format.h"

#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

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

// TODO [CLVM-EXT-03]: addr >= 0 && addr + 4 <= kMemSize
bool mem_in_bounds(std::int32_t addr) {
    return addr >= 0 && static_cast<std::size_t>(addr) + 4 <= kMemSize;
}

int run(const clvm_image& image, bool trace) {
    std::vector<std::int32_t> stack;
    std::vector<std::size_t> call_stack;
    std::array<std::uint8_t, kMemSize> mem{};
    stack.reserve(64);
    call_stack.reserve(16);

    std::size_t pc = image.entry;
    std::size_t steps = 0;

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

    while (pc < image.code_size) {
        if (++steps > kMaxSteps) {
            std::cerr << "error: step limit exceeded\n";
            return 2;
        }
        const Op op = static_cast<Op>(image.code[pc++]);
        std::int32_t lhs = 0;
        std::int32_t rhs = 0;

        switch (op) {
            case Op::Push:
                if (!need(4) || stack.size() >= kMaxStack) {
                    std::cerr << "error: bad PUSH\n";
                    return 2;
                }
                stack.push_back(read_i32_le(image.code + pc));
                pc += 4;
                break;
            case Op::Add:
            case Op::Sub:
            case Op::Mul:
            case Op::Div:
                if (!pop_value(stack, rhs) || !pop_value(stack, lhs)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                if (op == Op::Div && rhs == 0) {
                    std::cerr << "error: division by zero\n";
                    return 2;
                }
                if (op == Op::Add) {
                    stack.push_back(lhs + rhs);
                } else if (op == Op::Sub) {
                    stack.push_back(lhs - rhs);
                } else if (op == Op::Mul) {
                    stack.push_back(lhs * rhs);
                } else {
                    stack.push_back(lhs / rhs);
                }
                break;
            case Op::Dup:
                if (stack.empty() || stack.size() >= kMaxStack) {
                    std::cerr << "error: bad DUP\n";
                    return 2;
                }
                stack.push_back(stack.back());
                break;
            case Op::Print:
                if (!pop_value(stack, lhs)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                std::cout << lhs << '\n';
                break;
            case Op::Halt:
                return 0;
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
            case Op::Call: {
                // TODO [CLVM-EXT-02]: push return-PC; relative jump (como JMP)
                if (!need(2) || call_stack.size() >= kMaxCall) {
                    std::cerr << "error: bad CALL\n";
                }
                const std::int16_t relative = read_i16_le(image.code + pc);
                pc += 2;
                call_stack.push_back(pc);
                if (!checked_jump(relative)) {
                    std::cerr << "error: call outside code\n";
                    return 2;
                }
                break;
            }
            case Op::Ret: {
                // TODO [CLVM-EXT-02]: pop call_stack → pc; underflow → "return stack underflow"
                if (call_stack.empty()) {
                    std::cerr << "error: return stack underflow\n";
                    return 2;
                }
                pc = call_stack.back();
                call_stack.pop_back();
                break;
            }
            case Op::Store: {
                std::int32_t addr = 0;
                std::int32_t value = 0;
                if (!pop_value(stack, addr) || !pop_value(stack, value)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                if (!mem_in_bounds(addr)) {
                    std::cerr << "error: memory out of bounds\n";
                    return 2;
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
                if (!pop_value(stack, addr)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                if (!mem_in_bounds(addr)) {
                    std::cerr << "error: memory out of bounds\n";
                    return 2;
                }
                if (stack.size() >= kMaxStack) {
                    std::cerr << "error: stack overflow\n";
                    return 2;
                }
                stack.push_back(read_i32_le(mem.data() + static_cast<std::size_t>(addr)));
                break;
            }
            case Op::Drop:
                if (!pop_value(stack, lhs)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                break;
            case Op::Swap: {
                if (!pop_value(stack, rhs) || !pop_value(stack, lhs)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                stack.push_back(rhs);
                stack.push_back(lhs);
                break;
            }
            case Op::Eq:
            case Op::Lt:
                if (!pop_value(stack, rhs) || !pop_value(stack, lhs)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                if (op == Op::Eq) {
                    stack.push_back(lhs == rhs ? 1 : 0);
                } else {
                    stack.push_back(lhs < rhs ? 1 : 0);
                }
                break;
            case Op::Jnz: {
                if (!need(2)) {
                    std::cerr << "error: truncated JNZ\n";
                    return 2;
                }
                const std::int16_t relative = read_i16_le(image.code + pc);
                pc += 2;
                if (!pop_value(stack, lhs)) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                if (lhs != 0 && !checked_jump(relative)) {
                    std::cerr << "error: jump outside code\n";
                    return 2;
                }
                break;
            }
            default:
                std::cerr << "error: unknown opcode\n";
                return 2;
        }
        (void)trace;
    }
    std::cerr << "error: execution reached end without HALT\n";
    return 2;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2 || argc > 3) {
        std::cerr << "usage: clvm <program.clvm> [--trace]\n";
        return 1;
    }
    const bool trace = argc == 3 && std::string(argv[2]) == "--trace";
    std::ifstream input(argv[1], std::ios::binary);
    if (!input) {
        std::cerr << "error: cannot open file\n";
        return 1;
    }
    const std::vector<std::uint8_t> file{
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()};
    clvm_image image{};
    char error[128]{};
    if (!clvm_parse(file.data(), file.size(), &image, error, sizeof(error))) {
        std::cerr << "parse error: " << error << '\n';
        return 1;
    }
    return run(image, trace);
}
