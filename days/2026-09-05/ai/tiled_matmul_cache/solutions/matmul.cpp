// SOLVES [AI-MM-NAIVE-01]
// SOLVES [AI-MM-TILED-02]
#include "matmul.hpp"
#include <algorithm>

std::vector<float> matmul_naive(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n) {
    std::vector<float> c(m * n, 0.0f);
    for (std::size_t i = 0; i < m; ++i) {
        for (std::size_t j = 0; j < n; ++j) {
            float sum = 0.0f;
            for (std::size_t kk = 0; kk < k; ++kk) {
                sum += a[i * k + kk] * b[kk * n + j];
            }
            c[i * n + j] = sum;
        }
    }
    return c;
}

std::vector<float> matmul_tiled(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n,
    std::size_t tile) {
    std::vector<float> c(m * n, 0.0f);
    for (std::size_t ii = 0; ii < m; ii += tile) {
        for (std::size_t kk = 0; kk < k; kk += tile) {
            for (std::size_t jj = 0; jj < n; jj += tile) {
                const auto i_end = std::min(ii + tile, m);
                const auto k_end = std::min(kk + tile, k);
                const auto j_end = std::min(jj + tile, n);
                for (std::size_t i = ii; i < i_end; ++i) {
                    for (std::size_t x = kk; x < k_end; ++x) {
                        for (std::size_t j = jj; j < j_end; ++j) {
                            c[i * n + j] +=
                                a[i * k + x] * b[x * n + j];
                        }
                    }
                }
            }
        }
    }
    return c;
}
