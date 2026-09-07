#include "depth_buffer.hpp"
// PEDAGOGY-SOLUTION: GFX-DEPTH-PARITY-03
bool parity_scene_cpu(std::vector<depth_lab::Color>& fb, depth_lab::DepthBuffer& db) {
    db.clear(1.0f);
    for (int y = 0; y < db.height; ++y) {
        for (int x = 0; x < db.width; ++x) {
            const float z_back = 0.8f;
            const float z_front = 0.2f;
            if (db.test(x, y, z_back)) {
                fb[static_cast<std::size_t>(y) * db.width + x] = {200, 0, 0};
            }
            if (db.test(x, y, z_front)) {
                fb[static_cast<std::size_t>(y) * db.width + x] = {0, 0, 200};
            }
        }
    }
    return true;
}
