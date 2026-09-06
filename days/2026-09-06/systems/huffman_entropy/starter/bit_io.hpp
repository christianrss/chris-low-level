#pragma once
#include <cstdint>
#include <span>
#include <vector>

class BitWriter {
public:
    void write_bit(bool bit);
    void write_bits(std::uint32_t value, int bit_count);
    void flush();
    const std::vector<std::uint8_t>& bytes() const { return bytes_; }

private:
    std::vector<std::uint8_t> bytes_;
    std::uint8_t acc_ = 0;
    int bits_in_acc_ = 0;
};

class BitReader {
public:
    explicit BitReader(std::span<const std::uint8_t> data);
    bool read_bit(bool& out);

private:
    std::span<const std::uint8_t> data_;
    std::size_t byte_index_ = 0;
    int bits_left_in_byte_ = 0;
    std::uint8_t current_ = 0;
};
