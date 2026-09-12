#include "pso.hpp"

namespace pso {

PipelineState preset_at(int index) {
    const int i = ((index % kPresetCount) + kPresetCount) % kPresetCount;
    if (i == 0) {
        return PipelineState{kTopoTriangles, kFillSolid, 0.95f, 0.25f, 0.20f};
    }
    if (i == 1) {
        return PipelineState{kTopoTriangles, kFillWire, 0.25f, 0.90f, 0.35f};
    }
    return PipelineState{kTopoTriangles, kFillSolid, 0.25f, 0.45f, 0.95f};
}

PipelineState create_default_pso() {
    // PEDAGOGY-SOLUTION: GFX-PSO-CREATE
    return preset_at(0);
}

void bind(PipelineState& active, const PipelineState& src) {
    // PEDAGOGY-SOLUTION: GFX-PSO-BIND
    active = src;
}

void cycle_pso(PipelineState& active, int& preset_index) {
    // PEDAGOGY-SOLUTION: GFX-PSO-CYCLE
    preset_index = (preset_index + 1) % kPresetCount;
    bind(active, preset_at(preset_index));
}

}  // namespace pso
