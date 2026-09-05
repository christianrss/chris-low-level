#include "matmul.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
#include <vector>

int main() {
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

    std::cout << "OK matmul\n";
}
