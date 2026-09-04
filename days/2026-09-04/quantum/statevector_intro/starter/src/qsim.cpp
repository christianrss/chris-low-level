#include "qsim.hpp"
#include <cmath>
#include <stdexcept>
#include <utility>

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

void StateVector::apply_single(std::size_t qubit,
    const std::complex<double>& m00, const std::complex<double>& m01,
    const std::complex<double>& m10, const std::complex<double>& m11) {
    // TODO ETAPA 1
    (void)qubit; (void)m00; (void)m01; (void)m10; (void)m11;
}
void StateVector::apply_x(std::size_t qubit) { /* TODO ETAPA 2 */ (void)qubit; }
void StateVector::apply_h(std::size_t qubit) { /* TODO ETAPA 3 */ (void)qubit; }
void StateVector::apply_z(std::size_t qubit) { /* TODO ETAPA 4 */ (void)qubit; }
void StateVector::apply_cnot(std::size_t control, std::size_t target) { /* TODO ETAPA 5 */ (void)control; (void)target; }
