#include "descriptor_ring.hpp"
#include <stdexcept>

DescriptorRing::DescriptorRing(std::size_t capacity) : ring_(capacity) {
    if (capacity == 0) throw std::invalid_argument("ring capacity must be non-zero");
}

bool DescriptorRing::submit(std::uint32_t) {
    // TODO [RING-SUBMIT-01]: full check, descriptor ownership and producer wrap-around.
    return false;
}

bool DescriptorRing::device_complete_one() {
    // TODO [RING-COMPLETE-01]: complete the next device-owned descriptor.
    return false;
}

std::optional<std::uint32_t> DescriptorRing::reclaim() {
    // TODO [RING-RECLAIM-01]: return completed descriptors in consumer order.
    return std::nullopt;
}
