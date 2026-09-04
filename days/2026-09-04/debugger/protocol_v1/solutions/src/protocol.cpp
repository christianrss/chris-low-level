#include "protocol.hpp"
#include <cstddef>
#include <stdexcept>

static constexpr std::uint32_t kMagic = 0x31444B43U; // "CKD1" little-endian
static constexpr std::uint16_t kVersion = 1;
static constexpr std::size_t kHeaderSize = 20;

static void append_u16(std::vector<std::uint8_t>& out, std::uint16_t value) {
    out.push_back(static_cast<std::uint8_t>(value & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((value >> 8) & 0xFFu));
}

static void append_u32(std::vector<std::uint8_t>& out, std::uint32_t value) {
    for (int shift = 0; shift < 32; shift += 8) {
        out.push_back(static_cast<std::uint8_t>((value >> shift) & 0xFFu));
    }
}

static std::uint16_t read_u16(const std::vector<std::uint8_t>& bytes, std::size_t offset) {
    return static_cast<std::uint16_t>(
        bytes[offset] | (static_cast<std::uint16_t>(bytes[offset + 1]) << 8));
}

static std::uint32_t read_u32(const std::vector<std::uint8_t>& bytes, std::size_t offset) {
    std::uint32_t value = 0;
    for (int shift = 0; shift < 32; shift += 8) {
        value |= static_cast<std::uint32_t>(bytes[offset++]) << shift;
    }
    return value;
}

static std::uint32_t fnv1a(const std::uint8_t* data, std::size_t size) {
    std::uint32_t hash = 2166136261U;
    for (std::size_t i = 0; i < size; ++i) {
        hash ^= data[i];
        hash *= 16777619U;
    }
    return hash;
}

std::vector<std::uint8_t> encode_debug_packet(const DebugPacket& packet) {
    if (packet.payload.size() > 1024 * 1024) {
        throw std::invalid_argument("debug packet payload too large");
    }

    std::vector<std::uint8_t> out;
    out.reserve(kHeaderSize + packet.payload.size());
    append_u32(out, kMagic);
    append_u16(out, kVersion);
    append_u16(out, static_cast<std::uint16_t>(packet.command));
    append_u32(out, packet.request_id);
    append_u32(out, static_cast<std::uint32_t>(packet.payload.size()));
    append_u32(out, fnv1a(packet.payload.data(), packet.payload.size()));
    out.insert(out.end(), packet.payload.begin(), packet.payload.end());
    return out;
}

DebugPacket decode_debug_packet(const std::vector<std::uint8_t>& bytes) {
    if (bytes.size() < kHeaderSize) {
        throw std::runtime_error("debug packet header truncated");
    }
    if (read_u32(bytes, 0) != kMagic) {
        throw std::runtime_error("debug packet magic mismatch");
    }
    if (read_u16(bytes, 4) != kVersion) {
        throw std::runtime_error("unsupported debug protocol version");
    }

    const auto command = static_cast<DebugCommand>(read_u16(bytes, 6));
    const std::uint32_t request_id = read_u32(bytes, 8);
    const std::uint32_t payload_size = read_u32(bytes, 12);
    const std::uint32_t expected_hash = read_u32(bytes, 16);

    if (bytes.size() != kHeaderSize + payload_size) {
        throw std::runtime_error("debug packet length mismatch");
    }

    std::vector<std::uint8_t> payload(
        bytes.begin() + static_cast<std::ptrdiff_t>(kHeaderSize),
        bytes.end());
    const std::uint32_t actual_hash = fnv1a(payload.data(), payload.size());
    if (actual_hash != expected_hash) {
        throw std::runtime_error("debug packet checksum mismatch");
    }

    return {command, request_id, std::move(payload)};
}
