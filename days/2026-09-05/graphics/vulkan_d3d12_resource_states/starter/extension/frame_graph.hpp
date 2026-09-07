#pragma once
#include <string>
#include <vector>

// Frame graph pedagógico — liga estados GPU ao frame da artilharia (Day07 N9).
// Sem TODO no starter principal; leitura obrigatória após GFX-STATE-TRANSITION-01.

namespace gfx_frame {

enum class PassKind { Physics, TerrainRaster, ProjectileDraw, Present };

struct PassNode {
    PassKind kind{};
    std::string resource_name;
    std::string required_state;  // e.g. RENDER_TARGET / SHADER_RESOURCE
};

std::vector<PassNode> artillery_frame_graph();

}  // namespace gfx_frame
