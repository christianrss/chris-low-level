#include "lz77.hpp"
#include <algorithm>
#include <cstring>

// PEDAGOGY-SOLUTION: COMP-LZ77-01
// PEDAGOGY-SOLUTION: COMP-LZ77-02
// PEDAGOGY-SOLUTION: COMP-LZ77-03
// PEDAGOGY-SOLUTION: COMP-LZ77-04

bool find_longest_match(std::span<const std::uint8_t> data, std::size_t pos, LZ77Match& match) {
    match = {};
    if (pos >= data.size()) {
        return false;
    }
    const std::size_t window_start = (pos > LZ77_WINDOW_SIZE) ? (pos - LZ77_WINDOW_SIZE) : 0;
    const std::size_t max_len =
        static_cast<std::size_t>(std::min<std::size_t>(LZ77_MAX_MATCH, data.size() - pos));
    std::size_t best_len = 0;
    std::uint16_t best_off = 0;
    for (std::size_t start = window_start; start < pos; ++start) {
        std::size_t len = 0;
        while (len < max_len && data[start + len] == data[pos + len]) {
            ++len;
        }
        if (len >= LZ77_MIN_MATCH && len > best_len) {
            best_len = len;
            best_off = static_cast<std::uint16_t>(pos - start);
        }
    }
    if (best_len >= LZ77_MIN_MATCH) {
        match.offset = best_off;
        match.length = static_cast<std::uint8_t>(best_len);
        return true;
    }
    return false;
}

bool encode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    out.insert(out.end(), CHLZ7_MAGIC, CHLZ7_MAGIC + 5);
    const std::uint32_t len = static_cast<std::uint32_t>(input.size());
    out.push_back(static_cast<std::uint8_t>(len & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 24) & 0xFF));
    std::size_t pos = 0;
    while (pos < input.size()) {
        LZ77Match m{};
        if (find_longest_match(input, pos, m)) {
            out.push_back(0x01);
            out.push_back(static_cast<std::uint8_t>(m.offset & 0xFF));
            out.push_back(static_cast<std::uint8_t>((m.offset >> 8) & 0xFF));
            out.push_back(m.length);
            pos += m.length;
        } else {
            out.push_back(0x00);
            out.push_back(input[pos]);
            ++pos;
        }
    }
    return true;
}

bool decode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    if (input.size() < 9 || std::memcmp(input.data(), CHLZ7_MAGIC, 5) != 0) {
        return false;
    }
    std::uint32_t len = 0;
    len |= input[5];
    len |= static_cast<std::uint32_t>(input[6]) << 8;
    len |= static_cast<std::uint32_t>(input[7]) << 16;
    len |= static_cast<std::uint32_t>(input[8]) << 24;
    out.reserve(len);
    std::size_t p = 9;
    while (out.size() < len && p < input.size()) {
        const std::uint8_t tag = input[p++];
        if (tag == 0x00) {
            if (p >= input.size()) {
                return false;
            }
            out.push_back(input[p++]);
        } else if (tag == 0x01) {
            if (p + 2 >= input.size()) {
                return false;
            }
            const std::uint16_t offset =
                static_cast<std::uint16_t>(input[p] | (static_cast<std::uint16_t>(input[p + 1]) << 8));
            p += 2;
            if (p >= input.size()) {
                return false;
            }
            const std::uint8_t match_len = input[p++];
            if (offset == 0 || offset > out.size()) {
                return false;
            }
            const std::size_t start = out.size() - offset;
            for (std::uint8_t i = 0; i < match_len && out.size() < len; ++i) {
                out.push_back(out[start + i]);
            }
        } else {
            return false;
        }
    }
    return out.size() == len;
}
