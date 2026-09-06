#include "procgen.hpp"

namespace lantern {

CellType Dungeon::at(int x, int y) const {
    if (x < 0 || y < 0 || x >= width || y >= height) {
        return CellType::Wall;
    }
    return cells[static_cast<std::size_t>(y * width + x)];
}

bool Dungeon::is_floor(int x, int y) const {
    const CellType cell = at(x, y);
    return cell == CellType::Floor || cell == CellType::Slime;
}

bool Dungeon::is_water(int x, int y) const {
    const CellType cell = at(x, y);
    return cell == CellType::WaterShallow || cell == CellType::WaterDeep;
}

bool Dungeon::is_walkable(int x, int y, bool /*swimming*/) const {
    // TODO [LANTERN-WATER-12]: carve_water_pool + is_walkable com swimming.
    return is_floor(x, y);
}

int Dungeon::floor_count() const {
    int count = 0;
    for (const CellType cell : cells) {
        if (cell == CellType::Floor || cell == CellType::Slime) {
            ++count;
        }
    }
    return count;
}

int Dungeon::water_count() const {
    int count = 0;
    for (const CellType cell : cells) {
        if (cell == CellType::WaterShallow || cell == CellType::WaterDeep) {
            ++count;
        }
    }
    return count;
}

Dungeon generate_dungeon(std::uint32_t seed) {
    // TODO [LANTERN-PROC-01]: salas + corredores determinísticos.
    Dungeon dungeon{};
    dungeon.seed = seed;
    dungeon.width = kDungeonWidth;
    dungeon.height = kDungeonHeight;
    dungeon.cells.assign(static_cast<std::size_t>(dungeon.width * dungeon.height), CellType::Wall);

    Room starter_room{8, 8, 6, 6};
    dungeon.rooms.push_back(starter_room);
    for (int y = starter_room.y; y < starter_room.y + starter_room.h; ++y) {
        for (int x = starter_room.x; x < starter_room.x + starter_room.w; ++x) {
            dungeon.cells[static_cast<std::size_t>(y * dungeon.width + x)] = CellType::Floor;
        }
    }

    return dungeon;
}

} // namespace lantern
