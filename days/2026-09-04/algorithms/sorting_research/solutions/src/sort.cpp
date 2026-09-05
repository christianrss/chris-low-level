#include "sort.hpp"
#include <algorithm>
#include <cstddef>

// PEDAGOGY-SOLUTION: D2-SORT-MERGE-RANGE
static void merge_range(
    std::vector<int>& values,
    std::vector<int>& scratch,
    std::size_t begin,
    std::size_t middle,
    std::size_t end,
    SortStats& stats) {
    std::size_t left = begin;
    std::size_t right = middle;
    std::size_t out = begin;

    while (left < middle && right < end) {
        ++stats.comparisons;
        if (values[left] <= values[right]) {
            scratch[out++] = values[left++];
        } else {
            scratch[out++] = values[right++];
        }
        ++stats.moves;
    }
    while (left < middle) {
        scratch[out++] = values[left++];
        ++stats.moves;
    }
    while (right < end) {
        scratch[out++] = values[right++];
        ++stats.moves;
    }
    for (std::size_t i = begin; i < end; ++i) {
        values[i] = scratch[i];
        ++stats.moves;
    }
}

// PEDAGOGY-SOLUTION: D2-SORT-MERGE-RECURSE
static void merge_sort_impl(
    std::vector<int>& values,
    std::vector<int>& scratch,
    std::size_t begin,
    std::size_t end,
    SortStats& stats) {
    if (end - begin <= 1) {
        return;
    }
    const std::size_t middle = begin + (end - begin) / 2;
    merge_sort_impl(values, scratch, begin, middle, stats);
    merge_sort_impl(values, scratch, middle, end, stats);
    merge_range(values, scratch, begin, middle, end, stats);
}

SortStats merge_sort(std::vector<int>& values) {
    SortStats stats;
    std::vector<int> scratch(values.size());
    merge_sort_impl(values, scratch, 0, values.size(), stats);
    return stats;
}

// PEDAGOGY-SOLUTION: D2-SORT-PARTITION
static std::size_t partition(
    std::vector<int>& values,
    std::size_t begin,
    std::size_t end,
    SortStats& stats) {
    const int pivot = values[end - 1];
    std::size_t store = begin;
    for (std::size_t i = begin; i + 1 < end; ++i) {
        ++stats.comparisons;
        if (values[i] < pivot) {
            if (i != store) {
                std::swap(values[i], values[store]);
                stats.moves += 3;
            }
            ++store;
        }
    }
    if (store != end - 1) {
        std::swap(values[store], values[end - 1]);
        stats.moves += 3;
    }
    return store;
}

// PEDAGOGY-SOLUTION: D2-SORT-QUICK-LOOP
static void quick_sort_impl(
    std::vector<int>& values,
    std::size_t begin,
    std::size_t end,
    SortStats& stats) {
    while (end - begin > 1) {
        const std::size_t pivot = partition(values, begin, end, stats);
        const std::size_t left_size = pivot - begin;
        const std::size_t right_size = end - (pivot + 1);

        if (left_size < right_size) {
            quick_sort_impl(values, begin, pivot, stats);
            begin = pivot + 1;
        } else {
            quick_sort_impl(values, pivot + 1, end, stats);
            end = pivot;
        }
    }
}

SortStats quick_sort(std::vector<int>& values) {
    SortStats stats;
    quick_sort_impl(values, 0, values.size(), stats);
    return stats;
}
