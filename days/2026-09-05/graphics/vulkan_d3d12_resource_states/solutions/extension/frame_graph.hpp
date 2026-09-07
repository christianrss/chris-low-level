#pragma once
#include <string>
#include <vector>

namespace gfx_frame {

enum class PassKind { Physics, TerrainRaster, ProjectileDraw, Present };

struct PassNode {
    PassKind kind{};
    std::string resource_name;
    std::string required_state;
};

std::vector<PassNode> artillery_frame_graph();

}  // namespace gfx_frame
