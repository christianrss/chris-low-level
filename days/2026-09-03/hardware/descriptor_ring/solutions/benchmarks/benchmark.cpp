#include "descriptor_ring.hpp"
#include <chrono>
#include <cstdint>
#include <iostream>

int main() {
    DescriptorRing ring(256);
    constexpr std::uint64_t operations = 2'000'000;
    std::uint64_t completed = 0;
    const auto start = std::chrono::steady_clock::now();
    for (std::uint64_t i = 0; i < operations; ++i) {
        while (!ring.submit(1500)) {
            ring.device_complete_one();
            if (ring.reclaim()) ++completed;
        }
        ring.device_complete_one();
        if (ring.reclaim()) ++completed;
    }
    const auto end = std::chrono::steady_clock::now();
    const double seconds = std::chrono::duration<double>(end - start).count();
    std::cout << "completed=" << completed << " seconds=" << seconds
              << " desc/s=" << (completed / seconds) << "\n";
}
