#include "../src/procgen.hpp"

#include <cassert>
#include <iostream>

int main() {
    // PEDAGOGY-TEST: LANTERN-PROC-01 — Caso 1 seed fixa reproduz layout
    const lantern::Dungeon first = lantern::generate_dungeon(42u);
    const lantern::Dungeon second = lantern::generate_dungeon(42u);
    assert(first.floor_count() == second.floor_count());
    assert(first.rooms.size() == second.rooms.size());

    for (int y = 0; y < first.height; ++y) {
        for (int x = 0; x < first.width; ++x) {
            assert(first.at(x, y) == second.at(x, y));
        }
    }

    // Caso 2 — seed 42 produz quantidade de salas esperada
    assert(first.rooms.size() >= 6);
    assert(first.floor_count() >= 180);

    // Caso 3 — seed 42 inclui água (LANTERN-WATER-12)
    assert(first.water_count() >= 8);

    std::cout << "test_procgen: PASS seed=" << first.seed << " floors=" << first.floor_count()
              << " rooms=" << first.rooms.size() << '\n';
    return 0;
}
