#pragma once

#include <string>

namespace lantern {

// LANTERN-AUDIO-08: ambiente em loop + passos one-shot via miniaudio.
class AudioEngine {
public:
    bool initialize(const std::string& ambient_path, const std::string& footstep_path,
        const std::string& shoot_path);
    void shutdown();

    void play_footstep();
    void play_shoot();
    void update_movement_cooldown(float delta_seconds);

private:
    bool initialized_ = false;
    float footstep_cooldown_ = 0.0f;
};

} // namespace lantern
