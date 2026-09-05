// PEDAGOGY-TEST: SYS-PAGE-ALLOC-01: alocação sequencial e trace page→byte→bit
// PEDAGOGY-TEST: SYS-PAGE-FREE-02: OOM (-1) e rejeição de double-free
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `cmake -B build && cmake --build build` em starter/.
// Caso 2: **Trace page→byte→bit:** página 13 → byte 1, bit 5.
// Caso 3: **OOM:** alocador com 3 páginas retorna -1 na 4ª chamada.
// Caso 4: **Double-free:** `free_page` duas vezes na mesma página retorna false.
// Caso 5: **Out-of-range:** `free_page(99)` retorna false.
// Caso 6: Valide solutions/ com os mesmos testes.
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