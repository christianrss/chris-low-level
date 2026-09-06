#include "blocked_sort.hpp"
#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <string>
#include <vector>

static void run_case(
    const std::string& name,
    const std::vector<int>& input,
    std::size_t tile_size) {
    auto values = input;
    SortIoStats stats;
    const auto start = std::chrono::steady_clock::now();
    blocked_merge_sort(values, tile_size, stats);
    const auto end = std::chrono::steady_clock::now();
    const auto us = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

    auto expected = input;
    std::sort(expected.begin(), expected.end());
    const bool ok = values == expected;

    std::cout << name
              << " n=" << input.size()
              << " tile=" << tile_size
              << " us=" << us
              << " cmp=" << stats.comparisons
              << " bread=" << stats.block_reads
              << " bwrite=" << stats.block_writes
              << " ok=" << (ok ? 1 : 0) << "\n";
}

int main() {
    constexpr int n = 65536;
    std::mt19937 rng(20260904U);
    std::uniform_int_distribution<int> wide(0, 1000000);

    std::vector<int> random_values(n);
    std::generate(random_values.begin(), random_values.end(), [&] { return wide(rng); });

    for (std::size_t tile : {64U, 256U, 1024U, 4096U}) {
        run_case("random", random_values, tile);
    }

    auto sorted = random_values;
    std::sort(sorted.begin(), sorted.end());
    run_case("sorted", sorted, 256);

    auto reversed = sorted;
    std::reverse(reversed.begin(), reversed.end());
    run_case("reversed", reversed, 256);
}
