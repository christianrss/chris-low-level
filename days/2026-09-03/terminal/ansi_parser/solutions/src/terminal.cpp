// PEDAGOGY-SOLUTION: TERM-CSI-01
// PEDAGOGY-SOLUTION: TERM-FEED-01

#include "terminal.hpp"
#include <algorithm>
#include <cctype>
#include <stdexcept>

Terminal::Terminal(std::size_t cols, std::size_t rows)
    : cols_(cols), rows_(rows), cells_(cols * rows, ' ') {
    if (cols == 0 || rows == 0) {
        throw std::invalid_argument("terminal dimensions must be non-zero");
    }
}

void Terminal::put(char ch) {
    cells_[row_ * cols_ + col_] = ch;
    if (++col_ >= cols_) {
        col_ = 0;
        if (row_ + 1 < rows_) {
            ++row_;
        }
    }
}

int Terminal::param_or(int fallback) const {
    if (param_text_.empty()) {
        return fallback;
    }
    try {
        return std::stoi(param_text_);
    } catch (...) {
        return fallback;
    }
}

void Terminal::handle_csi(char final_byte) {
    const int n = std::max(1, param_or(1));
    switch (final_byte) {
    case 'A':
        row_ = static_cast<std::size_t>(std::max(0, static_cast<int>(row_) - n));
        break;
    case 'B':
        row_ = std::min(rows_ - 1, row_ + static_cast<std::size_t>(n));
        break;
    case 'C':
        col_ = std::min(cols_ - 1, col_ + static_cast<std::size_t>(n));
        break;
    case 'D':
        col_ = static_cast<std::size_t>(std::max(0, static_cast<int>(col_) - n));
        break;
    case 'J':
        if (param_or(0) == 2) {
            std::fill(cells_.begin(), cells_.end(), ' ');
            row_ = 0;
            col_ = 0;
        }
        break;
    case 'm':
        // SGR is parsed but styles are intentionally deferred to a later milestone.
        break;
    default:
        break;
    }
}

void Terminal::feed(const std::string& bytes) {
    for (unsigned char raw : bytes) {
        const char ch = static_cast<char>(raw);
        switch (state_) {
        case State::Ground:
            if (raw == 0x1B) {
                state_ = State::Escape;
            } else if (ch == '\n') {
                row_ = std::min(rows_ - 1, row_ + 1);
            } else if (ch == '\r') {
                col_ = 0;
            } else if (ch >= 0x20 && ch != 0x7F) {
                put(ch);
            }
            break;
        case State::Escape:
            if (ch == '[') {
                param_text_.clear();
                state_ = State::Csi;
            } else {
                state_ = State::Ground;
            }
            break;
        case State::Csi:
            if (std::isdigit(raw)) {
                param_text_.push_back(ch);
            } else if (ch == ';') {
                // Multiple parameters arrive in later milestones; retain parser synchronization.
            } else if (raw >= 0x40 && raw <= 0x7E) {
                handle_csi(ch);
                state_ = State::Ground;
                param_text_.clear();
            }
            break;
        }
    }
}

char Terminal::at(std::size_t row, std::size_t col) const {
    if (row >= rows_ || col >= cols_) {
        throw std::out_of_range("terminal cell outside range");
    }
    return cells_[row * cols_ + col];
}

std::string Terminal::line(std::size_t row) const {
    if (row >= rows_) {
        throw std::out_of_range("terminal row outside range");
    }
    const auto begin = cells_.begin() + static_cast<std::ptrdiff_t>(row * cols_);
    return std::string(begin, begin + static_cast<std::ptrdiff_t>(cols_));
}
