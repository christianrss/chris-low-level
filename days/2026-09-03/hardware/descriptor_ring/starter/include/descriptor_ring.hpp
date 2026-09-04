#pragma once
#include <cstddef>
#include <cstdint>
#include <optional>
#include <vector>

struct Descriptor {
    std::uint32_t length = 0;
    bool owned_by_device = false;
    bool completed = false;
};

class DescriptorRing {
public:
    explicit DescriptorRing(std::size_t capacity);
    bool submit(std::uint32_t length);
    bool device_complete_one();
    std::optional<std::uint32_t> reclaim();
    std::size_t outstanding() const { return count_; }
    std::size_t capacity() const { return ring_.size(); }

private:
    std::vector<Descriptor> ring_;
    std::size_t producer_ = 0;
    std::size_t device_ = 0;
    std::size_t consumer_ = 0;
    std::size_t count_ = 0;
    std::size_t device_pending_ = 0;
};
