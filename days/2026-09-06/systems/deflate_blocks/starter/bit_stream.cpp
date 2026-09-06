#include "bit_stream.hpp"

void BitWriter::write_bit(bool bit) {
    // TODO [COMP-DEFL-01]: acumular bit no buffer LSB-first e flush a cada 8 bits
}

void BitWriter::write_bits(std::uint32_t value, int count) {
    // TODO [COMP-DEFL-01]: chamar write_bit para cada bit de value (LSB primeiro)
}

void BitWriter::align_byte() {
    // TODO [COMP-DEFL-01]: flush parcial para alinhar fronteira de byte
}

std::vector<std::uint8_t> BitWriter::take_bytes() {
    align_byte();
    return std::move(out_);
}

BitReader::BitReader(const std::vector<std::uint8_t>& data) : in_(data) {}

bool BitReader::read_bit() {
    // TODO [COMP-DEFL-01]: retornar próximo bit LSB-first
    return false;
}

std::uint32_t BitReader::read_bits(int count) {
    // TODO [COMP-DEFL-01]: ler count bits LSB-first
    return 0;
}

bool BitReader::has_bits(int count) const {
    // TODO [COMP-DEFL-01]: verificar bits disponíveis
    return false;
}

void BitReader::align_byte() {
    // TODO [COMP-DEFL-01]: pular para próxima fronteira de byte
}
