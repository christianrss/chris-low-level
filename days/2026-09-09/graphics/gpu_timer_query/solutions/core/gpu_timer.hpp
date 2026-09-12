#pragma once

#include <chrono>

namespace gputq {

class GpuTimer {
public:
    void begin();
    void end();
    double last_ms() const;

private:
    bool active_ = false;
    std::chrono::steady_clock::time_point t0_{};
    double last_ms_ = 0.0;
};

}  // namespace gputq
