#include "descriptor_ring.hpp"
#include <stdexcept>

DescriptorRing::DescriptorRing(std::size_t capacity) : ring_(capacity) {
    if (capacity == 0) {
        throw std::invalid_argument("ring capacity must be non-zero");
    }
}

bool DescriptorRing::submit(std::uint32_t length) {
    if (count_ == ring_.size()) {
        return false;
    }
    auto& desc = ring_[producer_];
    desc.length = length;
    desc.owned_by_device = true;
    desc.completed = false;
    producer_ = (producer_ + 1) % ring_.size();
    ++count_;
    ++device_pending_;
    return true;
}

bool DescriptorRing::device_complete_one() {
    if (device_pending_ == 0) {
        return false;
    }
    auto& desc = ring_[device_];
    if (!desc.owned_by_device || desc.completed) {
        throw std::logic_error("ring ownership invariant broken");
    }
    desc.completed = true;
    desc.owned_by_device = false;
    device_ = (device_ + 1) % ring_.size();
    --device_pending_;
    return true;
}

std::optional<std::uint32_t> DescriptorRing::reclaim() {
    if (count_ == 0) {
        return std::nullopt;
    }
    auto& desc = ring_[consumer_];
    if (!desc.completed) {
        return std::nullopt;
    }
    const auto length = desc.length;
    desc = Descriptor{};
    consumer_ = (consumer_ + 1) % ring_.size();
    --count_;
    return length;
}
