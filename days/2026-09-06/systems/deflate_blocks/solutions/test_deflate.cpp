// PEDAGOGY-TEST: COMP-DEFL-01: BitWriter/BitReader LSB-first
// PEDAGOGY-TEST: COMP-DEFL-02: encode stored block
// PEDAGOGY-TEST: COMP-DEFL-03: decode stored block
// PEDAGOGY-TEST: COMP-DEFL-04: encode fixed huffman literals
// PEDAGOGY-TEST: COMP-DEFL-05: decode fixed huffman stream
#include "bit_stream.hpp"
#include "deflate.hpp"
#include <iostream>
#include <string>
#include <vector>

#define REQUIRE(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "FAIL: " << __FILE__ << ":" << __LINE__ << "\n"; \
            return 1; \
        } \
    } while (0)

int main() {
    BitWriter writer;
    writer.write_bits(0b1011u, 4);
    writer.write_bits(0b0001u, 4);
    auto bits = writer.take_bytes();
    REQUIRE(bits.size() == 1);
    REQUIRE(bits[0] == 0x1B);

    BitReader reader(bits);
    REQUIRE(reader.read_bits(4) == 0b1011u);
    REQUIRE(reader.read_bits(4) == 0b0001u);

    const std::vector<std::uint8_t> payload = {'D', 'E', 'F', 'L'};
    const auto stored = encode_stored_block(payload, true);
    const auto decoded = decode_stored_blocks(stored);
    REQUIRE(decoded == payload);

    const std::string text = "RFC1951";
    std::vector<std::uint8_t> literals(text.begin(), text.end());
    const auto fixed = encode_fixed_block(literals, true);
    const auto inflated = decode_fixed_block(fixed);
    REQUIRE(inflated == literals);

    std::cout << "OK deflate blocks\n";
    return 0;
}
