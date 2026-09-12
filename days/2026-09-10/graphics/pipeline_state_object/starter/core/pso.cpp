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
    // TODO [GFX-PSO-CREATE]: return preset_at(0) as the default solid-red PSO
    return PipelineState{};
}

void bind(PipelineState& active, const PipelineState& src) {
    // TODO [GFX-PSO-BIND]: copy src fields into active
    (void)active;
    (void)src;
}

void cycle_pso(PipelineState& active, int& preset_index) {
    // TODO [GFX-PSO-CYCLE]: advance preset_index mod 3 and bind that preset
    (void)active;
    (void)preset_index;
}

}  // namespace pso
