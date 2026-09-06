#pragma once

#include <cstdint>
#include <vector>

namespace lantern {

constexpr int kDungeonWidth = 32;
constexpr int kDungeonHeight = 32;

enum class CellType : unsigned char {
    Wall = 0,
    Floor = 1,
    WaterShallow = 2,
    WaterDeep = 3,
    Slime = 4,
};

struct Room {
    int x = 0;
    int y = 0;
    int w = 0;
    int h = 0;
};

struct Dungeon {
    std::uint32_t seed = 0;
    int width = kDungeonWidth;
    int height = kDungeonHeight;
    std::vector<CellType> cells;
    std::vector<Room> rooms;

    CellType at(int x, int y) const;
    bool is_floor(int x, int y) const;
    bool is_walkable(int x, int y, bool swimming) const;
    bool is_water(int x, int y) const;
    int floor_count() const;
    int water_count() const;
};

Dungeon generate_dungeon(std::uint32_t seed);

} // namespace lantern
