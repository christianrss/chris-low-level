#include "codec.hpp"
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "usage: chris_compress <rle|zlib> <text>\n";
        return 1;
    }
    const std::string mode = argv[1];
    const std::string text = argv[2];
    std::vector<std::uint8_t> in(text.begin(), text.end()), enc, dec;
    const bool ok = (mode == "rle") ? encode_rle(in, enc) && decode_rle(enc, dec)
                                    : zlib_compress_stored(in, enc) && zlib_decompress_stored(enc, dec);
    if (!ok || dec != in) {
        std::cerr << "round-trip failed\n";
        return 1;
    }
    std::cout << mode << " ok bytes=" << enc.size() << "\n";
    return 0;
}
