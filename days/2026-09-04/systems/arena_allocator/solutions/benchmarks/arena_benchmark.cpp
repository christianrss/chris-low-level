#include "arena.hpp"
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <memory>
#include <vector>

int main() {
    constexpr std::size_t allocations = 100000;
    constexpr std::size_t block_size = 64;
    constexpr int repetitions = 20;

    std::uint64_t checksum = 0;
    Arena arena(allocations * block_size + 4096);

    const auto arena_start = std::chrono::steady_clock::now();
    for (int rep = 0; rep < repetitions; ++rep) {
        arena.reset();
        for (std::size_t i = 0; i < allocations; ++i) {
            auto* p = static_cast<std::byte*>(arena.allocate(block_size, 16));
            p[0] = static_cast<std::byte>(i & 0xFFu);
            checksum += static_cast<unsigned char>(p[0]);
        }
    }
    const auto arena_end = std::chrono::steady_clock::now();

    const auto heap_start = std::chrono::steady_clock::now();
    for (int rep = 0; rep < repetitions; ++rep) {
        std::vector<std::unique_ptr<std::byte[]>> blocks;
        blocks.reserve(allocations);
        for (std::size_t i = 0; i < allocations; ++i) {
            auto p = std::make_unique<std::byte[]>(block_size);
            p[0] = static_cast<std::byte>(i & 0xFFu);
            checksum += static_cast<unsigned char>(p[0]);
            blocks.push_back(std::move(p));
        }
    }
    const auto heap_end = std::chrono::steady_clock::now();

    const auto arena_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
        arena_end - arena_start).count();
    const auto heap_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
        heap_end - heap_start).count();

    std::cout << "allocations=" << allocations * repetitions
              << " arena_ns=" << arena_ns
              << " heap_ns=" << heap_ns
              << " checksum=" << checksum << "\n";
}
