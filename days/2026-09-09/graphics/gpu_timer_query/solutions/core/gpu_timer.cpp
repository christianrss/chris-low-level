#include "gpu_timer.hpp"

namespace gputq {

void GpuTimer::begin() {
    // PEDAGOGY-SOLUTION: GFX-TQ-BEGIN
    t0_ = std::chrono::steady_clock::now();
    active_ = true;
}

void GpuTimer::end() {
    // PEDAGOGY-SOLUTION: GFX-TQ-END
    if (!active_) {
        return;
    }
    const auto t1 = std::chrono::steady_clock::now();
    last_ms_ = std::chrono::duration<double, std::milli>(t1 - t0_).count();
    active_ = false;
}

double GpuTimer::last_ms() const {
    // PEDAGOGY-SOLUTION: GFX-TQ-READ
    return last_ms_;
}

}  // namespace gputq
