// PEDAGOGY-SOLUTION: AI-MM-NAIVE-01
// PEDAGOGY-SOLUTION: AI-MM-TILED-02
#include "matmul.hpp"
#include <algorithm>
#include <stdexcept>

TileTrace trace_tile_4x4(std::size_t row, std::size_t col, std::size_t tile) {
    return {row / tile, col / tile, row, col};
}

static void check_shapes(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n) {
    if (a.size() != m * k || b.size() != k * n) {
        throw std::invalid_argument("shape mismatch");
    }
}

std::vector<float> matmul_naive(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n) {
    check_shapes(a, b, m, k, n);
    std::vector<float> c(m * n, 0.0f);
    for (std::size_t i = 0; i < m; ++i) {
        for (std::size_t j = 0; j < n; ++j) {
            float sum = 0.0f;
            for (std::size_t t = 0; t < k; ++t) {
                sum += a[i * k + t] * b[t * n + j];
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
    check_shapes(a, b, m, k, n);
    if (tile == 0) {
        throw std::invalid_argument("tile must be > 0");
    }

    std::vector<float> c(m * n, 0.0f);
    for (std::size_t ii = 0; ii < m; ii += tile) {
        for (std::size_t kk = 0; kk < k; kk += tile) {
            for (std::size_t jj = 0; jj < n; jj += tile) {
                for (std::size_t i = ii; i < std::min(ii + tile, m); ++i) {
                    for (std::size_t t = kk; t < std::min(kk + tile, k); ++t) {
                        const float a_val = a[i * k + t];
                        for (std::size_t j = jj; j < std::min(jj + tile, n); ++j) {
                            c[i * n + j] += a_val * b[t * n + j];
                        }
                    }
                }
            }
        }
    }
    return c;
}
