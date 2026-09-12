// PEDAGOGY-TEST: GFX-TQ-BEGIN
// PEDAGOGY-TEST: GFX-TQ-END
// PEDAGOGY-TEST: GFX-TQ-READ
// Test cases (TESTES_GUIADOS.md):
// Caso 1: begin() arma o relogio (GFX-TQ-BEGIN).
// Caso 2: end() grava elapsed ms (GFX-TQ-END).
// Caso 3: last_ms() devolve a ultima medicao (GFX-TQ-READ).
#include <cassert>
#include <chrono>
#include <thread>
#include "gpu_timer.hpp"

using namespace gputq;

int main() {
    GpuTimer t;
    assert(t.last_ms() == 0.0 || t.last_ms() >= 0.0);
    t.begin();
    std::this_thread::sleep_for(std::chrono::milliseconds(5));
    t.end();
    const double ms = t.last_ms();
    assert(ms >= 1.0);
    assert(ms < 5000.0);
    const double again = t.last_ms();
    assert(again == ms);
    return 0;
}
