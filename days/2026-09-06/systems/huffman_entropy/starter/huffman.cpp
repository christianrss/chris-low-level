#include "huffman.hpp"
#include "bit_io.hpp"
#include <cstring>

bool build_huffman_codes(const std::uint32_t freq[256], std::vector<HuffmanCodeEntry>& table) {
    table.clear();
    // TODO [COMP-HUF-02]: construir árvore Huffman e gerar tabela de códigos MSB-first
    (void)freq;
    return false;
}

bool encode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-HUF-03]: contar frequências, serializar header CHHUF + tabela + bitstream
    (void)input;
    return false;
}

bool decode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-HUF-04]: reconstruir árvore a partir da tabela e decodificar bit a bit
    (void)input;
    return false;
}
