#include "gzip_wrap.hpp"
#include "crc32.hpp"
#include "deflate_stored.hpp"
#include <stdexcept>

std::vector<std::uint8_t> gzip_compress(const std::vector<std::uint8_t>& data) {
    // TODO [COMP-ZLIB-04]: header gzip + deflate stored + CRC32 LE + ISIZE LE
    return {};
}

std::vector<std::uint8_t> gzip_decompress(const std::vector<std::uint8_t>& blob) {
    // TODO [COMP-ZLIB-04]: parse trailer e validar CRC32/ISIZE
    return {};
}
