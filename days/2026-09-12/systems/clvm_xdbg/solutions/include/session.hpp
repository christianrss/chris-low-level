#pragma once

#include "clvm_format.h"

#include <array>
#include <cstddef>
#include <cstdint>
#include <set>
#include <string>
#include <vector>

enum class DbgStatus {
    Ready = 0,
    Halted = 1,
    Breakpoint = 2,
    Error = 3
};

struct Session {
    std::vector<std::uint8_t> file;
    clvm_image image{};
    bool loaded = false;
    std::size_t pc = 0;
    std::vector<std::int32_t> data_stack;
    std::vector<std::size_t> call_stack;
    std::array<std::uint8_t, 256> mem{};
    std::set<std::size_t> breaks;
    std::vector<std::int32_t> prints;
    std::string last_error;
    DbgStatus status = DbgStatus::Ready;
    std::size_t steps = 0;

    bool load(const std::uint8_t* data, std::size_t n);
    std::string hex_dump() const;
    std::string disasm() const;
    std::string regs() const;
    std::string mem_view(std::size_t addr, std::size_t len) const;
    DbgStatus step();
    DbgStatus cont();
    bool set_break(std::size_t at);
};
