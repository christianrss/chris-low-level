#pragma once
#include <cstdint>
#include <vector>

struct SortStats {
    std::uint64_t comparisons = 0;
    std::uint64_t moves = 0;
};

SortStats merge_sort(std::vector<int>& values);
SortStats quick_sort(std::vector<int>& values);
