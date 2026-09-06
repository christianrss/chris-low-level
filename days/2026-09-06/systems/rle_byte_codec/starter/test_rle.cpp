#include "rle.hpp"
#include <cstring>
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
    // Caso 1: zeros run — PEDAGOGY-TEST: COMP-RLE-01
    std::vector<std::uint8_t> in(10, 0), enc, dec;
    CHECK(encode_rle(in, enc));
    CHECK(decode_rle(enc, dec));
    CHECK(dec == in);

    // Caso 2: ASCII sem repetição — PEDAGOGY-TEST: COMP-RLE-02
    const char* txt = "ABCD";
    in.assign(txt, txt + 4);
    CHECK(encode_rle(in, enc));
    CHECK(decode_rle(enc, dec));
    CHECK(dec == in);

    // Caso 3: corrupt magic — PEDAGOGY-TEST: COMP-RLE-03
    CHECK(encode_rle(in, enc));
    enc[0] = 'X';
    CHECK(!decode_rle(enc, dec));

    std::cout << "OK rle\n";
    return 0;
}
