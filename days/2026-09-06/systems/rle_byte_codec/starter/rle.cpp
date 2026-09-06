#include "rle.hpp"
#include <cstring>

bool encode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-RLE-01]: escrever header CHRLE + length LE32 e compactar runs (count, byte)
    (void)input;
    return false;
}

bool decode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-RLE-02]: validar magic e expandir runs
    // TODO [COMP-RLE-03]: rejeitar payload truncado (out.size() != len)
    (void)input;
    return false;
}
