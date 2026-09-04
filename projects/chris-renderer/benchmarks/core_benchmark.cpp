#include "engine.hpp"
#include <chrono>
#include <cstdint>
#include <iostream>

int main() {
    using clock = std::chrono::steady_clock;
    constexpr std::uint64_t iterations = 1'000'000;
    lab3d::SceneState scene{};
    std::uint64_t draw_items = 0;
    for (int i=0;i<1000;++i) { lab3d::physics_step(scene, 1.0f/120.0f); draw_items += lab3d::build_draw_list(scene).size(); }
    const auto t0=clock::now();
    for (std::uint64_t i=0;i<iterations;++i) {
        lab3d::physics_step(scene, 1.0f/120.0f);
        draw_items += lab3d::build_draw_list(scene).size();
    }
    const auto t1=clock::now();
    const double sec=std::chrono::duration<double>(t1-t0).count();
    std::cout << "iterations=" << iterations << " seconds=" << sec
              << " ns_per_iteration=" << (sec*1e9/iterations)
              << " checksum=" << draw_items << "\n";
}
