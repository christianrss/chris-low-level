#pragma once
#include <cstdint>
#include <vector>

std::vector<std::uint8_t> zlib_min_compress(const std::vector<std::uint8_t>& data);
std::vector<std::uint8_t> zlib_min_decompress(const std::vector<std::uint8_t>& blob);
