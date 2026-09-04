#include "terminal.hpp"
#include <cassert>
#include <iostream>

int main() {
    Terminal term(10, 4);
    term.feed("abc");
    assert(term.at(0, 0) == 'a');
    assert(term.at(0, 2) == 'c');
    assert(term.cursor_col() == 3);

    term.feed("\x1b[2D!");
    assert(term.at(0, 1) == '!');

    term.feed("\r\nX");
    assert(term.at(1, 0) == 'X');

    term.feed("\x1b[2J");
    assert(term.at(0, 0) == ' ');
    assert(term.cursor_row() == 0);
    assert(term.cursor_col() == 0);

    Terminal fragmented(8, 2);
    fragmented.feed("A\x1b");
    fragmented.feed("[2C");
    fragmented.feed("B");
    assert(fragmented.at(0, 0) == 'A');
    assert(fragmented.at(0, 3) == 'B');

    std::cout << "terminal tests passed\n";
}
