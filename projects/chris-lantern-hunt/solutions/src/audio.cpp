#include "audio.hpp"

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>

#define MINIAUDIO_IMPLEMENTATION
#include "../../third_party/miniaudio.h"

#include <iostream>

namespace lantern {

namespace {
constexpr float kFootstepCooldownSeconds = 0.35f;

ma_engine engine{};
ma_sound ambient_sound{};
ma_sound footstep_sound{};
ma_sound shoot_sound{};
} // namespace

bool AudioEngine::initialize(
    const std::string& ambient_path,
    const std::string& footstep_path,
    const std::string& shoot_path) {
    if (ma_engine_init(nullptr, &engine) != MA_SUCCESS) {
        // PEDAGOGY-SOLUTION: LANTERN-AUDIO-08
        std::cerr << "miniaudio engine init failed\n";
        return false;
    }

    if (ma_sound_init_from_file(&engine, ambient_path.c_str(), MA_SOUND_FLAG_STREAM, nullptr, nullptr,
            &ambient_sound) != MA_SUCCESS) {
        std::cerr << "Failed to load ambient: " << ambient_path << '\n';
        ma_engine_uninit(&engine);
        return false;
    }

    ma_sound_set_looping(&ambient_sound, MA_TRUE);
    ma_sound_start(&ambient_sound);

    if (ma_sound_init_from_file(&engine, footstep_path.c_str(), 0, nullptr, nullptr, &footstep_sound) !=
        MA_SUCCESS) {
        std::cerr << "Failed to load footstep: " << footstep_path << '\n';
    }

    if (ma_sound_init_from_file(&engine, shoot_path.c_str(), 0, nullptr, nullptr, &shoot_sound) !=
        MA_SUCCESS) {
        std::cerr << "Failed to load shoot: " << shoot_path << '\n';
    }

    initialized_ = true;
    return true;
}

void AudioEngine::shutdown() {
    if (!initialized_) {
        return;
    }

    ma_sound_uninit(&shoot_sound);
    ma_sound_uninit(&footstep_sound);
    ma_sound_uninit(&ambient_sound);
    ma_engine_uninit(&engine);
    initialized_ = false;
}

void AudioEngine::play_footstep() {
    if (!initialized_ || footstep_cooldown_ > 0.0f) {
        return;
    }

    ma_sound_seek_to_pcm_frame(&footstep_sound, 0);
    ma_sound_start(&footstep_sound);
    footstep_cooldown_ = kFootstepCooldownSeconds;
}

void AudioEngine::play_shoot() {
    if (!initialized_) {
        return;
    }

    ma_sound_seek_to_pcm_frame(&shoot_sound, 0);
    ma_sound_start(&shoot_sound);
}

void AudioEngine::update_movement_cooldown(float delta_seconds) {
    if (footstep_cooldown_ > 0.0f) {
        footstep_cooldown_ -= delta_seconds;
    }
}

} // namespace lantern
