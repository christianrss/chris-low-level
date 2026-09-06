#include "bit_io.hpp"

void BitWriter::write_bit(bool bit) {
    // TODO [COMP-HUF-01]: empilhar bit MSB-first no acumulador e flush a cada 8 bits
    (void)bit;
}

void BitWriter::write_bits(std::uint32_t value, int bit_count) {
    for (int i = bit_count - 1; i >= 0; --i) {
        write_bit(((value >> i) & 1u) != 0);
    }
}

void BitWriter::flush() {
    // TODO [COMP-HUF-01]: alinhar último byte parcial à esquerda (MSB)
}

BitReader::BitReader(std::span<const std::uint8_t> data) : data_(data) {}

bool BitReader::read_bit(bool& out) {
    // TODO [COMP-HUF-01]: ler próximo bit MSB-first do stream
    (void)out;
    return false;
}
