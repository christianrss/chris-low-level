#include "protocol.hpp"
#include <cassert>
#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    const DebugPacket original{
        DebugCommand::ReadMemory,
        42,
        {0x00, 0x10, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00},
    };

    const auto encoded = encode_debug_packet(original);
    const auto decoded = decode_debug_packet(encoded);
    assert(decoded.command == original.command);
    assert(decoded.request_id == original.request_id);
    assert(decoded.payload == original.payload);

    auto corrupted = encoded;
    corrupted.back() ^= 0xFFu;
    bool checksum_failed = false;
    try {
        (void)decode_debug_packet(corrupted);
    } catch (const std::runtime_error&) {
        checksum_failed = true;
    }
    assert(checksum_failed);

    bool truncated_failed = false;
    try {
        (void)decode_debug_packet({1, 2, 3});
    } catch (const std::runtime_error&) {
        truncated_failed = true;
    }
    assert(truncated_failed);

    std::cout << "chris-debugger protocol tests passed\n";
}
