#pragma once
#include <cstdint>
#include <vector>

std::uint32_t adler32(const std::uint8_t* data, std::size_t len);
std::uint32_t adler32(const std::vector<std::uint8_t>& data);
