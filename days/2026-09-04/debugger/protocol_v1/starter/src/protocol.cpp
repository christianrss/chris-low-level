#include "protocol.hpp"
#include <cstddef>
#include <stdexcept>

static constexpr std::uint32_t kMagic = 0x31444B43U;
static constexpr std::uint16_t kVersion = 1;
static constexpr std::size_t kHeaderSize = 20;

static void append_u16(
    std::vector<std::uint8_t>& out,
    std::uint16_t value) {
    // TODO ETAPA 1
    (void)out;
    (void)value;
}
static void append_u32(
    std::vector<std::uint8_t>& out,
    std::uint32_t value) {
    // TODO ETAPA 1
    (void)out;
    (void)value;
}
static std::uint16_t read_u16(
    const std::vector<std::uint8_t>& bytes,
    std::size_t offset) {
    // TODO ETAPA 2
    (void)bytes;
    (void)offset;
    return 0;
}
static std::uint32_t read_u32(
    const std::vector<std::uint8_t>& bytes,
    std::size_t offset) {
    // TODO ETAPA 2
    (void)bytes;
    (void)offset;
    return 0;
}
static std::uint32_t fnv1a(
    const std::uint8_t* data,
    std::size_t size) {
    // TODO ETAPA 3
    (void)data;
    (void)size;
    return 0;
}
std::vector<std::uint8_t> encode_debug_packet(const DebugPacket& packet) {
    // TODO ETAPA 4
    (void)packet;
    return {};
}
DebugPacket decode_debug_packet(const std::vector<std::uint8_t>& bytes) {
    // TODO ETAPA 5
    (void)bytes;
    throw std::logic_error("TODO decode");
}
