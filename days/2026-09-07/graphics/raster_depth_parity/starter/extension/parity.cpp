#include "depth_buffer.hpp"
// TODO [GFX-DEPTH-PARITY-03]: red triangle behind must not win over blue in front
bool parity_scene_cpu(std::vector<depth_lab::Color>& fb, depth_lab::DepthBuffer& db) {
    (void)fb;
    (void)db;
    return false;
}
