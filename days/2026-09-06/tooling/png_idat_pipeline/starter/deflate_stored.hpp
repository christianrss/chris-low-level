#pragma once
#include <cstdint>
#include <vector>

std::vector<std::uint8_t> encode_stored_block(const std::vector<std::uint8_t>& data, bool final_block);
std::vector<std::uint8_t> decode_stored_blocks(const std::vector<std::uint8_t>& raw);
