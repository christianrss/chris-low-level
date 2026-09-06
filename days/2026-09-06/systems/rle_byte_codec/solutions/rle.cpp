#include "rle.hpp"
#include <cstring>

// PEDAGOGY-SOLUTION: COMP-RLE-01
// PEDAGOGY-SOLUTION: COMP-RLE-02
// PEDAGOGY-SOLUTION: COMP-RLE-03

bool encode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    out.insert(out.end(), CHRLE_MAGIC, CHRLE_MAGIC + 5);
    const std::uint32_t len = static_cast<std::uint32_t>(input.size());
    out.push_back(static_cast<std::uint8_t>(len & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 24) & 0xFF));
    std::size_t i = 0;
    while (i < input.size()) {
        std::size_t j = i + 1;
        while (j < input.size() && input[j] == input[i] && (j - i) < 255) {
            ++j;
        }
        const std::uint8_t count = static_cast<std::uint8_t>(j - i);
        out.push_back(count);
        out.push_back(input[i]);
        i = j;
    }
    return true;
}

bool decode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    if (input.size() < 9 || std::memcmp(input.data(), CHRLE_MAGIC, 5) != 0) {
        return false;
    }
    std::uint32_t len = 0;
    len |= input[5];
    len |= static_cast<std::uint32_t>(input[6]) << 8;
    len |= static_cast<std::uint32_t>(input[7]) << 16;
    len |= static_cast<std::uint32_t>(input[8]) << 24;
    out.reserve(len);
    std::size_t p = 9;
    while (p + 1 < input.size() && out.size() < len) {
        const std::uint8_t count = input[p++];
        const std::uint8_t value = input[p++];
        for (std::uint8_t k = 0; k < count && out.size() < len; ++k) {
            out.push_back(value);
        }
    }
    return out.size() == len;
}
