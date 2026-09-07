#include "frame_graph.hpp"

namespace gfx_frame {

std::vector<PassNode> artillery_frame_graph() {
    return {
        {PassKind::Physics, "sim_buffer", "GENERAL"},
        {PassKind::TerrainRaster, "color_rt", "RENDER_TARGET"},
        {PassKind::ProjectileDraw, "color_rt", "RENDER_TARGET"},
        {PassKind::Present, "swapchain", "PRESENT"},
    };
}

}  // namespace gfx_frame
