#include "arena.hpp"
#include <stdexcept>

Arena::Arena(std::size_t capacity) : storage_(capacity) {
    if (capacity == 0) {
        throw std::invalid_argument("arena capacity must be non-zero");
    }
}

bool Arena::is_power_of_two(std::size_t value) noexcept {
    return value != 0 && (value & (value - 1)) == 0;
}

std::size_t Arena::align_up(std::size_t value, std::size_t alignment) {
    if (!is_power_of_two(alignment)) {
        throw std::invalid_argument("alignment must be a power of two");
    }
    const std::size_t mask = alignment - 1;
    return (value + mask) & ~mask;
}

void* Arena::allocate(std::size_t size, std::size_t alignment) {
    if (size == 0) {
        throw std::invalid_argument("allocation size must be non-zero");
    }

    const std::size_t base = reinterpret_cast<std::uintptr_t>(storage_.data());
    const std::size_t aligned_address = align_up(base + offset_, alignment);
    const std::size_t aligned_offset = aligned_address - base;

    if (aligned_offset > storage_.size() || size > storage_.size() - aligned_offset) {
        throw std::bad_alloc();
    }

    offset_ = aligned_offset + size;
    return storage_.data() + static_cast<std::ptrdiff_t>(aligned_offset);
}

void Arena::reset() noexcept {
    offset_ = 0;
}
