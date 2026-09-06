#include "lz77.hpp"

bool find_longest_match(std::span<const std::uint8_t> data, std::size_t pos, LZ77Match& match) {
    // TODO [COMP-LZ77-01]: respeitar janela LZ77_WINDOW_SIZE (32 KB)
    // TODO [COMP-LZ77-02]: retornar maior match >= LZ77_MIN_MATCH
    (void)data;
    (void)pos;
    match = {};
    return false;
}

bool encode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-LZ77-03]: header CHLZ7 + tokens literal/match
    (void)input;
    return false;
}

bool decode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-LZ77-04]: expandir literais e copiar da janela deslizante
    (void)input;
    return false;
}
