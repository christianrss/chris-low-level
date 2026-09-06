#include "procgen.hpp"

#include <algorithm>
#include <random>

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

bool Dungeon::is_walkable(int x, int y, bool swimming) const {
    const CellType cell = at(x, y);
    if (cell == CellType::Wall) {
        return false;
    }
    if (cell == CellType::WaterDeep && !swimming) {
        return false;
    }
    return cell == CellType::Floor || cell == CellType::Slime || cell == CellType::WaterShallow ||
           cell == CellType::WaterDeep;
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

namespace {

void carve_h_corridor(Dungeon& dungeon, int x0, int x1, int y) {
    const int start = std::min(x0, x1);
    const int end = std::max(x0, x1);
    for (int x = start; x <= end; ++x) {
        if (x >= 0 && x < dungeon.width && y >= 0 && y < dungeon.height) {
            dungeon.cells[static_cast<std::size_t>(y * dungeon.width + x)] = CellType::Floor;
        }
    }
}

void carve_v_corridor(Dungeon& dungeon, int y0, int y1, int x) {
    const int start = std::min(y0, y1);
    const int end = std::max(y0, y1);
    for (int y = start; y <= end; ++y) {
        if (x >= 0 && x < dungeon.width && y >= 0 && y < dungeon.height) {
            dungeon.cells[static_cast<std::size_t>(y * dungeon.width + x)] = CellType::Floor;
        }
    }
}

bool overlaps(const Room& a, const Room& b, int padding) {
    return a.x < b.x + b.w + padding && a.x + a.w + padding > b.x && a.y < b.y + b.h + padding &&
           a.y + a.h + padding > b.y;
}

void carve_room(Dungeon& dungeon, const Room& room) {
    for (int y = room.y; y < room.y + room.h; ++y) {
        for (int x = room.x; x < room.x + room.w; ++x) {
            dungeon.cells[static_cast<std::size_t>(y * dungeon.width + x)] = CellType::Floor;
        }
    }
}

// PEDAGOGY-SOLUTION: LANTERN-WATER-12 — lago shallow+deep na primeira sala grande.
void carve_water_pool(Dungeon& dungeon, std::mt19937& rng) {
    if (dungeon.rooms.empty()) {
        return;
    }

    const Room& room = dungeon.rooms[rng() % dungeon.rooms.size()];
    const int pool_w = std::max(3, room.w / 2);
    const int pool_h = std::max(3, room.h / 2);
    const int start_x = room.x + (room.w - pool_w) / 2;
    const int start_y = room.y + (room.h - pool_h) / 2;

    for (int y = start_y; y < start_y + pool_h; ++y) {
        for (int x = start_x; x < start_x + pool_w; ++x) {
            const bool deep = x > start_x && x < start_x + pool_w - 1 && y > start_y && y < start_y + pool_h - 1;
            dungeon.cells[static_cast<std::size_t>(y * dungeon.width + x)] =
                deep ? CellType::WaterDeep : CellType::WaterShallow;
        }
    }
}

void scatter_slime(Dungeon& dungeon, std::mt19937& rng) {
    std::uniform_int_distribution<int> x_dist(1, dungeon.width - 2);
    std::uniform_int_distribution<int> y_dist(1, dungeon.height - 2);
    for (int i = 0; i < 6; ++i) {
        const int x = x_dist(rng);
        const int y = y_dist(rng);
        if (dungeon.is_floor(x, y)) {
            dungeon.cells[static_cast<std::size_t>(y * dungeon.width + x)] = CellType::Slime;
        }
    }
}

} // namespace

Dungeon generate_dungeon(std::uint32_t seed) {
    // PEDAGOGY-SOLUTION: LANTERN-PROC-01
    Dungeon dungeon{};
    dungeon.seed = seed;
    dungeon.width = kDungeonWidth;
    dungeon.height = kDungeonHeight;
    dungeon.cells.assign(static_cast<std::size_t>(dungeon.width * dungeon.height), CellType::Wall);

    std::mt19937 rng(seed);
    std::uniform_int_distribution<int> room_w_dist(4, 7);
    std::uniform_int_distribution<int> room_h_dist(4, 7);
    std::uniform_int_distribution<int> x_dist(1, dungeon.width - 8);
    std::uniform_int_distribution<int> y_dist(1, dungeon.height - 8);

    constexpr int kTargetRooms = 8;
    constexpr int kMaxAttempts = 120;

    for (int attempt = 0; attempt < kMaxAttempts && static_cast<int>(dungeon.rooms.size()) < kTargetRooms;
         ++attempt) {
        Room room{};
        room.w = room_w_dist(rng);
        room.h = room_h_dist(rng);
        room.x = x_dist(rng);
        room.y = y_dist(rng);

        if (room.x + room.w >= dungeon.width - 1 || room.y + room.h >= dungeon.height - 1) {
            continue;
        }

        bool blocked = false;
        for (const Room& existing : dungeon.rooms) {
            if (overlaps(room, existing, 2)) {
                blocked = true;
                break;
            }
        }

        if (blocked) {
            continue;
        }

        carve_room(dungeon, room);
        dungeon.rooms.push_back(room);
    }

    std::sort(dungeon.rooms.begin(), dungeon.rooms.end(), [](const Room& a, const Room& b) {
        return a.x < b.x;
    });

    for (std::size_t i = 1; i < dungeon.rooms.size(); ++i) {
        const Room& prev = dungeon.rooms[i - 1];
        const Room& current = dungeon.rooms[i];
        const int prev_cx = prev.x + prev.w / 2;
        const int prev_cy = prev.y + prev.h / 2;
        const int cur_cx = current.x + current.w / 2;
        const int cur_cy = current.y + current.h / 2;

        if (rng() % 2 == 0) {
            carve_h_corridor(dungeon, prev_cx, cur_cx, prev_cy);
            carve_v_corridor(dungeon, prev_cy, cur_cy, cur_cx);
        } else {
            carve_v_corridor(dungeon, prev_cy, cur_cy, prev_cx);
            carve_h_corridor(dungeon, prev_cx, cur_cx, cur_cy);
        }
    }

    carve_water_pool(dungeon, rng);
    scatter_slime(dungeon, rng);

    return dungeon;
}

} // namespace lantern
