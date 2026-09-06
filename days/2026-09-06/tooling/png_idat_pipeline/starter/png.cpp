#include "png.hpp"
#include "zlib_min.hpp"
#include <cstring>
#include <stdexcept>

std::uint32_t png_chunk_crc(const char* type, const std::vector<std::uint8_t>& data) {
    // TODO [COMP-PNG-01]: CRC32 sobre type+data
    return 0;
}

std::vector<std::uint8_t> png_chunk(const char* type, const std::vector<std::uint8_t>& data) {
    // TODO [COMP-PNG-01]: length BE + type + data + crc BE
    return {};
}

std::vector<std::uint8_t> build_ihdr(const PngImage& spec) {
    // TODO [COMP-PNG-02]: 13 bytes IHDR (width/height BE, bit depth, color type)
    return {};
}

std::vector<std::uint8_t> filter_none_scanlines(const PngImage& img) {
    // TODO [COMP-PNG-03]: prefix 0 por linha + pixels
    return {};
}

std::vector<std::uint8_t> encode_png(const PngImage& img) {
    // TODO [COMP-PNG-04]: assinatura + IHDR + IDAT zlib + IEND
    return {};
}

PngImage decode_png(const std::vector<std::uint8_t>& blob) {
    // TODO [COMP-PNG-04]: parse chunks e reconstruir pixels
    return {};
}
