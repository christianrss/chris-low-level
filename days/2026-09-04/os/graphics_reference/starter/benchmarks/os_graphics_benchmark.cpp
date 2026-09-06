#include "graphics.hpp"
#include <chrono>
#include <cstdint>
#include <iostream>
#include <vector>

int main() {
    constexpr std::size_t width = 640;
    constexpr std::size_t height = 360;
    constexpr int frames = 40;

    Surface window_a(320, 180, Pixel{200, 30, 30, 230});
    Surface window_b(300, 220, Pixel{30, 80, 220, 200});
    std::uint64_t checksum = 0;
    std::uint64_t pixels_full = 0;
    std::uint64_t pixels_damage = 0;

    const auto start_full = std::chrono::steady_clock::now();
    for (int frame = 0; frame < frames; ++frame) {
        const std::vector<Layer> layers = {
            {&window_a, 20 + frame, 30},
            {&window_b, 150, 80 + frame / 2},
        };
        const Surface output = Compositor::compose(
            width,
            height,
            Pixel{20, 20, 20, 255},
            layers);
        pixels_full += static_cast<std::uint64_t>(width) * height;
        const Pixel sample = output.pixel(frame % width, frame % height);
        checksum += sample.r + sample.g + sample.b;
    }
    const auto end_full = std::chrono::steady_clock::now();
    const double seconds_full =
        std::chrono::duration<double>(end_full - start_full).count();

    Surface framebuffer(width, height, Pixel{20, 20, 20, 255});
    DirtyTracker damage;
    damage.mark_dirty(0, 0, static_cast<int>(width), static_cast<int>(height));

    const auto start_damage = std::chrono::steady_clock::now();
    for (int frame = 0; frame < frames; ++frame) {
        const int ax = 20 + frame;
        const int by = 80 + frame / 2;
        // Conservative damage: previous+current footprints of both windows.
        damage.mark_dirty(ax - 1, 30, 321, 180);
        damage.mark_dirty(150, by - 1, 300, 221);
        const std::vector<Layer> layers = {
            {&window_a, ax, 30},
            {&window_b, 150, by},
        };
        const FrameStats stats = FramePacer::compose_with_damage(
            framebuffer,
            Pixel{20, 20, 20, 255},
            layers,
            damage);
        pixels_damage += stats.pixels_touched;
        const Pixel sample = framebuffer.pixel(frame % width, frame % height);
        checksum += sample.r + sample.g + sample.b;
    }
    const auto end_damage = std::chrono::steady_clock::now();
    const double seconds_damage =
        std::chrono::duration<double>(end_damage - start_damage).count();

    std::cout << "mode=full frames=" << frames
              << " seconds=" << seconds_full
              << " fps=" << frames / seconds_full
              << " pixels_touched=" << pixels_full << "\n";
    std::cout << "mode=damage frames=" << frames
              << " seconds=" << seconds_damage
              << " fps=" << frames / seconds_damage
              << " pixels_touched=" << pixels_damage
              << " checksum=" << checksum << "\n";
}
