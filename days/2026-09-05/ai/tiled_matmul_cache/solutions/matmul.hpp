#pragma once
#include <cstddef>
#include <string>
#include <vector>

struct TileTrace {
    std::size_t tile_row;
    std::size_t tile_col;
    std::size_t global_row;
    std::size_t global_col;
};

TileTrace trace_tile_4x4(std::size_t row, std::size_t col, std::size_t tile = 4);

std::vector<float> matmul_naive(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n);

std::vector<float> matmul_tiled(
    const std::vector<float>& a,
    const std::vector<float>& b,
    std::size_t m,
    std::size_t k,
    std::size_t n,
    std::size_t tile);
