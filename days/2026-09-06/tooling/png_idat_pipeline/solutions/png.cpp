// PEDAGOGY-SOLUTION: COMP-PNG-01
// PEDAGOGY-SOLUTION: COMP-PNG-02
// PEDAGOGY-SOLUTION: COMP-PNG-03
// PEDAGOGY-SOLUTION: COMP-PNG-04
#include "png.hpp"
#include "zlib_min.hpp"
#include "crc32.hpp"
#include <cstring>
#include <stdexcept>

namespace {
constexpr std::uint8_t kSignature[8] = {137, 80, 78, 71, 13, 10, 26, 10};

std::uint32_t read_be32(const std::uint8_t* p) {
    return (static_cast<std::uint32_t>(p[0]) << 24) | (static_cast<std::uint32_t>(p[1]) << 16) |
           (static_cast<std::uint32_t>(p[2]) << 8) | static_cast<std::uint32_t>(p[3]);
}
}  // namespace

std::uint32_t png_chunk_crc(const char* type, const std::vector<std::uint8_t>& data) {
    std::vector<std::uint8_t> buf(4 + data.size());
    std::memcpy(buf.data(), type, 4);
    if (!data.empty()) {
        std::memcpy(buf.data() + 4, data.data(), data.size());
    }
    return crc32(buf.data(), buf.size());
}

std::vector<std::uint8_t> png_chunk(const char* type, const std::vector<std::uint8_t>& data) {
    std::vector<std::uint8_t> out(4 + 4 + data.size() + 4);
    const auto len = static_cast<std::uint32_t>(data.size());
    out[0] = static_cast<std::uint8_t>((len >> 24) & 0xFFu);
    out[1] = static_cast<std::uint8_t>((len >> 16) & 0xFFu);
    out[2] = static_cast<std::uint8_t>((len >> 8) & 0xFFu);
    out[3] = static_cast<std::uint8_t>(len & 0xFFu);
    std::memcpy(out.data() + 4, type, 4);
    if (!data.empty()) {
        std::memcpy(out.data() + 8, data.data(), data.size());
    }
    const auto c = png_chunk_crc(type, data);
    const std::size_t o = 8 + data.size();
    out[o + 0] = static_cast<std::uint8_t>((c >> 24) & 0xFFu);
    out[o + 1] = static_cast<std::uint8_t>((c >> 16) & 0xFFu);
    out[o + 2] = static_cast<std::uint8_t>((c >> 8) & 0xFFu);
    out[o + 3] = static_cast<std::uint8_t>(c & 0xFFu);
    return out;
}

std::vector<std::uint8_t> build_ihdr(const PngImage& spec) {
    std::vector<std::uint8_t> data(13);
    data[0] = static_cast<std::uint8_t>((spec.width >> 24) & 0xFFu);
    data[1] = static_cast<std::uint8_t>((spec.width >> 16) & 0xFFu);
    data[2] = static_cast<std::uint8_t>((spec.width >> 8) & 0xFFu);
    data[3] = static_cast<std::uint8_t>(spec.width & 0xFFu);
    data[4] = static_cast<std::uint8_t>((spec.height >> 24) & 0xFFu);
    data[5] = static_cast<std::uint8_t>((spec.height >> 16) & 0xFFu);
    data[6] = static_cast<std::uint8_t>((spec.height >> 8) & 0xFFu);
    data[7] = static_cast<std::uint8_t>(spec.height & 0xFFu);
    data[8] = spec.bit_depth;
    data[9] = spec.color_type;
    data[10] = 0;
    data[11] = 0;
    data[12] = 0;
    return data;
}

std::vector<std::uint8_t> filter_none_scanlines(const PngImage& img) {
    const std::size_t row_bytes = img.width;
    std::vector<std::uint8_t> raw((row_bytes + 1) * img.height);
    for (std::uint32_t y = 0; y < img.height; ++y) {
        raw[y * (row_bytes + 1)] = 0;
        std::memcpy(raw.data() + y * (row_bytes + 1) + 1, img.pixels.data() + y * row_bytes, row_bytes);
    }
    return raw;
}

std::vector<std::uint8_t> encode_png(const PngImage& img) {
    std::vector<std::uint8_t> out(std::begin(kSignature), std::end(kSignature));
    const auto ihdr = build_ihdr(img);
    const auto ihdr_chunk = png_chunk("IHDR", ihdr);
    out.insert(out.end(), ihdr_chunk.begin(), ihdr_chunk.end());
    const auto filtered = filter_none_scanlines(img);
    const auto idat_payload = zlib_min_compress(filtered);
    const auto idat_chunk = png_chunk("IDAT", idat_payload);
    out.insert(out.end(), idat_chunk.begin(), idat_chunk.end());
    const auto iend_chunk = png_chunk("IEND", {});
    out.insert(out.end(), iend_chunk.begin(), iend_chunk.end());
    return out;
}

PngImage decode_png(const std::vector<std::uint8_t>& blob) {
    if (blob.size() < 8 || std::memcmp(blob.data(), kSignature, 8) != 0) {
        throw std::runtime_error("bad png signature");
    }
    PngImage img;
    std::vector<std::uint8_t> idat;
    std::size_t pos = 8;
    while (pos + 12 <= blob.size()) {
        const auto len = read_be32(blob.data() + pos);
        const char* type = reinterpret_cast<const char*>(blob.data() + pos + 4);
        const auto data_off = pos + 8;
        const auto crc_off = data_off + len;
        if (crc_off + 4 > blob.size()) {
            throw std::runtime_error("truncated png chunk");
        }
        std::vector<std::uint8_t> data;
        if (len) {
            data.assign(blob.begin() + data_off, blob.begin() + data_off + len);
        }
        const auto expect = png_chunk_crc(type, data);
        const auto got = read_be32(blob.data() + crc_off);
        if (expect != got) {
            throw std::runtime_error("png chunk crc mismatch");
        }
        if (std::strncmp(type, "IHDR", 4) == 0 && len == 13) {
            img.width = read_be32(data.data());
            img.height = read_be32(data.data() + 4);
            img.bit_depth = data[8];
            img.color_type = data[9];
        } else if (std::strncmp(type, "IDAT", 4) == 0) {
            idat.insert(idat.end(), data.begin(), data.end());
        } else if (std::strncmp(type, "IEND", 4) == 0) {
            break;
        }
        pos = crc_off + 4;
    }
    const auto raw = zlib_min_decompress(idat);
    const std::size_t row_bytes = img.width;
    img.pixels.resize(row_bytes * img.height);
    for (std::uint32_t y = 0; y < img.height; ++y) {
        const auto filter = raw[y * (row_bytes + 1)];
        if (filter != 0) {
            throw std::runtime_error("only filter none supported");
        }
        std::memcpy(img.pixels.data() + y * row_bytes, raw.data() + y * (row_bytes + 1) + 1, row_bytes);
    }
    return img;
}
