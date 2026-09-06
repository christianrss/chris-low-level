#pragma once
#include <cstdint>
#include <vector>

struct PngImage {
    std::uint32_t width{0};
    std::uint32_t height{0};
    std::uint8_t bit_depth{8};
    std::uint8_t color_type{0};
    std::vector<std::uint8_t> pixels;
};

std::uint32_t png_chunk_crc(const char* type, const std::vector<std::uint8_t>& data);
std::vector<std::uint8_t> png_chunk(const char* type, const std::vector<std::uint8_t>& data);

std::vector<std::uint8_t> build_ihdr(const PngImage& spec);
std::vector<std::uint8_t> filter_none_scanlines(const PngImage& img);
std::vector<std::uint8_t> encode_png(const PngImage& img);
PngImage decode_png(const std::vector<std::uint8_t>& blob);
