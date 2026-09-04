// PEDAGOGY-SOLUTION: CPU-STEP-01

#include "cpu.hpp"
#include <algorithm>
#include <stdexcept>

TinyCpu::TinyCpu(std::size_t memory_size) : memory_(memory_size, 0) {
    if (memory_size == 0 || memory_size > 65536) {
        throw std::invalid_argument("memory size must be between 1 and 65536 bytes");
    }
}

void TinyCpu::reset() {
    regs_.fill(0);
    pc_ = 0;
    halted_ = false;
}

void TinyCpu::load_program(const std::vector<std::uint8_t>& program, std::uint16_t base) {
    const std::size_t start = base;
    if (start + program.size() > memory_.size()) {
        throw std::out_of_range("program does not fit in memory");
    }
    std::copy(program.begin(), program.end(), memory_.begin() + static_cast<std::ptrdiff_t>(start));
    pc_ = base;
    halted_ = false;
}

std::uint8_t TinyCpu::fetch8() {
    if (pc_ >= memory_.size()) {
        throw std::out_of_range("program counter outside memory");
    }
    return memory_[pc_++];
}

std::uint16_t TinyCpu::fetch16() {
    const std::uint16_t lo = fetch8();
    const std::uint16_t hi = fetch8();
    return static_cast<std::uint16_t>(lo | (hi << 8));
}

std::size_t TinyCpu::checked_reg(std::uint8_t raw) const {
    if (raw >= regs_.size()) {
        throw std::runtime_error("invalid register index");
    }
    return raw;
}

bool TinyCpu::step() {
    if (halted_) {
        return false;
    }

    const auto op = static_cast<Op>(fetch8());
    switch (op) {
    case Op::Nop:
        break;
    case Op::MovI: {
        const auto dst = checked_reg(fetch8());
        regs_[dst] = fetch16();
        break;
    }
    case Op::Add: {
        const auto dst = checked_reg(fetch8());
        const auto src = checked_reg(fetch8());
        regs_[dst] = static_cast<std::uint16_t>(regs_[dst] + regs_[src]);
        break;
    }
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
    case Op::Load: {
        const auto dst = checked_reg(fetch8());
        const auto addr = fetch16();
        if (static_cast<std::size_t>(addr) + 1 >= memory_.size()) {
            throw std::out_of_range("load outside memory");
        }
        regs_[dst] = static_cast<std::uint16_t>(memory_[addr] | (memory_[addr + 1] << 8));
        break;
    }
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
    case Op::Halt:
        halted_ = true;
        return false;
    default:
        throw std::runtime_error("unknown opcode");
    }
    return true;
}

void TinyCpu::run(std::size_t max_steps) {
    std::size_t steps = 0;
    while (!halted_) {
        if (steps++ >= max_steps) {
            throw std::runtime_error("step limit exceeded");
        }
        step();
    }
}

std::uint16_t TinyCpu::reg(std::size_t index) const {
    if (index >= regs_.size()) {
        throw std::out_of_range("register outside range");
    }
    return regs_[index];
}

std::uint8_t TinyCpu::memory(std::uint16_t address) const {
    if (address >= memory_.size()) {
        throw std::out_of_range("memory address outside range");
    }
    return memory_[address];
}
