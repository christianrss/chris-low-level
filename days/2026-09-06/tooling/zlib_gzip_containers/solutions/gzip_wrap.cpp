// PEDAGOGY-SOLUTION: COMP-ZLIB-04
#include "gzip_wrap.hpp"
#include "crc32.hpp"
#include "deflate_stored.hpp"
#include <stdexcept>

std::vector<std::uint8_t> gzip_compress(const std::vector<std::uint8_t>& data) {
    std::vector<std::uint8_t> out{
        0x1F, 0x8B, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03};
    const auto raw = encode_stored_block(data, true);
    out.insert(out.end(), raw.begin(), raw.end());
    const auto crc = crc32(data);
    const auto isize = static_cast<std::uint32_t>(data.size());
    out.push_back(static_cast<std::uint8_t>(crc & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((crc >> 8) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((crc >> 16) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((crc >> 24) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>(isize & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((isize >> 8) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((isize >> 16) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((isize >> 24) & 0xFFu));
    return out;
}

std::vector<std::uint8_t> gzip_decompress(const std::vector<std::uint8_t>& blob) {
    if (blob.size() < 18 || blob[0] != 0x1F || blob[1] != 0x8B) {
        throw std::runtime_error("not a gzip stream");
    }
    std::size_t pos = 10;
    const auto crc = static_cast<std::uint32_t>(blob[blob.size() - 8]) |
                     (static_cast<std::uint32_t>(blob[blob.size() - 7]) << 8) |
                     (static_cast<std::uint32_t>(blob[blob.size() - 6]) << 16) |
                     (static_cast<std::uint32_t>(blob[blob.size() - 5]) << 24);
    const auto isize = static_cast<std::uint32_t>(blob[blob.size() - 4]) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 3]) << 8) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 2]) << 16) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 1]) << 24);
    std::vector<std::uint8_t> raw(blob.begin() + pos, blob.end() - 8);
    const auto data = decode_stored_blocks(raw);
    if (crc32(data) != crc) {
        throw std::runtime_error("gzip crc mismatch");
    }
    if (static_cast<std::uint32_t>(data.size()) != isize) {
        throw std::runtime_error("gzip isize mismatch");
    }
    return data;
}
