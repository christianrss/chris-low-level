#include "graphics.hpp"
#include <cassert>
#include <iostream>
#include <vector>

int main() {
    const Pixel black{0, 0, 0, 255};
    const Pixel red{255, 0, 0, 255};
    const Pixel blue_half{0, 0, 255, 128};
    Surface base(4, 4, red);
    Surface top(2, 2, blue_half);
    const Surface output = Compositor::compose(4, 4, black, std::vector<Layer>{{&base, 0, 0}, {&top, 1, 1}});
    assert(output.pixel(0, 0) == red);
    const Pixel mixed = output.pixel(1, 1);
    assert(mixed.r >= 126 && mixed.r <= 128);
    assert(mixed.g == 0);
    assert(mixed.b >= 127 && mixed.b <= 129);
    Surface clipped(3, 3, black);
    clipped.fill_rect(-1, -1, 3, 3, red);
    assert(clipped.pixel(0, 0) == red);
    assert(clipped.pixel(2, 2) == black);
    std::cout << "chris-os graphics reference tests passed\n";
}
