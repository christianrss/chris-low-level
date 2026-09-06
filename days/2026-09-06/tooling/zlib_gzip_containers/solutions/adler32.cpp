// PEDAGOGY-SOLUTION: COMP-ZLIB-01
#include "adler32.hpp"

std::uint32_t adler32(const std::uint8_t* data, std::size_t len) {
    std::uint32_t s1 = 1;
    std::uint32_t s2 = 0;
    for (std::size_t i = 0; i < len; ++i) {
        s1 = (s1 + data[i]) % 65521u;
        s2 = (s2 + s1) % 65521u;
    }
    return (s2 << 16) | s1;
}

std::uint32_t adler32(const std::vector<std::uint8_t>& data) {
    return adler32(data.data(), data.size());
}
