// TESTS [GFX-STATE-TRANSITION-01] [GFX-VK-MAP-02] [GFX-D3D12-MAP-03]
#include "resource_state.hpp"
#include <cassert>
#include <cstdio>
int main(){Tracker t(State::CopyDst);assert(t.transition(State::ShaderRead));assert(t.transition(State::RenderTarget));assert(t.transition(State::Present));assert(!t.transition(State::Present));assert(t.transition(State::RenderTarget));assert(Tracker::vk(State::Present).find("PRESENT")!=std::string::npos);assert(Tracker::d3d12(State::CopyDst).find("COPY_DEST")!=std::string::npos);puts("OK graphics states");}
