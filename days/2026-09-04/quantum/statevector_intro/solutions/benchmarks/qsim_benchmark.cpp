#include "qsim.hpp"
#include <chrono>
#include <cstddef>
#include <iostream>

int main() {
    for (std::size_t qubits : {10u, 14u, 18u}) {
        StateVector state(qubits);
        const auto start = std::chrono::steady_clock::now();
        std::size_t gates = 0;
        for (int layer = 0; layer < 8; ++layer) {
            for (std::size_t q = 0; q < qubits; ++q) {
                state.apply_h(q);
                ++gates;
            }
        }
        const auto end = std::chrono::steady_clock::now();
        const double seconds = std::chrono::duration<double>(end - start).count();
        const std::size_t bytes = state.amplitudes() * sizeof(std::complex<double>);
        std::cout << "qubits=" << qubits
                  << " amplitudes=" << state.amplitudes()
                  << " bytes=" << bytes
                  << " gates=" << gates
                  << " seconds=" << seconds
                  << " gates_per_s=" << gates / seconds
                  << " norm=" << state.norm_squared() << "\n";
    }
}
