#include "bit_stream.hpp"

void BitWriter::write_bit(bool bit) {
    if (bit) {
        bit_buf_ |= (1u << bit_count_);
    }
    ++bit_count_;
    if (bit_count_ == 8) {
        out_.push_back(static_cast<std::uint8_t>(bit_buf_ & 0xFFu));
        bit_buf_ = 0;
        bit_count_ = 0;
    }
}

void BitWriter::write_bits(std::uint32_t value, int count) {
    for (int i = 0; i < count; ++i) {
        write_bit((value >> i) & 1u);
    }
}

void BitWriter::align_byte() {
    if (bit_count_ != 0) {
        out_.push_back(static_cast<std::uint8_t>(bit_buf_ & 0xFFu));
        bit_buf_ = 0;
        bit_count_ = 0;
    }
}

std::vector<std::uint8_t> BitWriter::take_bytes() {
    align_byte();
    return std::move(out_);
}

BitReader::BitReader(const std::vector<std::uint8_t>& data) : in_(data) {}

bool BitReader::read_bit() {
    if (bit_pos_ >= in_.size() * 8) {
        return false;
    }
    const auto byte = in_[bit_pos_ / 8];
    const auto bit = (byte >> (bit_pos_ % 8)) & 1u;
    ++bit_pos_;
    return bit != 0;
}

std::uint32_t BitReader::read_bits(int count) {
    std::uint32_t value = 0;
    for (int i = 0; i < count; ++i) {
        if (read_bit()) {
            value |= (1u << i);
        }
    }
    return value;
}

bool BitReader::has_bits(int count) const {
    return (in_.size() * 8) - bit_pos_ >= static_cast<std::size_t>(count);
}

void BitReader::align_byte() {
    const auto rem = bit_pos_ % 8;
    if (rem != 0) {
        bit_pos_ += 8 - rem;
    }
}
