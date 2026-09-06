#pragma once
#include <cstdint>
#include <string>
#include <vector>

struct FixedLitTables {
    std::uint16_t code[288]{};
    std::uint8_t len[288]{};
};

FixedLitTables build_fixed_literal_tables();

std::vector<std::uint8_t> encode_stored_block(const std::vector<std::uint8_t>& data, bool final_block);
std::vector<std::uint8_t> decode_stored_blocks(const std::vector<std::uint8_t>& raw);

std::vector<std::uint8_t> encode_fixed_block(const std::vector<std::uint8_t>& literals, bool final_block);
std::vector<std::uint8_t> decode_fixed_block(const std::vector<std::uint8_t>& raw);
