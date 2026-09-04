#include "tensor.hpp"
#include <chrono>
#include <cstddef>
#include <iostream>

int main() {
    constexpr std::size_t n = 128;
    constexpr int repetitions = 4;
    Tensor2D a(n, n);
    Tensor2D b(n, n);

    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = 0; j < n; ++j) {
            a.at(i, j) = static_cast<float>((i + j) % 17) / 17.0F;
            b.at(i, j) = static_cast<float>((i * 3 + j) % 19) / 19.0F;
        }
    }

    double checksum = 0.0;
    const auto start = std::chrono::steady_clock::now();
    for (int rep = 0; rep < repetitions; ++rep) {
        const Tensor2D c = matmul(a.view(), b.view());
        checksum += c.at(rep, rep);
    }
    const auto end = std::chrono::steady_clock::now();
    const double seconds = std::chrono::duration<double>(end - start).count();
    const double flops = 2.0 * static_cast<double>(n) * n * n * repetitions;

    std::cout << "n=" << n
              << " repetitions=" << repetitions
              << " seconds=" << seconds
              << " gflops=" << flops / seconds / 1.0e9
              << " checksum=" << checksum << "\n";
}
