#pragma once
#include <cstdint>
#include <span>
#include <vector>

inline constexpr char CHRLE_MAGIC[6] = "CHRLE";

bool encode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
bool decode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
