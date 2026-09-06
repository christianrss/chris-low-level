// PEDAGOGY-SOLUTION: COMP-DEFL-02
// PEDAGOGY-SOLUTION: COMP-DEFL-03
// PEDAGOGY-SOLUTION: COMP-DEFL-04
// PEDAGOGY-SOLUTION: COMP-DEFL-05
#include "deflate.hpp"
#include "bit_stream.hpp"
#include <stdexcept>

namespace {

std::uint16_t reverse_bits(std::uint16_t code, int len) {
    std::uint16_t rev = 0;
    for (int i = 0; i < len; ++i) {
        if ((code >> i) & 1u) {
            rev |= static_cast<std::uint16_t>(1u << (len - 1 - i));
        }
    }
    return rev;
}

int decode_symbol(BitReader& reader, const FixedLitTables& tables) {
    std::uint32_t code = 0;
    for (int len = 1; len <= 15; ++len) {
        code |= reader.read_bit() ? (1u << (len - 1)) : 0u;
        for (int sym = 0; sym < 288; ++sym) {
            if (tables.len[sym] == len && tables.code[sym] == code) {
                return sym;
            }
        }
    }
    throw std::runtime_error("invalid fixed huffman code");
}

}  // namespace

FixedLitTables build_fixed_literal_tables() {
    std::uint8_t lens[288]{};
    for (int i = 0; i <= 143; ++i) {
        lens[i] = 8;
    }
    for (int i = 144; i <= 255; ++i) {
        lens[i] = 9;
    }
    lens[256] = 7;
    for (int i = 257; i <= 285; ++i) {
        lens[i] = 8;
    }
    for (int i = 286; i <= 287; ++i) {
        lens[i] = 8;
    }

    std::uint16_t bl_count[16]{};
    for (int i = 0; i < 288; ++i) {
        if (lens[i]) {
            ++bl_count[lens[i]];
        }
    }

    std::uint16_t next_code[16]{};
    std::uint16_t code = 0;
    for (int bits = 1; bits <= 15; ++bits) {
        code = static_cast<std::uint16_t>((code + bl_count[bits - 1]) << 1);
        next_code[bits] = code;
    }

    FixedLitTables tables{};
    for (int sym = 0; sym < 288; ++sym) {
        if (!lens[sym]) {
            continue;
        }
        const auto canonical = next_code[lens[sym]]++;
        tables.code[sym] = reverse_bits(canonical, lens[sym]);
        tables.len[sym] = lens[sym];
    }
    return tables;
}

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
            throw std::runtime_error("only stored blocks supported in this decoder path");
        }
        reader.align_byte();
        const auto len_lo = reader.read_bits(8);
        const auto len_hi = reader.read_bits(8);
        const auto nlen_lo = reader.read_bits(8);
        const auto nlen_hi = reader.read_bits(8);
        const auto len = static_cast<std::uint16_t>(len_lo | (len_hi << 8));
        const auto nlen = static_cast<std::uint16_t>(nlen_lo | (nlen_hi << 8));
        if (static_cast<std::uint16_t>(~len) != nlen) {
            throw std::runtime_error("LEN/NLEN mismatch");
        }
        for (std::uint16_t i = 0; i < len; ++i) {
            out.push_back(static_cast<std::uint8_t>(reader.read_bits(8)));
        }
    }
    return out;
}

std::vector<std::uint8_t> encode_fixed_block(const std::vector<std::uint8_t>& literals, bool final_block) {
    const auto tables = build_fixed_literal_tables();
    BitWriter writer;
    writer.write_bits(final_block ? 1u : 0u, 1);
    writer.write_bits(1u, 2);
    for (const auto byte : literals) {
        writer.write_bits(tables.code[byte], tables.len[byte]);
    }
    writer.write_bits(tables.code[256], tables.len[256]);
    return writer.take_bytes();
}

std::vector<std::uint8_t> decode_fixed_block(const std::vector<std::uint8_t>& raw) {
    const auto tables = build_fixed_literal_tables();
    BitReader reader(raw);
    std::vector<std::uint8_t> out;
    bool final = false;
    while (!final) {
        final = reader.read_bit();
        const auto btype = reader.read_bits(2);
        if (btype != 1) {
            throw std::runtime_error("expected fixed huffman block");
        }
        while (true) {
            const int sym = decode_symbol(reader, tables);
            if (sym == 256) {
                break;
            }
            if (sym < 0 || sym > 255) {
                throw std::runtime_error("literal out of range");
            }
            out.push_back(static_cast<std::uint8_t>(sym));
        }
    }
    return out;
}
