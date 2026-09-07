#pragma once
#include <complex>
#include <cstddef>
#include <vector>

class StateVector2 {
public:
    StateVector2();
    double probability(std::size_t index) const;
    void apply_h(std::size_t qubit);
    double measure_probability(std::size_t index) const;
    void collapse_to(std::size_t index);
    static std::size_t born_select(const std::vector<double>& probs, double u);

private:
    std::vector<std::complex<double>> state_;
};
