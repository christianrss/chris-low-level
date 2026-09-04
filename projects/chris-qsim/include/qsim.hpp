#pragma once
#include <complex>
#include <cstddef>
#include <vector>

class StateVector {
public:
    explicit StateVector(std::size_t qubits);

    std::size_t qubits() const noexcept { return qubits_; }
    std::size_t amplitudes() const noexcept { return state_.size(); }
    std::complex<double> amplitude(std::size_t index) const;
    double probability(std::size_t index) const;
    double norm_squared() const noexcept;

    void apply_x(std::size_t qubit);
    void apply_h(std::size_t qubit);
    void apply_z(std::size_t qubit);
    void apply_cnot(std::size_t control, std::size_t target);

private:
    void check_qubit(std::size_t qubit) const;
    void apply_single(
        std::size_t qubit,
        const std::complex<double>& m00,
        const std::complex<double>& m01,
        const std::complex<double>& m10,
        const std::complex<double>& m11);

    std::size_t qubits_ = 0;
    std::vector<std::complex<double>> state_;
};
