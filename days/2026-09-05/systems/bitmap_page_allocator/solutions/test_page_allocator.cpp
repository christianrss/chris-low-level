// PEDAGOGY-TEST [SYS-PAGE-ALLOC-01]: alocação sequencial e trace page→byte→bit
// PEDAGOGY-TEST [SYS-PAGE-FREE-02]: OOM (-1) e rejeição de double-free
#include "page_allocator.hpp"
#include <cassert>
#include <iostream>

int main() {
    const auto trace = trace_page_to_bit(13);
    assert(trace.page == 13);
    assert(trace.byte_index == 1);
    assert(trace.bit_index == 5);

    PageAllocator alloc(3);
    assert(alloc.allocate() == 0);
    assert(alloc.allocate() == 1);
    assert(alloc.allocate() == 2);
    assert(alloc.allocate() == -1);

    assert(alloc.free_page(1));
    assert(!alloc.is_used(1));
    assert(alloc.allocate() == 1);

    assert(!alloc.free_page(1));
    assert(!alloc.free_page(99));

    std::cout << "OK page allocator\n";
    return 0;
}
