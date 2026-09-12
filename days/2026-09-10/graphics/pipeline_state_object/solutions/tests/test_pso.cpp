// PEDAGOGY-TEST: GFX-PSO-CREATE
// PEDAGOGY-TEST: GFX-PSO-BIND
// PEDAGOGY-TEST: GFX-PSO-CYCLE
// Test cases (TESTES_GUIADOS.md):
// Caso 1: create_default_pso() returns solid fill + red-ish color (GFX-PSO-CREATE).
// Caso 2: bind() copies topology/fill/color into active (GFX-PSO-BIND).
// Caso 3: cycle_pso() rotates through 3 presets (GFX-PSO-CYCLE).
#include <cassert>
#include <cmath>
#include "pso.hpp"

using namespace pso;

int main() {
    PipelineState def = create_default_pso();
    assert(def.fill_mode == kFillSolid);
    assert(def.r > 0.5f);

    PipelineState active{};
    PipelineState src = preset_at(1);
    bind(active, src);
    assert(active.fill_mode == kFillWire);
    assert(std::fabs(active.g - src.g) < 1e-5f);

    int idx = 0;
    bind(active, create_default_pso());
    cycle_pso(active, idx);
    assert(idx == 1);
    assert(active.fill_mode == kFillWire);
    cycle_pso(active, idx);
    assert(idx == 2);
    assert(active.b > 0.5f);
    cycle_pso(active, idx);
    assert(idx == 0);
    assert(active.fill_mode == kFillSolid);
    return 0;
}
