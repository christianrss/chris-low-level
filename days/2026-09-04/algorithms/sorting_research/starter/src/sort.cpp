#include "sort.hpp"
#include <algorithm>
#include <cstddef>

static void merge_range(std::vector<int>& values, std::vector<int>& scratch,
                        std::size_t begin, std::size_t middle, std::size_t end,
                        SortStats& stats) {
    // TODO [D2-SORT-MERGE-RANGE]: mesclar os intervalos [begin,middle) e [middle,end).
    (void)values; (void)scratch; (void)begin; (void)middle; (void)end; (void)stats;
}

static void merge_sort_impl(std::vector<int>& values, std::vector<int>& scratch,
                            std::size_t begin, std::size_t end, SortStats& stats) {
    // TODO [D2-SORT-MERGE-RECURSE]: dividir recursivamente e chamar merge_range.
    (void)values; (void)scratch; (void)begin; (void)end; (void)stats;
}

SortStats merge_sort(std::vector<int>& values) {
    SortStats stats;
    std::vector<int> scratch(values.size());
    merge_sort_impl(values, scratch, 0, values.size(), stats);
    return stats;
}

static std::size_t partition(std::vector<int>& values, std::size_t begin,
                             std::size_t end, SortStats& stats) {
    // TODO [D2-SORT-PARTITION]: particionar usando o ultimo elemento como pivot.
    (void)values; (void)begin; (void)end; (void)stats;
    return begin;
}

static void quick_sort_impl(std::vector<int>& values, std::size_t begin,
                            std::size_t end, SortStats& stats) {
    // TODO [D2-SORT-QUICK-LOOP]: recursar no lado menor e iterar no maior.
    (void)values; (void)begin; (void)end; (void)stats;
}

SortStats quick_sort(std::vector<int>& values) {
    SortStats stats;
    quick_sort_impl(values, 0, values.size(), stats);
    return stats;
}
