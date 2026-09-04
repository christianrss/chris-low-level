// Reference CLVM interpreter: fetch, decode, execute and validate control flow.
#include "clvm_format.h"

#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {

constexpr std::size_t kMaxStack = 1024;
constexpr std::size_t kMaxSteps = 1'000'000;

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

const char* op_name(Op op) {
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
    }

    return "UNKNOWN";
}

bool pop_value(std::vector<std::int32_t>& stack, std::int32_t& value) {
    if (stack.empty()) {
        return false;
    }

    value = stack.back();
    stack.pop_back();
    return true;
}

void trace_state(
    std::size_t pc,
    Op op,
    const std::vector<std::int32_t>& stack) {

    std::cerr << "pc=" << pc << " op=" << op_name(op) << " stack=[";

    for (std::size_t i = 0; i < stack.size(); ++i) {
        if (i != 0) {
            std::cerr << ',';
        }
        std::cerr << stack[i];
    }

    std::cerr << "]\n";
}

int run(const clvm_image& image, bool trace) {
    std::vector<std::int32_t> stack;
    stack.reserve(64);

    std::size_t pc = image.entry;
    std::size_t steps = 0;

    const auto need = [&](std::size_t byte_count) {
        return pc + byte_count <= image.code_size;
    };

    const auto checked_jump = [&](std::int16_t relative) -> bool {
        // pc already points to the instruction after the jump operand.
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

        const std::size_t opcode_pc = pc;
        const Op op = static_cast<Op>(image.code[pc++]);

        if (trace) {
            trace_state(opcode_pc, op, stack);
        }

        std::int32_t lhs = 0;
        std::int32_t rhs = 0;

        switch (op) {
            case Op::Push:
                if (!need(4)) {
                    std::cerr << "error: truncated PUSH\n";
                    return 2;
                }
                if (stack.size() >= kMaxStack) {
                    std::cerr << "error: stack overflow\n";
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
                if (stack.empty()) {
                    std::cerr << "error: stack underflow\n";
                    return 2;
                }
                if (stack.size() >= kMaxStack) {
                    std::cerr << "error: stack overflow\n";
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

            default:
                std::cerr << "error: unknown opcode 0x"
                          << std::hex
                          << static_cast<unsigned>(op)
                          << std::dec
                          << " at pc="
                          << opcode_pc
                          << '\n';
                return 2;
        }
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
        std::istreambuf_iterator<char>()
    };

    clvm_image image{};
    char error[128]{};

    if (!clvm_parse(file.data(), file.size(), &image, error, sizeof(error))) {
        std::cerr << "parse error: " << error << '\n';
        return 1;
    }

    return run(image, trace);
}
