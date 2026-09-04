#include "sort.hpp"
#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <string>
#include <vector>

static void run_case(const std::string& name, const std::vector<int>& input) {
    auto merge_values = input;
    const auto merge_start = std::chrono::steady_clock::now();
    const auto merge_stats = merge_sort(merge_values);
    const auto merge_end = std::chrono::steady_clock::now();

    auto quick_values = input;
    const auto quick_start = std::chrono::steady_clock::now();
    const auto quick_stats = quick_sort(quick_values);
    const auto quick_end = std::chrono::steady_clock::now();

    const auto merge_us = std::chrono::duration_cast<std::chrono::microseconds>(
        merge_end - merge_start).count();
    const auto quick_us = std::chrono::duration_cast<std::chrono::microseconds>(
        quick_end - quick_start).count();

    std::cout << name
              << " n=" << input.size()
              << " merge_us=" << merge_us
              << " merge_cmp=" << merge_stats.comparisons
              << " quick_us=" << quick_us
              << " quick_cmp=" << quick_stats.comparisons << "\n";
}

int main() {
    constexpr int n = 12000;
    std::mt19937 rng(20260904U);
    std::uniform_int_distribution<int> wide(0, 1000000);
    std::uniform_int_distribution<int> narrow(0, 15);

    std::vector<int> random_values(n);
    std::generate(random_values.begin(), random_values.end(), [&] { return wide(rng); });
    run_case("random", random_values);

    auto sorted = random_values;
    std::sort(sorted.begin(), sorted.end());
    run_case("sorted", sorted);

    auto reversed = sorted;
    std::reverse(reversed.begin(), reversed.end());
    run_case("reversed", reversed);

    std::vector<int> duplicates(n);
    std::generate(duplicates.begin(), duplicates.end(), [&] { return narrow(rng); });
    run_case("duplicates", duplicates);
}
