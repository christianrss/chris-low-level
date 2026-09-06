#pragma once
#include <cstdint>
#include <vector>

class BitWriter {
public:
    void write_bit(bool bit);
    void write_bits(std::uint32_t value, int count);
    void align_byte();
    const std::vector<std::uint8_t>& bytes() const { return out_; }
    std::vector<std::uint8_t> take_bytes();

private:
    std::vector<std::uint8_t> out_;
    std::uint32_t bit_buf_{0};
    int bit_count_{0};
};

class BitReader {
public:
    explicit BitReader(const std::vector<std::uint8_t>& data);

    bool read_bit();
    std::uint32_t read_bits(int count);
    bool has_bits(int count) const;
    void align_byte();
    std::size_t bit_pos() const { return bit_pos_; }

private:
    const std::vector<std::uint8_t>& in_;
    std::size_t bit_pos_{0};
};
