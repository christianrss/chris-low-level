#include "audio.hpp"

namespace lantern {

bool AudioEngine::initialize(const std::string& /*ambient_path*/, const std::string& /*footstep_path*/,
    const std::string& /*shoot_path*/) {
    // TODO [LANTERN-AUDIO-08]: miniaudio engine + loop ambiente + one-shot passos (cooldown 350 ms).
    initialized_ = false;
    return false;
}

void AudioEngine::shutdown() {
    initialized_ = false;
}

void AudioEngine::play_footstep() {}

void AudioEngine::play_shoot() {}

void AudioEngine::update_movement_cooldown(float /*delta_seconds*/) {}

} // namespace lantern
