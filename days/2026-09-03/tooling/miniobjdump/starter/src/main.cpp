#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

std::uint16_t read_u16_le(const std::vector<std::uint8_t>& data, std::size_t offset) {
    if (offset + 2 > data.size()) {
        throw std::runtime_error("truncated u16");
    }

    // TODO [OBJDUMP-U16-01]: combine two bytes in little-endian order.
    return 0;
}

std::uint32_t read_u32_le(const std::vector<std::uint8_t>& data, std::size_t offset) {
    if (offset + 4 > data.size()) {
        throw std::runtime_error("truncated u32");
    }

    // TODO [OBJDUMP-U32-01]: combine four bytes in little-endian order.
    return 0;
}

std::vector<std::uint8_t> read_file(const std::string& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) {
        throw std::runtime_error("cannot open file: " + path);
    }

    return {
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>(),
    };
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: miniobjdump <binary>\n";
        return 2;
    }

    try {
        const std::vector<std::uint8_t> data = read_file(argv[1]);
        std::cout << "file_size=" << data.size() << " bytes\n";

        if (data.size() >= 4 && data[0] == 0x7F &&
            data[1] == 'E' && data[2] == 'L' && data[3] == 'F') {
            std::cout << "ELF detected\n";
        } else if (data.size() >= 2 && data[0] == 'M' && data[1] == 'Z') {
            std::cout << "possible PE detected\n";
        } else {
            std::cout << "unknown format\n";
        }

        // TODO [OBJDUMP-PARSE-01]: parse headers, enumerate sections and decode .text.
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << "\n";
        return 1;
    }
}
