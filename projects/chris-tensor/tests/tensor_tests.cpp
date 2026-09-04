#include "tensor.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

static bool near(float a, float b) {
    return std::fabs(a - b) < 1.0e-5F;
}

int main() {
    Tensor2D matrix(2, 3, {1, 2, 3, 4, 5, 6});
    const auto transposed = matrix.transpose_view();
    assert(transposed.rows == 3);
    assert(transposed.cols == 2);
    assert(near(transposed.at(2, 1), 6.0F));

    Tensor2D left(2, 3, {1, 2, 3, 4, 5, 6});
    Tensor2D right(3, 2, {7, 8, 9, 10, 11, 12});
    const Tensor2D result = matmul(left.view(), right.view());
    assert(near(result.at(0, 0), 58.0F));
    assert(near(result.at(0, 1), 64.0F));
    assert(near(result.at(1, 0), 139.0F));
    assert(near(result.at(1, 1), 154.0F));

    bool mismatch = false;
    try {
        Tensor2D bad(4, 4);
        (void)matmul(left.view(), bad.view());
    } catch (const std::invalid_argument&) {
        mismatch = true;
    }
    assert(mismatch);

    std::cout << "chris-tensor tests passed\n";
}
