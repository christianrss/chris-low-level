#include "descriptor_ring.hpp"
#include <stdexcept>

DescriptorRing::DescriptorRing(std::size_t capacity) : ring_(capacity) {
    if (capacity == 0) throw std::invalid_argument("ring capacity must be non-zero");
}

bool DescriptorRing::submit(std::uint32_t) {
    // TODO: full check, descriptor ownership and producer wrap-around.
    return false;
}

bool DescriptorRing::device_complete_one() {
    // TODO: complete the next device-owned descriptor.
    return false;
}

std::optional<std::uint32_t> DescriptorRing::reclaim() {
    // TODO: return completed descriptors in consumer order.
    return std::nullopt;
}
