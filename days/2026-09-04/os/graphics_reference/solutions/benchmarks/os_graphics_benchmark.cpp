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

    const auto start = std::chrono::steady_clock::now();
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
        const Pixel sample = output.pixel(frame % width, frame % height);
        checksum += sample.r + sample.g + sample.b;
    }
    const auto end = std::chrono::steady_clock::now();
    const double seconds = std::chrono::duration<double>(end - start).count();
    std::cout << "frames=" << frames
              << " seconds=" << seconds
              << " fps=" << frames / seconds
              << " checksum=" << checksum << "\n";
}
