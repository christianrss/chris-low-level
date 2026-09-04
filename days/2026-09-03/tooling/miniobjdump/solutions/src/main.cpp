#include <algorithm>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

std::uint16_t read_u16_le(const std::vector<std::uint8_t>& data, std::size_t offset) {
    if (offset + 2 > data.size()) {
        throw std::runtime_error("truncated u16");
    }

    return static_cast<std::uint16_t>(data[offset]) |
           (static_cast<std::uint16_t>(data[offset + 1]) << 8U);
}

std::uint32_t read_u32_le(const std::vector<std::uint8_t>& data, std::size_t offset) {
    if (offset + 4 > data.size()) {
        throw std::runtime_error("truncated u32");
    }

    return static_cast<std::uint32_t>(data[offset]) |
           (static_cast<std::uint32_t>(data[offset + 1]) << 8U) |
           (static_cast<std::uint32_t>(data[offset + 2]) << 16U) |
           (static_cast<std::uint32_t>(data[offset + 3]) << 24U);
}

std::uint64_t read_u64_le(const std::vector<std::uint8_t>& data, std::size_t offset) {
    const std::uint64_t low = read_u32_le(data, offset);
    const std::uint64_t high = read_u32_le(data, offset + 4);
    return low | (high << 32U);
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

std::string read_c_string(
    const std::vector<std::uint8_t>& data,
    std::size_t offset,
    std::size_t limit) {

    if (offset >= data.size()) {
        return "<bad-name>";
    }

    std::string result;
    while (offset < data.size() && offset < limit && data[offset] != 0) {
        result.push_back(static_cast<char>(data[offset]));
        ++offset;
    }
    return result;
}

void print_hex_byte(std::uint8_t byte) {
    std::cout << std::hex << std::setw(2) << std::setfill('0')
              << static_cast<unsigned>(byte) << std::dec;
}

void decode_x86_64(
    const std::vector<std::uint8_t>& data,
    std::size_t offset,
    std::size_t size,
    std::uint64_t virtual_address) {

    const std::size_t end = std::min(data.size(), offset + size);
    std::size_t pc = offset;

    std::cout << "\nDisassembly subset:\n";
    while (pc < end) {
        const std::size_t instruction_offset = pc;
        const std::uint64_t address = virtual_address + (pc - offset);
        const std::uint8_t opcode = data[pc++];

        std::cout << "  0x" << std::hex << address << std::dec << "  ";
        print_hex_byte(opcode);
        std::cout << "  ";

        if (opcode == 0x55U) {
            std::cout << "push rbp";
        } else if (opcode == 0xC3U) {
            std::cout << "ret";
        } else if (opcode == 0x90U) {
            std::cout << "nop";
        } else if ((opcode == 0xE8U || opcode == 0xE9U) && pc + 4 <= end) {
            const std::int32_t displacement =
                static_cast<std::int32_t>(read_u32_le(data, pc));
            pc += 4;

            const std::uint64_t next_address = virtual_address + (pc - offset);
            const std::uint64_t target =
                static_cast<std::uint64_t>(static_cast<std::int64_t>(next_address) + displacement);

            std::cout << (opcode == 0xE8U ? "call " : "jmp ")
                      << "0x" << std::hex << target << std::dec;
        } else if (opcode == 0x48U && pc + 2 <= end &&
                   data[pc] == 0x89U && data[pc + 1] == 0xE5U) {
            pc += 2;
            std::cout << "mov rbp, rsp";
        } else {
            std::cout << "db 0x";
            print_hex_byte(opcode);
        }

        std::cout << "\n";

        if (pc <= instruction_offset) {
            throw std::runtime_error("decoder made no progress");
        }
    }
}

bool inspect_elf64(const std::vector<std::uint8_t>& data) {
    if (data.size() < 64 ||
        data[0] != 0x7FU || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
        return false;
    }

    if (data[4] != 2U || data[5] != 1U) {
        throw std::runtime_error("only ELF64 little-endian is supported today");
    }

    const std::uint64_t section_table = read_u64_le(data, 40);
    const std::uint16_t section_entry_size = read_u16_le(data, 58);
    const std::uint16_t section_count = read_u16_le(data, 60);
    const std::uint16_t string_index = read_u16_le(data, 62);

    if (section_entry_size < 64U || string_index >= section_count) {
        throw std::runtime_error("invalid ELF section table metadata");
    }

    const std::uint64_t strings_header =
        section_table + static_cast<std::uint64_t>(string_index) * section_entry_size;
    const std::uint64_t strings_offset = read_u64_le(data, strings_header + 24);
    const std::uint64_t strings_size = read_u64_le(data, strings_header + 32);

    std::cout << "Format: ELF64 little-endian\n";
    std::cout << "Sections: " << section_count << "\n\n";

    for (std::uint16_t index = 0; index < section_count; ++index) {
        const std::uint64_t header =
            section_table + static_cast<std::uint64_t>(index) * section_entry_size;

        if (header + 64 > data.size()) {
            throw std::runtime_error("section header outside file");
        }

        const std::uint32_t name_offset = read_u32_le(data, header);
        const std::uint64_t address = read_u64_le(data, header + 16);
        const std::uint64_t file_offset = read_u64_le(data, header + 24);
        const std::uint64_t size = read_u64_le(data, header + 32);

        const std::string name = read_c_string(
            data,
            static_cast<std::size_t>(strings_offset + name_offset),
            static_cast<std::size_t>(strings_offset + strings_size));

        std::cout << std::setw(2) << index << "  "
                  << std::left << std::setw(18) << name << std::right
                  << " off=0x" << std::hex << file_offset
                  << " size=0x" << size
                  << " va=0x" << address << std::dec << "\n";

        if (name == ".text" && file_offset < data.size()) {
            decode_x86_64(
                data,
                static_cast<std::size_t>(file_offset),
                static_cast<std::size_t>(size),
                address);
        }
    }

    return true;
}

bool inspect_pe(const std::vector<std::uint8_t>& data) {
    if (data.size() < 0x40 || data[0] != 'M' || data[1] != 'Z') {
        return false;
    }

    const std::uint32_t pe_offset = read_u32_le(data, 0x3C);
    if (static_cast<std::uint64_t>(pe_offset) + 24U > data.size()) {
        throw std::runtime_error("PE header outside file");
    }

    if (std::memcmp(data.data() + pe_offset, "PE\0\0", 4) != 0) {
        throw std::runtime_error("MZ file without PE signature");
    }

    const std::uint16_t section_count = read_u16_le(data, pe_offset + 6);
    const std::uint16_t optional_size = read_u16_le(data, pe_offset + 20);
    const std::size_t section_table = pe_offset + 24U + optional_size;

    std::cout << "Format: PE\n";
    std::cout << "Sections: " << section_count << "\n\n";

    for (std::uint16_t index = 0; index < section_count; ++index) {
        const std::size_t header = section_table + static_cast<std::size_t>(index) * 40U;
        if (header + 40U > data.size()) {
            throw std::runtime_error("PE section header outside file");
        }

        char name_buffer[9]{};
        std::memcpy(name_buffer, data.data() + header, 8);
        const std::string name(name_buffer);

        const std::uint32_t virtual_address = read_u32_le(data, header + 12);
        const std::uint32_t raw_size = read_u32_le(data, header + 16);
        const std::uint32_t raw_offset = read_u32_le(data, header + 20);

        std::cout << std::setw(2) << index << "  "
                  << std::left << std::setw(10) << name << std::right
                  << " raw=0x" << std::hex << raw_offset
                  << " size=0x" << raw_size
                  << " rva=0x" << virtual_address << std::dec << "\n";

        if (name == ".text" && raw_offset < data.size()) {
            decode_x86_64(data, raw_offset, raw_size, virtual_address);
        }
    }

    return true;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: miniobjdump <binary>\n";
        return 2;
    }

    try {
        const std::vector<std::uint8_t> data = read_file(argv[1]);

        if (inspect_elf64(data) || inspect_pe(data)) {
            return 0;
        }

        std::cerr << "unsupported file format\n";
        return 1;
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << "\n";
        return 1;
    }
}
