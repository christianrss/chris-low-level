#include "measure.hpp"
#include <cmath>

StateVector2::StateVector2() : state_(4) {
    state_[0] = {1.0, 0.0};
}

double StateVector2::probability(std::size_t index) const {
    const auto& a = state_[index];
    return std::norm(a);
}

void StateVector2::apply_h(std::size_t qubit) {
    const double inv = 1.0 / std::sqrt(2.0);
    if (qubit == 0) {
        const auto a0 = state_[0], a1 = state_[1], a2 = state_[2], a3 = state_[3];
        state_[0] = inv * (a0 + a1);
        state_[1] = inv * (a2 + a3);
        state_[2] = inv * (a0 - a1);
        state_[3] = inv * (a2 - a3);
    }
}

double StateVector2::measure_probability(std::size_t index) const {
    // PEDAGOGY-SOLUTION: Q-MEAS-01
    return probability(index);
}

void StateVector2::collapse_to(std::size_t index) {
    // PEDAGOGY-SOLUTION: Q-MEAS-02
    for (std::size_t i = 0; i < state_.size(); ++i) {
        state_[i] = (i == index) ? std::complex<double>{1.0, 0.0} : std::complex<double>{0.0, 0.0};
    }
}

std::size_t StateVector2::born_select(const std::vector<double>& probs, double u) {
    // PEDAGOGY-SOLUTION: Q-BORN-03
    double acc = 0.0;
    for (std::size_t i = 0; i < probs.size(); ++i) {
        acc += probs[i];
        if (u < acc) return i;
    }
    return probs.empty() ? 0 : probs.size() - 1;
}
