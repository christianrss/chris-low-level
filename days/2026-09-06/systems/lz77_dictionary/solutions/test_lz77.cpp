#include "lz77.hpp"
#include <iostream>
#include <string>
#include <vector>

#define CHECK(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "FAIL " #cond "\n"; \
            return 1; \
        } \
    } while (0)

int main() {
    // Caso 1: janela 32 KB — PEDAGOGY-TEST: COMP-LZ77-01
    CHECK(LZ77_WINDOW_SIZE == 32768);
    CHECK(LZ77_MIN_MATCH == 3);

    const std::string phrase = "ABCABCABCD";
    std::vector<std::uint8_t> data(phrase.begin(), phrase.end());

    // Caso 2: longest match — PEDAGOGY-TEST: COMP-LZ77-02
    LZ77Match m{};
    const std::size_t pos = 3;
    CHECK(find_longest_match(data, pos, m));
    CHECK(m.length >= LZ77_MIN_MATCH);
    CHECK(m.offset <= LZ77_WINDOW_SIZE);

    std::vector<std::uint8_t> in(phrase.begin(), phrase.end()), enc, dec;
    // Caso 3: encode tokens — PEDAGOGY-TEST: COMP-LZ77-03
    CHECK(encode_lz77(in, enc));
    // Caso 4: decode sliding window — PEDAGOGY-TEST: COMP-LZ77-04
    CHECK(decode_lz77(enc, dec));
    CHECK(dec == in);

    CHECK(encode_lz77(in, enc));
    enc[0] = 'X';
    CHECK(!decode_lz77(enc, dec));

    std::cout << "OK lz77\n";
    return 0;
}
