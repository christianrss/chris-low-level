// PEDAGOGY-TEST: D2-ARENA-POWER2
// PEDAGOGY-TEST: D2-ARENA-ALIGN-UP
// PEDAGOGY-TEST: D2-ARENA-ALLOCATE
// PEDAGOGY-TEST: D2-ARENA-RESET
#include "arena.hpp"
#include <cassert>
#include <cstdint>
#include <iostream>
#include <new>
#include <stdexcept>

int main() {
    Arena arena(1024);

    void* first = arena.allocate(7, 8);
    void* second = arena.allocate(32, 32);
    assert(reinterpret_cast<std::uintptr_t>(first) % 8 == 0);
    assert(reinterpret_cast<std::uintptr_t>(second) % 32 == 0);
    assert(arena.used() >= 39);

    const auto used_before_reset = arena.used();
    assert(used_before_reset > 0);
    arena.reset();
    assert(arena.used() == 0);

    bool bad_alignment = false;
    try {
        arena.allocate(8, 3);
    } catch (const std::invalid_argument&) {
        bad_alignment = true;
    }
    assert(bad_alignment);

    bool exhausted = false;
    try {
        arena.allocate(2048, 8);
    } catch (const std::bad_alloc&) {
        exhausted = true;
    }
    assert(exhausted);

    std::cout << "chris-arena tests passed\n";
}
