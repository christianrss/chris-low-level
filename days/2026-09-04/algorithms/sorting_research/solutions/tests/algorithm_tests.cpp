#include "sort.hpp"
#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

static void check(std::vector<int> input) {
    auto expected = input;
    std::sort(expected.begin(), expected.end());

    auto merge_values = input;
    const auto merge_stats = merge_sort(merge_values);
    assert(merge_values == expected);

    auto quick_values = input;
    const auto quick_stats = quick_sort(quick_values);
    assert(quick_values == expected);

    if (input.size() > 1) {
        assert(merge_stats.comparisons > 0);
        assert(quick_stats.comparisons > 0);
    }
}

int main() {
    check({});
    check({1});
    check({2, 1});
    check({5, 1, 5, -3, 7, 7, 2});
    check({1, 2, 3, 4, 5, 6});
    check({6, 5, 4, 3, 2, 1});
    std::cout << "chris-algorithms tests passed\n";
}
