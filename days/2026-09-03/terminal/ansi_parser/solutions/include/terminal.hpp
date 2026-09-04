#pragma once
#include <cstddef>
#include <string>
#include <vector>

class Terminal {
public:
    Terminal(std::size_t cols = 80, std::size_t rows = 24);
    void feed(const std::string& bytes);
    char at(std::size_t row, std::size_t col) const;
    std::size_t cursor_row() const { return row_; }
    std::size_t cursor_col() const { return col_; }
    std::string line(std::size_t row) const;

private:
    enum class State { Ground, Escape, Csi };
    void put(char ch);
    void handle_csi(char final_byte);
    int param_or(int fallback) const;

    std::size_t cols_;
    std::size_t rows_;
    std::vector<char> cells_;
    std::size_t row_ = 0;
    std::size_t col_ = 0;
    State state_ = State::Ground;
    std::string param_text_;
};
