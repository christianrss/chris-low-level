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
    // TODO [SYS-PAGE-ALLOC-01]
    return -1;
}

bool PageAllocator::free_page(std::size_t page) {
    // TODO [SYS-PAGE-FREE-02]
    (void)page;
    return false;
}
