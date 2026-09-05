// SOLVES [GFX-STATE-TRANSITION-01] [GFX-VK-MAP-02] [GFX-D3D12-MAP-03]
#include "resource_state.hpp"
#include <stdexcept>
bool Tracker::transition(State n){if(n==s_)return false;bool ok=(s_==State::CopyDst&&n==State::ShaderRead)||(s_==State::ShaderRead&&n==State::RenderTarget)||(s_==State::RenderTarget&&n==State::Present)||(s_==State::Present&&n==State::RenderTarget);if(ok)s_=n;return ok;}
std::string Tracker::vk(State s){switch(s){case State::CopyDst:return "VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL";case State::ShaderRead:return "VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL";case State::RenderTarget:return "VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL";case State::Present:return "VK_IMAGE_LAYOUT_PRESENT_SRC_KHR";}throw std::runtime_error("state");}
std::string Tracker::d3d12(State s){switch(s){case State::CopyDst:return "D3D12_RESOURCE_STATE_COPY_DEST";case State::ShaderRead:return "D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE";case State::RenderTarget:return "D3D12_RESOURCE_STATE_RENDER_TARGET";case State::Present:return "D3D12_RESOURCE_STATE_PRESENT";}throw std::runtime_error("state");}
