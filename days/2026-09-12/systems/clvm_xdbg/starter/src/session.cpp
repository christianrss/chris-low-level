#include "session.hpp"

bool Session::load(const std::uint8_t* data, std::size_t n) {
    // TODO [XDBG-LOAD-01]: copy file bytes, call clvm_parse, set pc = entry
    (void)data;
    (void)n;
    last_error = "not implemented";
    loaded = false;
    return false;
}

std::string Session::hex_dump() const {
    // TODO [XDBG-HEX-01]: dump header 16 B then code, with offsets and region tags
    return {};
}

std::string Session::disasm() const {
    // TODO [XDBG-DISASM-01]: mnemonic at PC, including PUSH i32 and branch i16
    return {};
}

std::string Session::regs() const {
    // TODO [XDBG-REGS-01]: pc, status, data stack, call stack, prints, steps
    return {};
}

std::string Session::mem_view(std::size_t addr, std::size_t len) const {
    // TODO [XDBG-MEM-01]: hex of RAM 256 B starting at addr
    (void)addr;
    (void)len;
    return {};
}

DbgStatus Session::step() {
    // TODO [XDBG-STEP-01]: fetch/decode/execute one opcode; do not hide this in run()
    last_error = "not implemented";
    status = DbgStatus::Error;
    return status;
}

DbgStatus Session::cont() {
    // TODO [XDBG-BREAK-01]: step until HALT, breakpoint landing, or error
    return step();
}

bool Session::set_break(std::size_t at) {
    // TODO [XDBG-BREAK-01]: record a code PC breakpoint
    (void)at;
    return false;
}

// TODO [XDBG-ERR-01]: emit truncated / unknown opcode / stack underflow /
// memory out of bounds / return stack underflow from step()
