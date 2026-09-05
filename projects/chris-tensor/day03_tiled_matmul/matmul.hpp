#pragma once
#include <cstddef>
#include <vector>

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
