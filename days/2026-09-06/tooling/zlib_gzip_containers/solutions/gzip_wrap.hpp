#pragma once
#include <cstdint>
#include <vector>

std::vector<std::uint8_t> gzip_compress(const std::vector<std::uint8_t>& data);
std::vector<std::uint8_t> gzip_decompress(const std::vector<std::uint8_t>& blob);
