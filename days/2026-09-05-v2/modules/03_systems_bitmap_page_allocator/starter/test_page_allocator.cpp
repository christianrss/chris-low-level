// PEDAGOGY-TEST: SYS-PAGE-FREE-02
// PEDAGOGY-TEST: SYS-PAGE-ALLOC-01
// TESTS [SYS-PAGE-ALLOC-01] [SYS-PAGE-FREE-02]
#include "page_allocator.hpp"
#include <cassert>
#include <cstdio>
int main(){PageAllocator a(3);assert(a.allocate()==0);assert(a.allocate()==1);assert(a.allocate()==2);assert(a.allocate()==-1);assert(a.free_page(1));assert(!a.free_page(1));assert(a.allocate()==1);as
sert(!a.free_page(99));puts("OK allocator");}
