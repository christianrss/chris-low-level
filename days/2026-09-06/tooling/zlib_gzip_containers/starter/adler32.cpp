#include "adler32.hpp"

std::uint32_t adler32(const std::uint8_t* data, std::size_t len) {
    // TODO [COMP-ZLIB-01]: RFC1950 Adler32 com mod 65521
    return 0;
}

std::uint32_t adler32(const std::vector<std::uint8_t>& data) {
    return adler32(data.data(), data.size());
}
