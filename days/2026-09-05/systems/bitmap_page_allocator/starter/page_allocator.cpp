// TODO [SYS-PAGE-ALLOC-01] [SYS-PAGE-FREE-02]
#include "page_allocator.hpp"

PageBitTrace trace_page_to_bit(std::size_t page) {
    // TODO [SYS-PAGE-ALLOC-01]: retornar page, byte_index (page/8), bit_index (page%8)
    return {page, 0, 0};
}

PageAllocator::PageAllocator(std::size_t page_count)
    : page_count_(page_count), bits_((page_count + 7) / 8, 0) {}

bool PageAllocator::is_used(std::size_t page) const {
    // TODO [SYS-PAGE-ALLOC-01]: consultar bit no bitmap
    return true;
}

void PageAllocator::set_used(std::size_t page, bool used) {
    // TODO [SYS-PAGE-FREE-02]: setar ou limpar bit
}

int PageAllocator::allocate() {
    // TODO [SYS-PAGE-ALLOC-01]: primeira página livre ou -1 (OOM)
    return -1;
}

bool PageAllocator::free_page(std::size_t page) {
    // TODO [SYS-PAGE-FREE-02]: liberar página usada; rejeitar double-free
    return false;
}
