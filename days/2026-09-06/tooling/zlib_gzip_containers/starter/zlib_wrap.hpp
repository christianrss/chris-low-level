#pragma once
#include <cstdint>
#include <vector>

struct ZlibPacket {
    std::uint8_t cmf{0};
    std::uint8_t flg{0};
    std::vector<std::uint8_t> deflate_raw;
    std::uint32_t adler_checksum{0};
};

ZlibPacket zlib_compress(const std::vector<std::uint8_t>& data);
std::vector<std::uint8_t> zlib_blob_from_packet(const ZlibPacket& pkt);
std::vector<std::uint8_t> zlib_decompress(const std::vector<std::uint8_t>& blob);
