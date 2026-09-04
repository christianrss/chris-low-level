#include "protocol.hpp"
#include <chrono>
#include <cstdint>
#include <iostream>

int main() {
    constexpr int packets = 300000;
    DebugPacket packet{DebugCommand::ReadRegisters, 7, std::vector<std::uint8_t>(64, 0x5A)};
    std::uint64_t checksum = 0;

    const auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < packets; ++i) {
        packet.request_id = static_cast<std::uint32_t>(i);
        const auto bytes = encode_debug_packet(packet);
        const auto decoded = decode_debug_packet(bytes);
        checksum += decoded.request_id;
    }
    const auto end = std::chrono::steady_clock::now();
    const double seconds = std::chrono::duration<double>(end - start).count();
    std::cout << "packets=" << packets
              << " seconds=" << seconds
              << " packets_per_s=" << packets / seconds
              << " checksum=" << checksum << "\n";
}
