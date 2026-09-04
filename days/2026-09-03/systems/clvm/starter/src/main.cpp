#include "clvm_format.h"

#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {

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
    // Reconstruct explicitly so the file format is independent of host endian.
    const std::uint32_t value =
        static_cast<std::uint32_t>(bytes[0]) |
        (static_cast<std::uint32_t>(bytes[1]) << 8U) |
        (static_cast<std::uint32_t>(bytes[2]) << 16U) |
        (static_cast<std::uint32_t>(bytes[3]) << 24U);

    return static_cast<std::int32_t>(value);
}

int run(const clvm_image& image, bool trace) {
    std::vector<std::int32_t> stack;
    std::size_t pc = image.entry;

    while (pc < image.code_size) {
        const std::size_t opcode_pc = pc;
        const std::uint8_t opcode = image.code[pc++];

        if (trace) {
            std::cerr << "pc=" << opcode_pc
                      << " op=0x" << std::hex << static_cast<unsigned>(opcode)
                      << std::dec << " depth=" << stack.size() << '\n';
        }

        switch (static_cast<Op>(opcode)) {
            case Op::Push:
                if (pc + 4 > image.code_size) {
                    std::cerr << "truncated PUSH\n";
                    return 2;
                }
                stack.push_back(read_i32_le(image.code + pc));
                pc += 4;
                break;

            case Op::Halt:
                return 0;

            // TODO [CLVM-VM-ARITH-01]: implement ADD/SUB/MUL/DIV/DUP/PRINT with checks.
            // TODO [CLVM-VM-JUMP-01]: implement JMP/JZ with signed i16 relative offsets.
            default:
                std::cerr << "unimplemented/unknown opcode at pc="
                          << opcode_pc << '\n';
                return 2;
        }
    }

    std::cerr << "reached end without HALT\n";
    return 2;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "usage: clvm <program.clvm> [--trace]\n";
        return 1;
    }

    const bool trace = argc > 2 && std::string(argv[2]) == "--trace";
    std::ifstream input(argv[1], std::ios::binary);
    if (!input) {
        std::cerr << "cannot open input file\n";
        return 1;
    }

    std::vector<std::uint8_t> file{
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
