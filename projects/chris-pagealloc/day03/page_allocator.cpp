// SOLVES [SYS-PAGE-ALLOC-01]
// SOLVES [SYS-PAGE-FREE-02]
#include "page_allocator.hpp"

PageAllocator::PageAllocator(std::size_t page_count)
    : page_count_(page_count), bits_((page_count + 7) / 8, 0) {}

bool PageAllocator::is_used(std::size_t page) const {
    if (page >= page_count_) {
        return true;
    }
    return (bits_[page / 8] & (1u << (page % 8))) != 0;
}

void PageAllocator::set_used(std::size_t page, bool used) {
    const auto mask = static_cast<std::uint8_t>(1u << (page % 8));
    if (used) {
        bits_[page / 8] |= mask;
    } else {
        bits_[page / 8] &= static_cast<std::uint8_t>(~mask);
    }
}

int PageAllocator::allocate() {
    for (std::size_t page = 0; page < page_count_; ++page) {
        if (!is_used(page)) {
            set_used(page, true);
            return static_cast<int>(page);
        }
    }
    return -1;
}

bool PageAllocator::free_page(std::size_t page) {
    if (page >= page_count_ || !is_used(page)) {
        return false;
    }
    set_used(page, false);
    return true;
}
