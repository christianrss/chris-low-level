#include "codec.hpp"

static std::uint32_t adler32(std::span<const std::uint8_t> data) {
    std::uint32_t s1 = 1, s2 = 0;
    for (auto b : data) {
        s1 = (s1 + b) % 65521;
        s2 = (s2 + s1) % 65521;
    }
    return (s2 << 16) | s1;
}

bool zlib_compress_stored(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out = {0x78, 0x01, 0x01};
    const std::uint16_t len = static_cast<std::uint16_t>(input.size());
    out.push_back(static_cast<std::uint8_t>(len & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 8) & 0xFF));
    const std::uint16_t nlen = static_cast<std::uint16_t>(~len);
    out.push_back(static_cast<std::uint8_t>(nlen & 0xFF));
    out.push_back(static_cast<std::uint8_t>((nlen >> 8) & 0xFF));
    out.insert(out.end(), input.begin(), input.end());
    const auto checksum = adler32(input);
    out.push_back(static_cast<std::uint8_t>((checksum >> 24) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((checksum >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((checksum >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>(checksum & 0xFF));
    return true;
}

bool zlib_decompress_stored(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    if (input.size() < 10 || input[0] != 0x78) return false;
    std::size_t p = 2;
    if (input[p] != 0x01) return false;
    ++p;
    const std::uint16_t len = input[p] | (static_cast<std::uint16_t>(input[p + 1]) << 8);
    p += 4;
    if (p + len + 4 > input.size()) return false;
    out.assign(input.begin() + static_cast<std::ptrdiff_t>(p),
               input.begin() + static_cast<std::ptrdiff_t>(p + len));
    return true;
}
