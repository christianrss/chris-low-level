#include "zlib_min.hpp"
#include "adler32.hpp"
#include "deflate_stored.hpp"
#include <stdexcept>

std::vector<std::uint8_t> zlib_min_compress(const std::vector<std::uint8_t>& data) {
    std::vector<std::uint8_t> out{0x78, 0x01};
    const auto raw = encode_stored_block(data, true);
    out.insert(out.end(), raw.begin(), raw.end());
    const auto a = adler32(data);
    out.push_back(static_cast<std::uint8_t>((a >> 24) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((a >> 16) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((a >> 8) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>(a & 0xFFu));
    return out;
}

std::vector<std::uint8_t> zlib_min_decompress(const std::vector<std::uint8_t>& blob) {
    if (blob.size() < 6) {
        throw std::runtime_error("zlib blob too small");
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
