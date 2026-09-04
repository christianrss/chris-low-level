#include "qsim.hpp"
#include <cmath>
#include <stdexcept>

StateVector::StateVector(std::size_t qubits) : qubits_(qubits) {
    if (qubits == 0 || qubits > 24) {
        throw std::invalid_argument("qubit count must be between 1 and 24");
    }
    state_.assign(std::size_t{1} << qubits, {0.0, 0.0});
    state_[0] = {1.0, 0.0};
}

void StateVector::check_qubit(std::size_t qubit) const {
    if (qubit >= qubits_) {
        throw std::out_of_range("qubit outside range");
    }
}

std::complex<double> StateVector::amplitude(std::size_t index) const {
    if (index >= state_.size()) {
        throw std::out_of_range("basis index outside range");
    }
    return state_[index];
}

double StateVector::probability(std::size_t index) const {
    return std::norm(amplitude(index));
}

double StateVector::norm_squared() const noexcept {
    double total = 0.0;
    for (const auto& value : state_) {
        total += std::norm(value);
    }
    return total;
}

void StateVector::apply_single(std::size_t qubit, const std::complex<double>& m00, const std::complex<double>& m01, const std::complex<double>& m10, const std::complex<double>& m11) {
    check_qubit(qubit);
    const std::size_t bit = std::size_t{1} << qubit;
    const std::size_t step = bit << 1;
    for (std::size_t base = 0; base < state_.size(); base += step) {
        for (std::size_t offset = 0; offset < bit; ++offset) {
            const std::size_t zero = base + offset;
            const std::size_t one = zero + bit;
            const auto a0 = state_[zero];
            const auto a1 = state_[one];
            state_[zero] = m00 * a0 + m01 * a1;
            state_[one] = m10 * a0 + m11 * a1;
        }
    }
}

void StateVector::apply_x(std::size_t qubit) { apply_single(qubit, {0,0}, {1,0}, {1,0}, {0,0}); }
void StateVector::apply_h(std::size_t qubit) { const double s = 1.0 / std::sqrt(2.0); apply_single(qubit, {s,0}, {s,0}, {s,0}, {-s,0}); }
void StateVector::apply_z(std::size_t qubit) { apply_single(qubit, {1,0}, {0,0}, {0,0}, {-1,0}); }

void StateVector::apply_cnot(std::size_t control, std::size_t target) {
    check_qubit(control); check_qubit(target);
    if (control == target) throw std::invalid_argument("control and target must differ");
    const std::size_t control_bit = std::size_t{1} << control;
    const std::size_t target_bit = std::size_t{1} << target;
    for (std::size_t index = 0; index < state_.size(); ++index) {
        const bool control_on = (index & control_bit) != 0;
        const bool target_off = (index & target_bit) == 0;
        if (control_on && target_off) {
            const std::size_t partner = index | target_bit;
            std::swap(state_[index], state_[partner]);
        }
    }
}
