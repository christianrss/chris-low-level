#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <vector>

class TinyCpu {
public:
    enum class Op : std::uint8_t {
        Nop = 0x00,
        MovI = 0x10,
        Add = 0x20,
        Store = 0x30,
        Load = 0x31,
        Jnz = 0x40,
        Halt = 0xFF,
    };

    explicit TinyCpu(std::size_t memory_size = 65536);
    void reset();
    void load_program(const std::vector<std::uint8_t>& program, std::uint16_t base = 0);
    bool step();
    void run(std::size_t max_steps = 1'000'000);
    std::uint16_t reg(std::size_t index) const;
    std::uint8_t memory(std::uint16_t address) const;
    std::uint16_t pc() const { return pc_; }
    bool halted() const { return halted_; }

private:
    std::uint8_t fetch8();
    std::uint16_t fetch16();
    std::size_t checked_reg(std::uint8_t raw) const;

    std::vector<std::uint8_t> memory_;
    std::array<std::uint16_t, 4> regs_{};
    std::uint16_t pc_ = 0;
    bool halted_ = false;
};
