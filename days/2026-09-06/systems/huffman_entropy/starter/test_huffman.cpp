#include "bit_io.hpp"
#include "huffman.hpp"
#include <iostream>
#include <vector>

#define CHECK(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "FAIL " #cond "\n"; \
            return 1; \
        } \
    } while (0)

int main() {
    // Caso 1: bit writer MSB-first — PEDAGOGY-TEST: COMP-HUF-01
    BitWriter w;
    w.write_bits(0b1011, 4);
    w.flush();
    CHECK(w.bytes().size() == 1);
    CHECK(w.bytes()[0] == 0xB0);
    BitReader r(std::span<const std::uint8_t>(w.bytes()));
    bool b0 = false, b1 = false, b2 = false, b3 = false;
    CHECK(r.read_bit(b0) && b0);
    CHECK(r.read_bit(b1) && !b1);
    CHECK(r.read_bit(b2) && b2);
    CHECK(r.read_bit(b3) && b3);

    std::vector<std::uint8_t> in{'A', 'A', 'A', 'B', 'B', 'C'}, enc, dec;
    // Caso 2: build huffman table — PEDAGOGY-TEST: COMP-HUF-02
    std::uint32_t freq[256] = {};
    for (auto c : in) {
        ++freq[c];
    }
    std::vector<HuffmanCodeEntry> table;
    CHECK(build_huffman_codes(freq, table));
    CHECK(!table.empty());

    // Caso 3: encode round-trip header — PEDAGOGY-TEST: COMP-HUF-03
    CHECK(encode_huffman(in, enc));
    // Caso 4: decode + corrupt magic — PEDAGOGY-TEST: COMP-HUF-04
    CHECK(decode_huffman(enc, dec));
    CHECK(dec == in);

    CHECK(encode_huffman(in, enc));
    enc[0] = 'X';
    CHECK(!decode_huffman(enc, dec));

    std::cout << "OK huffman\n";
    return 0;
}
