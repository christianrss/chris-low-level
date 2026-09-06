#include "deflate.hpp"
#include "bit_stream.hpp"
#include <stdexcept>

FixedLitTables build_fixed_literal_tables() {
    // TODO [COMP-DEFL-04]: preencher tabelas fixas RFC1951 (lit 0-255 + EOB 256)
    return {};
}

std::vector<std::uint8_t> encode_stored_block(const std::vector<std::uint8_t>& data, bool final_block) {
    // TODO [COMP-DEFL-02]: BFINAL/BTYPE=00 + LEN/NLEN + payload
    return {};
}

std::vector<std::uint8_t> decode_stored_blocks(const std::vector<std::uint8_t>& raw) {
    // TODO [COMP-DEFL-03]: ler bloco stored e validar LEN/NLEN
    return {};
}

std::vector<std::uint8_t> encode_fixed_block(const std::vector<std::uint8_t>& literals, bool final_block) {
    // TODO [COMP-DEFL-04]: BTYPE=01 + literais + símbolo 256
    return {};
}

std::vector<std::uint8_t> decode_fixed_block(const std::vector<std::uint8_t>& raw) {
    // TODO [COMP-DEFL-05]: decodificar Huffman fixo até EOB
    return {};
}
