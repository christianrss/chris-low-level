#pragma once
#include <cstddef>
#include <vector>

struct TensorView2D {
    const float* data = nullptr;
    std::size_t rows = 0;
    std::size_t cols = 0;
    std::size_t row_stride = 0;
    std::size_t col_stride = 0;

    float at(std::size_t row, std::size_t col) const;
};

class Tensor2D {
public:
    Tensor2D(std::size_t rows, std::size_t cols);
    Tensor2D(std::size_t rows, std::size_t cols, std::vector<float> values);

    float& at(std::size_t row, std::size_t col);
    float at(std::size_t row, std::size_t col) const;
    std::size_t rows() const noexcept { return rows_; }
    std::size_t cols() const noexcept { return cols_; }

    TensorView2D view() const noexcept;
    TensorView2D transpose_view() const noexcept;

private:
    std::size_t checked_index(std::size_t row, std::size_t col) const;
    std::size_t rows_ = 0;
    std::size_t cols_ = 0;
    std::vector<float> data_;
};

Tensor2D matmul(const TensorView2D& left, const TensorView2D& right);
