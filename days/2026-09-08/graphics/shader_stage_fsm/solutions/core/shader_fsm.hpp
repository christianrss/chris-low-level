#pragma once

namespace shfsm {

enum class Stage {
    Edit = 0,
    Compile = 1,
    Link = 2,
    Ready = 3,
};

struct Rgb {
    float r = 0.0f;
    float g = 0.0f;
    float b = 0.0f;
};

class ShaderFsm {
public:
    ShaderFsm();
    Stage stage() const;
    void advance();
    void reset();
    Rgb stage_color() const;

private:
    Stage stage_;
};

}  // namespace shfsm
