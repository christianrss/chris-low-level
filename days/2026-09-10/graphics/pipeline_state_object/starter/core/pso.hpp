#pragma once

namespace pso {

constexpr int kTopoTriangles = 0;
constexpr int kTopoLines = 1;
constexpr int kFillSolid = 0;
constexpr int kFillWire = 1;
constexpr int kPresetCount = 3;

struct PipelineState {
    int topology = kTopoTriangles;
    int fill_mode = kFillSolid;
    float r = 1.0f;
    float g = 0.0f;
    float b = 0.0f;
};

PipelineState create_default_pso();
void bind(PipelineState& active, const PipelineState& src);
void cycle_pso(PipelineState& active, int& preset_index);
PipelineState preset_at(int index);

}  // namespace pso
