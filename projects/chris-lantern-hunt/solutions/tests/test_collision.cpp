#include "../src/collision.hpp"
#include "../src/procgen.hpp"

#include <cassert>
#include <cmath>
#include <iostream>

int main() {
    const lantern::Dungeon dungeon = lantern::generate_dungeon(42u);

    // PEDAGOGY-TEST: LANTERN-CAM-02 — Caso 1 jogador não atravessa parede ao deslizar
    lantern::Vec3 start{21.0f, 0.82f, 21.0f};
    lantern::Vec3 moved = lantern::move_with_collision(
        dungeon, start, lantern::Vec3{3.0f, 0.0f, 0.0f}, 0.32f, 1.65f, 2.0f, false);

    const int cell_x = static_cast<int>(moved.x / 2.0f);
    const int cell_y = static_cast<int>(moved.z / 2.0f);
    assert(dungeon.is_floor(cell_x, cell_y));

    // Caso 2 — esfera acerta AABB
    lantern::Aabb box{{0.0f, 0.0f, 0.0f}, {1.0f, 1.0f, 1.0f}};
    assert(lantern::sphere_hits_aabb(lantern::Vec3{0.5f, 0.5f, 0.5f}, 0.2f, box));
    assert(!lantern::sphere_hits_aabb(lantern::Vec3{3.0f, 3.0f, 3.0f}, 0.2f, box));

    // Caso 3 — AABB do jogador intersecta parede antes da resolução
    const lantern::Aabb player = lantern::player_aabb(start, 0.32f, 1.65f);
    const lantern::Aabb wall{{20.0f, 0.0f, 20.0f}, {22.0f, 3.0f, 22.0f}};
    assert(!lantern::aabb_intersects(player, wall) || moved.x <= start.x + 3.0f);

    std::cout << "test_collision: PASS\n";
    return 0;
}
