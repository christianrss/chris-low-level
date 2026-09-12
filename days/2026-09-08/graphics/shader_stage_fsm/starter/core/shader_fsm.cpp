#include "shader_fsm.hpp"

namespace shfsm {

ShaderFsm::ShaderFsm() : stage_(Stage::Edit) {}

Stage ShaderFsm::stage() const {
    return stage_;
}

void ShaderFsm::advance() {
    // TODO [GFX-SH-ADVANCE]: EDIT->COMPILE->LINK->READY->EDIT
    (void)stage_;
}

void ShaderFsm::reset() {
    // TODO [GFX-SH-RESET]: return to EDIT
    (void)stage_;
}

Rgb ShaderFsm::stage_color() const {
    // TODO [GFX-SH-COLOR]: map Stage to RGB floats in [0,1]
    return {0.0f, 0.0f, 0.0f};
}

}  // namespace shfsm
