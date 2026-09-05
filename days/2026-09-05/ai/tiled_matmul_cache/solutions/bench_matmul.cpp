// Benchmark unificado naive vs tiled — PEDAGOGY-TEST [AI-MM-TILED-02]
#include "matmul.hpp"
#include <chrono>
#include <iostream>
#include <vector>

int main() {
    constexpr std::size_t n = 64;
    constexpr std::size_t tile = 8;

    std::vector<float> a(n * n);
    std::vector<float> b(n * n);
    for (std::size_t i = 0; i < a.size(); ++i) {
        a[i] = static_cast<float>(static_cast<int>(i % 13) - 6) / 13.0f;
        b[i] = static_cast<float>(static_cast<int>(i % 11) - 5) / 11.0f;
    }

    for (int warm = 0; warm < 2; ++warm) {
        volatile float sink = matmul_naive(a, b, n, n, n)[0]
            + matmul_tiled(a, b, n, n, n, tile)[0];
        (void)sink;
    }

    double naive_total = 0.0;
    double tiled_total = 0.0;
    constexpr int runs = 5;

    for (int run = 0; run < runs; ++run) {
        const auto t0 = std::chrono::steady_clock::now();
        auto x = matmul_naive(a, b, n, n, n);
        const auto t1 = std::chrono::steady_clock::now();
        auto y = matmul_tiled(a, b, n, n, n, tile);
        const auto t2 = std::chrono::steady_clock::now();

        naive_total += std::chrono::duration<double, std::milli>(t1 - t0).count();
        tiled_total += std::chrono::duration<double, std::milli>(t2 - t1).count();
        volatile float check = x[0] + y[0];
        (void)check;
    }

    std::cout << "unified_bench n=" << n << " tile=" << tile << '\n';
    std::cout << "naive_avg_ms=" << (naive_total / runs) << '\n';
    std::cout << "tiled_avg_ms=" << (tiled_total / runs) << '\n';
    return 0;
}
