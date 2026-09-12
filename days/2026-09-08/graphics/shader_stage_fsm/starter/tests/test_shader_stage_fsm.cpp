// PEDAGOGY-TEST: GFX-SH-ADVANCE
// PEDAGOGY-TEST: GFX-SH-RESET
// PEDAGOGY-TEST: GFX-SH-COLOR
// Test cases (TESTES_GUIADOS.md):
// Caso 1: advance() walks EDIT->COMPILE->LINK->READY->EDIT (GFX-SH-ADVANCE).
// Caso 2: reset() returns to EDIT from any stage (GFX-SH-RESET).
// Caso 3: stage_color() returns distinct RGB per stage (GFX-SH-COLOR).
#include <cassert>
#include <cmath>
#include "shader_fsm.hpp"

using namespace shfsm;

static bool near(float a, float b) {
    return std::fabs(a - b) < 1e-4f;
}

int main() {
    ShaderFsm fsm;
    assert(fsm.stage() == Stage::Edit);
    fsm.advance();
    assert(fsm.stage() == Stage::Compile);
    fsm.advance();
    assert(fsm.stage() == Stage::Link);
    fsm.advance();
    assert(fsm.stage() == Stage::Ready);
    fsm.advance();
    assert(fsm.stage() == Stage::Edit);

    fsm.advance();
    fsm.advance();
    assert(fsm.stage() == Stage::Link);
    fsm.reset();
    assert(fsm.stage() == Stage::Edit);

    const Rgb c0 = fsm.stage_color();
    assert(near(c0.r, 0.95f) && near(c0.g, 0.75f) && near(c0.b, 0.20f));
    fsm.advance();
    const Rgb c1 = fsm.stage_color();
    assert(near(c1.r, 0.25f) && near(c1.g, 0.55f) && near(c1.b, 0.95f));
    fsm.advance();
    const Rgb c2 = fsm.stage_color();
    assert(near(c2.r, 0.70f) && near(c2.g, 0.35f) && near(c2.b, 0.90f));
    fsm.advance();
    const Rgb c3 = fsm.stage_color();
    assert(near(c3.r, 0.25f) && near(c3.g, 0.85f) && near(c3.b, 0.40f));
    return 0;
}
