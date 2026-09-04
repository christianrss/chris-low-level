#include "terminal.hpp"
#include <stdexcept>

Terminal::Terminal(std::size_t cols, std::size_t rows)
    : cols_(cols), rows_(rows), cells_(cols * rows, ' ') {
    if (cols == 0 || rows == 0) throw std::invalid_argument("terminal dimensions must be non-zero");
}

void Terminal::put(char ch) {
    cells_[row_ * cols_ + col_] = ch;
    if (++col_ >= cols_) { col_ = 0; if (row_ + 1 < rows_) ++row_; }
}

int Terminal::param_or(int fallback) const { return fallback; }
void Terminal::handle_csi(char) { /* TODO */ }

void Terminal::feed(const std::string& bytes) {
    for (char ch : bytes) {
        if (ch == '\r') col_ = 0;
        else if (ch == '\n') row_ = (row_ + 1 < rows_) ? row_ + 1 : row_;
        else if (static_cast<unsigned char>(ch) >= 0x20) put(ch);
        // TODO: add ESC -> CSI incremental state machine.
    }
}

char Terminal::at(std::size_t row, std::size_t col) const {
    if (row >= rows_ || col >= cols_) throw std::out_of_range("terminal cell outside range");
    return cells_[row * cols_ + col];
}

std::string Terminal::line(std::size_t row) const {
    if (row >= rows_) throw std::out_of_range("terminal row outside range");
    auto begin = cells_.begin() + static_cast<std::ptrdiff_t>(row * cols_);
    return std::string(begin, begin + static_cast<std::ptrdiff_t>(cols_));
}
