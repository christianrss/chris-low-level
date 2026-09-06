#include "crc32.hpp"

std::uint32_t crc32(const std::uint8_t* data, std::size_t len) {
    // TODO [COMP-ZLIB-04]: CRC32 IEEE (polinômio 0xEDB88320)
    return 0;
}

std::uint32_t crc32(const std::vector<std::uint8_t>& data) {
    return crc32(data.data(), data.size());
}
