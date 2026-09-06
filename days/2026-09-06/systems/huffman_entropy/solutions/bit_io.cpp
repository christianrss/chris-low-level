#include "bit_io.hpp"

// PEDAGOGY-SOLUTION: COMP-HUF-01

void BitWriter::write_bit(bool bit) {
    acc_ = static_cast<std::uint8_t>((acc_ << 1) | (bit ? 1u : 0u));
    ++bits_in_acc_;
    if (bits_in_acc_ == 8) {
        bytes_.push_back(acc_);
        acc_ = 0;
        bits_in_acc_ = 0;
    }
}

void BitWriter::write_bits(std::uint32_t value, int bit_count) {
    for (int i = bit_count - 1; i >= 0; --i) {
        write_bit(((value >> i) & 1u) != 0);
    }
}

void BitWriter::flush() {
    if (bits_in_acc_ > 0) {
        acc_ = static_cast<std::uint8_t>(acc_ << (8 - bits_in_acc_));
        bytes_.push_back(acc_);
        acc_ = 0;
        bits_in_acc_ = 0;
    }
}

BitReader::BitReader(std::span<const std::uint8_t> data) : data_(data) {}

bool BitReader::read_bit(bool& out) {
    if (bits_left_in_byte_ == 0) {
        if (byte_index_ >= data_.size()) {
            return false;
        }
        current_ = data_[byte_index_++];
        bits_left_in_byte_ = 8;
    }
    out = (current_ & 0x80u) != 0;
    current_ = static_cast<std::uint8_t>(current_ << 1);
    --bits_left_in_byte_;
    return true;
}
