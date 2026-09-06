#include "codec.hpp"
#include <cstring>

namespace {
constexpr char kMagic[6] = "CHRLE";
}

bool encode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.assign(kMagic, kMagic + 5);
    const std::uint32_t len = static_cast<std::uint32_t>(input.size());
    for (int i = 0; i < 4; ++i) out.push_back(static_cast<std::uint8_t>((len >> (8 * i)) & 0xFF));
    for (std::size_t i = 0; i < input.size();) {
        std::size_t j = i + 1;
        while (j < input.size() && input[j] == input[i] && j - i < 255) ++j;
        out.push_back(static_cast<std::uint8_t>(j - i));
        out.push_back(input[i]);
        i = j;
    }
    return true;
}

bool decode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    if (input.size() < 9 || std::memcmp(input.data(), kMagic, 5) != 0) return false;
    std::uint32_t len = 0;
    for (int i = 0; i < 4; ++i) len |= static_cast<std::uint32_t>(input[5 + i]) << (8 * i);
    std::size_t p = 9;
    while (p + 1 < input.size() && out.size() < len) {
        const auto count = input[p++];
        const auto value = input[p++];
        for (std::uint8_t k = 0; k < count && out.size() < len; ++k) out.push_back(value);
    }
    return out.size() == len;
}
