#include "deflate_stored.hpp"
#include "bit_stream.hpp"
#include <stdexcept>

std::vector<std::uint8_t> encode_stored_block(const std::vector<std::uint8_t>& data, bool final_block) {
    BitWriter writer;
    writer.write_bits(final_block ? 1u : 0u, 1);
    writer.write_bits(0u, 2);
    writer.align_byte();
    const auto len = static_cast<std::uint16_t>(data.size());
    const auto nlen = static_cast<std::uint16_t>(~len);
    writer.write_bits(len & 0xFFu, 8);
    writer.write_bits((len >> 8) & 0xFFu, 8);
    writer.write_bits(nlen & 0xFFu, 8);
    writer.write_bits((nlen >> 8) & 0xFFu, 8);
    for (const auto byte : data) {
        writer.write_bits(byte, 8);
    }
    return writer.take_bytes();
}

std::vector<std::uint8_t> decode_stored_blocks(const std::vector<std::uint8_t>& raw) {
    BitReader reader(raw);
    std::vector<std::uint8_t> out;
    bool final = false;
    while (!final) {
        final = reader.read_bit();
        const auto btype = reader.read_bits(2);
        if (btype != 0) {
            throw std::runtime_error("only stored blocks supported");
        }
        reader.align_byte();
        const auto len = static_cast<std::uint16_t>(reader.read_bits(8) | (reader.read_bits(8) << 8));
        const auto nlen = static_cast<std::uint16_t>(reader.read_bits(8) | (reader.read_bits(8) << 8));
        if (static_cast<std::uint16_t>(~len) != nlen) {
            throw std::runtime_error("LEN/NLEN mismatch");
        }
        for (std::uint16_t i = 0; i < len; ++i) {
            out.push_back(static_cast<std::uint8_t>(reader.read_bits(8)));
        }
    }
    return out;
}
