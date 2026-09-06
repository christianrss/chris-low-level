#pragma once
#include <cstdint>
#include <span>
#include <vector>

inline constexpr char CHLZ7_MAGIC[6] = "CHLZ7";
constexpr std::size_t LZ77_WINDOW_SIZE = 32768;
constexpr std::size_t LZ77_MIN_MATCH = 3;
constexpr std::size_t LZ77_MAX_MATCH = 255;

struct LZ77Match {
    std::uint16_t offset = 0;
    std::uint8_t length = 0;
};

bool find_longest_match(std::span<const std::uint8_t> data, std::size_t pos, LZ77Match& match);
bool encode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
bool decode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
