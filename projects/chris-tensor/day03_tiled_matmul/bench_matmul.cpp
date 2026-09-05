#include "matmul.hpp"
#include <chrono>
#include <iostream>
#include <vector>

int main() {
    constexpr std::size_t n = 128;
    std::vector<float> a(n * n);
    std::vector<float> b(n * n);
    for (std::size_t i = 0; i < a.size(); ++i) {
        a[i] = static_cast<float>(static_cast<int>(i % 13) - 6) / 13.0f;
        b[i] = static_cast<float>(static_cast<int>(i % 11) - 5) / 11.0f;
    }

    for (int warm = 0; warm < 2; ++warm) {
        auto x = matmul_naive(a, b, n, n, n);
        auto y = matmul_tiled(a, b, n, n, n, 16);
        volatile float sink = x[0] + y[0];
        (void)sink;
    }

    for (int run = 0; run < 9; ++run) {
        const auto t0 = std::chrono::steady_clock::now();
        auto x = matmul_naive(a, b, n, n, n);
        const auto t1 = std::chrono::steady_clock::now();
        auto y = matmul_tiled(a, b, n, n, n, 16);
        const auto t2 = std::chrono::steady_clock::now();
        const auto naive_ms =
            std::chrono::duration<double, std::milli>(t1 - t0).count();
        const auto tiled_ms =
            std::chrono::duration<double, std::milli>(t2 - t1).count();
        std::cout << naive_ms << ' ' << tiled_ms << '\n';
    }
}
