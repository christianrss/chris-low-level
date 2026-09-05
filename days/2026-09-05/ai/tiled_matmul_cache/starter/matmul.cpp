#include "matmul.hpp"

TileTrace trace_tile_4x4(std::size_t row, std::size_t col, std::size_t tile) {
    // TODO [AI-MM-TILED-02]: mapear (row,col) global para tile_row/tile_col
    return {0, 0, row, col};
}

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
