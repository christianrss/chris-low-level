// PEDAGOGY-TEST: Q-MEAS-01
// PEDAGOGY-TEST: Q-MEAS-02
// PEDAGOGY-TEST: Q-BORN-03
// Caso 1: |0> após H em q0 tem P(0)=P(1)=0.5
// Caso 2: collapse_to(1) deixa amplitude 1 em índice 1
// Caso 3: born_select com u=0.25 escolhe índice 1 quando probs={0.5,0.5}
#include <cassert>
#include <cmath>
#include "measure.hpp"

int main() {
    StateVector2 sv;
    sv.apply_h(0);
    assert(std::fabs(sv.measure_probability(0) - 0.5) < 1e-6);
    assert(std::fabs(sv.measure_probability(1) - 0.5) < 1e-6);
    sv.collapse_to(1);
    assert(std::fabs(sv.probability(1) - 1.0) < 1e-6);
    const std::vector<double> p = {0.5, 0.5};
    assert(StateVector2::born_select(p, 0.25) == 1);
    return 0;
}
