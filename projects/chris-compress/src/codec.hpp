#pragma once
#include <cstdint>
#include <span>
#include <vector>

bool encode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
bool decode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
bool zlib_compress_stored(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
bool zlib_decompress_stored(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out);
