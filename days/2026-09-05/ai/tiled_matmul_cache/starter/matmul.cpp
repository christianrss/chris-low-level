#include "matmul.hpp"

std::vector<float> matmul_naive(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n) {
    // TODO [AI-MM-NAIVE-01]
    (void)a;
    (void)b;
    (void)k;
    return std::vector<float>(m * n);
}

std::vector<float> matmul_tiled(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n,
    std::size_t tile) {
    // TODO [AI-MM-TILED-02]
    (void)a;
    (void)b;
    (void)k;
    (void)tile;
    return std::vector<float>(m * n);
}
