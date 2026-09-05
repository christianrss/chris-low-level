#include "page_allocator.hpp"
#include <cassert>
#include <iostream>

int main() {
    PageAllocator allocator(3);
    assert(allocator.allocate() == 0);
    assert(allocator.allocate() == 1);
    assert(allocator.allocate() == 2);
    assert(allocator.allocate() == -1);
    assert(allocator.free_page(1));
    assert(!allocator.free_page(1));
    assert(allocator.allocate() == 1);
    std::cout << "OK page allocator\n";
}
