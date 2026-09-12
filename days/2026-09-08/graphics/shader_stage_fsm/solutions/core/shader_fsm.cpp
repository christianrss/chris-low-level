#include "shader_fsm.hpp"

namespace shfsm {

ShaderFsm::ShaderFsm() : stage_(Stage::Edit) {}

Stage ShaderFsm::stage() const {
    return stage_;
}

void ShaderFsm::advance() {
    // PEDAGOGY-SOLUTION: GFX-SH-ADVANCE
    switch (stage_) {
    case Stage::Edit:
        stage_ = Stage::Compile;
        break;
    case Stage::Compile:
        stage_ = Stage::Link;
        break;
    case Stage::Link:
        stage_ = Stage::Ready;
        break;
    case Stage::Ready:
        stage_ = Stage::Edit;
        break;
    }
}

void ShaderFsm::reset() {
    // PEDAGOGY-SOLUTION: GFX-SH-RESET
    stage_ = Stage::Edit;
}

Rgb ShaderFsm::stage_color() const {
    // PEDAGOGY-SOLUTION: GFX-SH-COLOR
    switch (stage_) {
    case Stage::Edit:
        return {0.95f, 0.75f, 0.20f};
    case Stage::Compile:
        return {0.25f, 0.55f, 0.95f};
    case Stage::Link:
        return {0.70f, 0.35f, 0.90f};
    case Stage::Ready:
        return {0.25f, 0.85f, 0.40f};
    }
    return {1.0f, 1.0f, 1.0f};
}

}  // namespace shfsm
