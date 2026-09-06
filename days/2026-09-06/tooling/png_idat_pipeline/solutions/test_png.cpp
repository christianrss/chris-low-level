// PEDAGOGY-TEST: COMP-PNG-01: chunk length/type/crc
// PEDAGOGY-TEST: COMP-PNG-02: IHDR 13 bytes
// PEDAGOGY-TEST: COMP-PNG-03: filter None scanlines
// PEDAGOGY-TEST: COMP-PNG-04: roundtrip encode/decode
#include "png.hpp"
#include <iostream>
#include <vector>

#define REQUIRE(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "FAIL: " << __FILE__ << ":" << __LINE__ << "\n"; \
            return 1; \
        } \
    } while (0)

int main() {
    PngImage img;
    img.width = 3;
    img.height = 2;
    img.bit_depth = 8;
    img.color_type = 0;
    img.pixels = {10, 20, 30, 40, 50, 60};

    const auto ihdr = build_ihdr(img);
    REQUIRE(ihdr.size() == 13);
    REQUIRE(ihdr[8] == 8);
    REQUIRE(ihdr[9] == 0);

    const auto filtered = filter_none_scanlines(img);
    REQUIRE(filtered.size() == (img.width + 1) * img.height);
    REQUIRE(filtered[0] == 0);
    REQUIRE(filtered[1] == 10);

    const auto chunk = png_chunk("IHDR", ihdr);
    REQUIRE(chunk.size() == 4 + 4 + 13 + 4);

    const auto blob = encode_png(img);
    REQUIRE(blob.size() > 8);
    REQUIRE(blob[0] == 137 && blob[1] == 80);

    const auto decoded = decode_png(blob);
    REQUIRE(decoded.width == img.width);
    REQUIRE(decoded.height == img.height);
    REQUIRE(decoded.pixels == img.pixels);

    std::cout << "OK png idat pipeline\n";
    return 0;
}
