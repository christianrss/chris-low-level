#pragma once
#include <cstdint>
#include <vector>

enum class DebugCommand : std::uint16_t {
    Ping = 1,
    ReadRegisters = 2,
    ReadMemory = 3,
    ContinueExecution = 4,
    BreakExecution = 5,
};

struct DebugPacket {
    DebugCommand command = DebugCommand::Ping;
    std::uint32_t request_id = 0;
    std::vector<std::uint8_t> payload;
};

std::vector<std::uint8_t> encode_debug_packet(const DebugPacket& packet);
DebugPacket decode_debug_packet(const std::vector<std::uint8_t>& bytes);
