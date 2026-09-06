// PEDAGOGY-SOLUTION: COMP-ZLIB-02
// PEDAGOGY-SOLUTION: COMP-ZLIB-03
#include "zlib_wrap.hpp"
#include "adler32.hpp"
#include "deflate_stored.hpp"
#include <stdexcept>

ZlibPacket zlib_compress(const std::vector<std::uint8_t>& data) {
    ZlibPacket pkt;
    pkt.cmf = 0x78;
    pkt.flg = 0x01;
    if (((pkt.cmf << 8) + pkt.flg) % 31 != 0) {
        throw std::runtime_error("bad zlib header checksum");
    }
    pkt.deflate_raw = encode_stored_block(data, true);
    pkt.adler_checksum = adler32(data);
    return pkt;
}

std::vector<std::uint8_t> zlib_blob_from_packet(const ZlibPacket& pkt) {
    std::vector<std::uint8_t> out{pkt.cmf, pkt.flg};
    out.insert(out.end(), pkt.deflate_raw.begin(), pkt.deflate_raw.end());
    out.push_back(static_cast<std::uint8_t>((pkt.adler_checksum >> 24) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((pkt.adler_checksum >> 16) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((pkt.adler_checksum >> 8) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>(pkt.adler_checksum & 0xFFu));
    return out;
}

std::vector<std::uint8_t> zlib_decompress(const std::vector<std::uint8_t>& blob) {
    if (blob.size() < 6) {
        throw std::runtime_error("zlib blob too small");
    }
    const std::uint8_t cmf = blob[0];
    const std::uint8_t flg = blob[1];
    if (((cmf << 8) + flg) % 31 != 0) {
        throw std::runtime_error("zlib header check failed");
    }
    if ((cmf & 0x0Fu) != 8) {
        throw std::runtime_error("only deflate method supported");
    }
    const auto adler = (static_cast<std::uint32_t>(blob[blob.size() - 4]) << 24) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 3]) << 16) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 2]) << 8) |
                       static_cast<std::uint32_t>(blob[blob.size() - 1]);
    std::vector<std::uint8_t> raw(blob.begin() + 2, blob.end() - 4);
    const auto data = decode_stored_blocks(raw);
    if (adler32(data) != adler) {
        throw std::runtime_error("adler32 mismatch");
    }
    return data;
}
