#pragma once
#include <cstdint>
#include <span>
#include <vector>

inline constexpr char CHHUF_MAGIC[6] = "CHHUF";

struct HuffmanCodeEntry {
    std::uint8_t symbol = 0;
    std::uint8_t bit_length = 0;
    std::uint16_t code = 0;
};

bool build_huffman_codes(const std::uint32_t freq[256], std::vector<HuffmanCodeEntry>& table);
bool encode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
bool decode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
