#include "cpu.hpp"
#include <chrono>
#include <cstdint>
#include <iostream>
#include <vector>

static std::uint8_t op(TinyCpu::Op value) {
    return static_cast<std::uint8_t>(value);
}

int main() {
    constexpr int runs = 5000;
    std::vector<std::uint8_t> program;
    program.reserve(4 + 3 * 128 + 1);
    program.insert(program.end(), {op(TinyCpu::Op::MovI), 0, 1, 0});
    for (int i = 0; i < 128; ++i) {
        program.insert(program.end(), {op(TinyCpu::Op::Add), 0, 0});
    }
    program.push_back(op(TinyCpu::Op::Halt));

    const auto start = std::chrono::steady_clock::now();
    std::uint64_t checksum = 0;
    for (int i = 0; i < runs; ++i) {
        TinyCpu cpu;
        cpu.load_program(program);
        cpu.run();
        checksum += cpu.reg(0);
    }
    const auto end = std::chrono::steady_clock::now();
    const auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
    const double instructions = static_cast<double>(runs) * 130.0;
    std::cout << "instructions=" << instructions << " ns=" << ns
              << " MIPS=" << (instructions / static_cast<double>(ns) * 1000.0)
              << " checksum=" << checksum << "\n";
}
