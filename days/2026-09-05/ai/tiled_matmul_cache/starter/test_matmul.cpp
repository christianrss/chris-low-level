// PEDAGOGY-TEST: AI-MM-NAIVE-01: multiplicação 2x3·3x2 correta
// PEDAGOGY-TEST: AI-MM-TILED-02: equivalência tiled vs naive e trace 4x4
// PEDAGOGY-TEST: AI-MM-TILED-02: matriz 64x64 com tile 8
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `test_matmul` valida naive 2×3·3×2 e equivalência tiled.
// Caso 2: **Trace 4×4:** `trace_tile_4x4(5,7,4)` → tile (1,1).
// Caso 3: **64×64:** matrizes 64×64 com tile=8 devem coincidir (tolerância 1e-3).
// Caso 4: **Benchmark unificado:** `bench_matmul` imprime `naive_avg_ms` e `tiled_avg_ms` 
// Caso 5: Valide solutions/ após implementar ambos os TODOs.
#include "matmul.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
#include <vector>

static std::vector<float> make_matrix(std::size_t rows, std::size_t cols, int seed) {
    std::vector<float> out(rows * cols);
    for (std::size_t i = 0; i < out.size(); ++i) {
        out[i] = static_cast<float>((static_cast<int>(i) + seed) % 11 - 5);
    }
    return out;
}

int main() {
    const auto trace = trace_tile_4x4(5, 7, 4);
    assert(trace.tile_row == 1);
    assert(trace.tile_col == 1);
    assert(trace.global_row == 5);
    assert(trace.global_col == 7);

    std::vector<float> a = {1, 2, 3, 4, 5, 6};
    std::vector<float> b = {7, 8, 9, 10, 11, 12};
    auto c = matmul_naive(a, b, 2, 3, 2);
    assert(c.size() == 4);
    assert(std::fabs(c[0] - 58.0f) < 1e-5f);
    assert(std::fabs(c[3] - 154.0f) < 1e-5f);

    std::vector<float> a2(15);
    std::vector<float> b2(20);
    for (std::size_t i = 0; i < a2.size(); ++i) {
        a2[i] = static_cast<float>(static_cast<int>(i % 7) - 3);
    }
    for (std::size_t i = 0; i < b2.size(); ++i) {
        b2[i] = static_cast<float>(static_cast<int>(i % 5) - 2);
    }

    auto naive = matmul_naive(a2, b2, 3, 5, 4);
    auto tiled = matmul_tiled(a2, b2, 3, 5, 4, 2);
    assert(naive.size() == tiled.size());
    for (std::size_t i = 0; i < naive.size(); ++i) {
        assert(std::fabs(naive[i] - tiled[i]) < 1e-5f);
    }

    const std::size_t dim = 64;
    auto big_a = make_matrix(dim, dim, 3);
    auto big_b = make_matrix(dim, dim, 7);
    auto big_naive = matmul_naive(big_a, big_b, dim, dim, dim);
    auto big_tiled = matmul_tiled(big_a, big_b, dim, dim, dim, 8);
    for (std::size_t i = 0; i < big_naive.size(); ++i) {
        assert(std::fabs(big_naive[i] - big_tiled[i]) < 1e-3f);
    }

    std::cout << "OK matmul\n";
    return 0;
}