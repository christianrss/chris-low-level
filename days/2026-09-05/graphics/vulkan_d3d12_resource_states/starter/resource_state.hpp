#pragma once
#include <string>

enum class State {
    CopyDst,
    ShaderRead,
    RenderTarget,
    Present,
};

class ResourceTracker {
public:
    explicit ResourceTracker(State state) : state_(state) {}
    bool transition(State next);
    State state() const { return state_; }

private:
    State state_;
};

std::string to_vulkan(State state);
std::string to_d3d12(State state);
