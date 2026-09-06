#include "zlib_wrap.hpp"
#include "adler32.hpp"
#include "deflate_stored.hpp"
#include <stdexcept>

ZlibPacket zlib_compress(const std::vector<std::uint8_t>& data) {
    // TODO [COMP-ZLIB-02]: CMF/FLG + deflate stored + Adler32 BE
    return {};
}

std::vector<std::uint8_t> zlib_blob_from_packet(const ZlibPacket& pkt) {
    // TODO [COMP-ZLIB-02]: serializar CMF/FLG + deflate + Adler32 BE
    return {};
}

std::vector<std::uint8_t> zlib_decompress(const std::vector<std::uint8_t>& blob) {
    // TODO [COMP-ZLIB-03]: validar header, inflar stored, checar Adler32
    return {};
}
