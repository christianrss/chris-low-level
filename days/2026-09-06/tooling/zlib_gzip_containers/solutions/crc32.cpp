// PEDAGOGY-SOLUTION: COMP-ZLIB-04
#include "crc32.hpp"

namespace {
std::uint32_t table[256];
bool table_init = false;

void init_table() {
    for (std::uint32_t i = 0; i < 256; ++i) {
        std::uint32_t c = i;
        for (int k = 0; k < 8; ++k) {
            c = (c & 1u) ? (0xEDB88320u ^ (c >> 1)) : (c >> 1);
        }
        table[i] = c;
    }
    table_init = true;
}
}  // namespace

std::uint32_t crc32(const std::uint8_t* data, std::size_t len) {
    if (!table_init) {
        init_table();
    }
    std::uint32_t crc = 0xFFFFFFFFu;
    for (std::size_t i = 0; i < len; ++i) {
        crc = table[(crc ^ data[i]) & 0xFFu] ^ (crc >> 8);
    }
    return crc ^ 0xFFFFFFFFu;
}

std::uint32_t crc32(const std::vector<std::uint8_t>& data) {
    return crc32(data.data(), data.size());
}
