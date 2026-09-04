#include "tensor.hpp"
#include <stdexcept>
#include <utility>

float TensorView2D::at(std::size_t row, std::size_t col) const {
    // TODO ETAPA 1: validar limites e calcular row*row_stride + col*col_stride.
    (void)row; (void)col;
    throw std::logic_error("TODO TensorView2D::at");
}

Tensor2D::Tensor2D(std::size_t rows, std::size_t cols)
    : rows_(rows), cols_(cols), data_(rows * cols, 0.0F) {
    if (rows == 0 || cols == 0) throw std::invalid_argument("tensor dimensions must be non-zero");
}

Tensor2D::Tensor2D(std::size_t rows, std::size_t cols, std::vector<float> values)
    : rows_(rows), cols_(cols), data_(std::move(values)) {
    if (rows == 0 || cols == 0 || data_.size() != rows * cols) throw std::invalid_argument("tensor shape does not match data");
}

std::size_t Tensor2D::checked_index(std::size_t row, std::size_t col) const {
    if (row >= rows_ || col >= cols_) throw std::out_of_range("tensor index outside range");
    return row * cols_ + col;
}

float& Tensor2D::at(std::size_t row, std::size_t col) { return data_[checked_index(row, col)]; }
float Tensor2D::at(std::size_t row, std::size_t col) const { return data_[checked_index(row, col)]; }

TensorView2D Tensor2D::view() const noexcept {
    // TODO ETAPA 2
    return {};
}

TensorView2D Tensor2D::transpose_view() const noexcept {
    // TODO ETAPA 3
    return {};
}

Tensor2D matmul(const TensorView2D& left, const TensorView2D& right) {
    // TODO ETAPA 4
    (void)left; (void)right;
    throw std::logic_error("TODO matmul");
}
