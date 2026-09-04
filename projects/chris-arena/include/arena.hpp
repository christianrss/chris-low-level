#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>

class Arena {
public:
    explicit Arena(std::size_t capacity);

    void* allocate(std::size_t size, std::size_t alignment);
    void reset() noexcept;

    std::size_t used() const noexcept { return offset_; }
    std::size_t capacity() const noexcept { return storage_.size(); }

private:
    static bool is_power_of_two(std::size_t value) noexcept;
    static std::size_t align_up(std::size_t value, std::size_t alignment);

    std::vector<std::byte> storage_;
    std::size_t offset_ = 0;
};
