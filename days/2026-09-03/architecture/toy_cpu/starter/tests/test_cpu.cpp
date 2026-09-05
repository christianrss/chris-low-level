// PEDAGOGY-TEST: CPU-STEP-01
// Test cases (TESTES_GUIADOS.md):
// Caso 1: Escreva um teste do comportamento mais simples antes de adicionar a feature.
// Caso 2: Rode e observe a falha.
// Caso 3: Implemente apenas o necessario para esse teste.
// Caso 4: Adicione edge case/erro relevante.
// Caso 5: Quando encontrar um bug durante o exercicio, transforme-o em regression test ant
#include "cpu.hpp"
#include <cassert>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

static std::uint8_t op(TinyCpu::Op value) {
    return static_cast<std::uint8_t>(value);
}

int main() {
    {
        TinyCpu cpu;
        std::vector<std::uint8_t> program = {
            op(TinyCpu::Op::MovI), 0, 5, 0,
            op(TinyCpu::Op::MovI), 1, 7, 0,
            op(TinyCpu::Op::Add), 0, 1,
            op(TinyCpu::Op::Halt),
        };
        cpu.load_program(program);
        cpu.run();
        assert(cpu.reg(0) == 12);
    }

    {
        TinyCpu cpu;
        std::vector<std::uint8_t> program = {
            op(TinyCpu::Op::MovI), 2, 0x34, 0x12,
            op(TinyCpu::Op::Store), 2, 0x00, 0x01,
            op(TinyCpu::Op::Load), 3, 0x00, 0x01,
            op(TinyCpu::Op::Halt),
        };
        cpu.load_program(program);
        cpu.run();
        assert(cpu.reg(3) == 0x1234);
        assert(cpu.memory(0x0100) == 0x34);
        assert(cpu.memory(0x0101) == 0x12);
    }


    {
        TinyCpu cpu;
        std::vector<std::uint8_t> program = {
            op(TinyCpu::Op::MovI), 0, 1, 0,        // 0..3
            op(TinyCpu::Op::Jnz), 0, 12, 0,       // 4..7 -> jump to HALT at 12
            op(TinyCpu::Op::MovI), 1, 99, 0,      // 8..11 must be skipped
            op(TinyCpu::Op::Halt),                 // 12
        };
        cpu.load_program(program);
        cpu.run();
        assert(cpu.reg(1) == 0);
        assert(cpu.pc() == 13);
    }

    {
        TinyCpu cpu;
        bool threw = false;
        try {
            cpu.load_program({0x7E});
            cpu.step();
        } catch (const std::runtime_error&) {
            threw = true;
        }
        assert(threw);
    }

    std::cout << "chris-cpu tests passed\n";
}