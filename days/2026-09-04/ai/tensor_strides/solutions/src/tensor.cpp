#include "tensor.hpp"
#include <stdexcept>
#include <utility>

// PEDAGOGY-SOLUTION: D2-TENSOR-VIEW-AT
float TensorView2D::at(std::size_t row, std::size_t col) const {
    if (row >= rows || col >= cols || data == nullptr) {
        throw std::out_of_range("tensor view index outside range");
    }
    return data[row * row_stride + col * col_stride];
}

Tensor2D::Tensor2D(std::size_t rows, std::size_t cols)
    : rows_(rows), cols_(cols), data_(rows * cols, 0.0F) {
    if (rows == 0 || cols == 0) {
        throw std::invalid_argument("tensor dimensions must be non-zero");
    }
}

Tensor2D::Tensor2D(std::size_t rows, std::size_t cols, std::vector<float> values)
    : rows_(rows), cols_(cols), data_(std::move(values)) {
    if (rows == 0 || cols == 0 || data_.size() != rows * cols) {
        throw std::invalid_argument("tensor shape does not match data");
    }
}

std::size_t Tensor2D::checked_index(std::size_t row, std::size_t col) const {
    if (row >= rows_ || col >= cols_) {
        throw std::out_of_range("tensor index outside range");
    }
    return row * cols_ + col;
}

float& Tensor2D::at(std::size_t row, std::size_t col) {
    return data_[checked_index(row, col)];
}

float Tensor2D::at(std::size_t row, std::size_t col) const {
    return data_[checked_index(row, col)];
}

TensorView2D Tensor2D::view() const noexcept {
    return {data_.data(), rows_, cols_, cols_, 1};
}

// PEDAGOGY-SOLUTION: D2-TENSOR-TRANSPOSE
TensorView2D Tensor2D::transpose_view() const noexcept {
    return {data_.data(), cols_, rows_, 1, cols_};
}

// PEDAGOGY-SOLUTION: D2-TENSOR-MATMUL
Tensor2D matmul(const TensorView2D& left, const TensorView2D& right) {
    if (left.cols != right.rows) {
        throw std::invalid_argument("matmul inner dimensions do not match");
    }

    Tensor2D out(left.rows, right.cols);
    for (std::size_t i = 0; i < left.rows; ++i) {
        for (std::size_t k = 0; k < left.cols; ++k) {
            const float a = left.at(i, k);
            for (std::size_t j = 0; j < right.cols; ++j) {
                out.at(i, j) += a * right.at(k, j);
            }
        }
    }
    return out;
}
