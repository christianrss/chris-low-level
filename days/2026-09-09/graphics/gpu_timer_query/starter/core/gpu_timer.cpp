#include "gpu_timer.hpp"

namespace gputq {

void GpuTimer::begin() {
    // TODO [GFX-TQ-BEGIN]: mark start time with steady_clock
    (void)active_;
}

void GpuTimer::end() {
    // TODO [GFX-TQ-END]: compute elapsed ms into last_ms_
    (void)active_;
}

double GpuTimer::last_ms() const {
    // TODO [GFX-TQ-READ]: return last measured milliseconds
    return -1.0;
}

}  // namespace gputq
