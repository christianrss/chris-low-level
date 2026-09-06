#include "codec.hpp"
#include <cassert>
#include <string>

int main() {
    const std::string text = "compress-capstone-day06";
    std::vector<std::uint8_t> in(text.begin(), text.end()), enc, dec;
    assert(encode_rle(in, enc));
    assert(decode_rle(enc, dec));
    assert(dec == in);
    assert(zlib_compress_stored(in, enc));
    assert(zlib_decompress_stored(enc, dec));
    assert(dec == in);
    return 0;
}
