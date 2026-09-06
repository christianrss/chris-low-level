// PEDAGOGY-TEST: D2-BLOCK-MERGE-RUN
// PEDAGOGY-TEST: D2-BLOCK-SORT-TILE
// PEDAGOGY-TEST: D2-BLOCK-PASSES
// PEDAGOGY-TEST: D2-BLOCK-IO-STATS
#include "blocked_sort.hpp"
#include <algorithm>
#include <cassert>
#include <iostream>
#include <stdexcept>
#include <vector>

static void expect_sorted(std::vector<int> input, std::size_t tile_size) {
    auto expected = input;
    std::sort(expected.begin(), expected.end());
    SortIoStats stats;
    blocked_merge_sort(input, tile_size, stats);
    assert(input == expected);
    if (expected.size() > 1) {
        assert(stats.comparisons > 0);
        assert(stats.block_reads > 0);
        assert(stats.block_writes > 0);
    }
}

int main() {
    // Caso 1: vazios e singleton — sem I/O nem comparações.
    {
        std::vector<int> empty;
        SortIoStats stats;
        blocked_merge_sort(empty, 4, stats);
        assert(empty.empty());
        assert(stats.comparisons == 0);
        assert(stats.block_reads == 0);
        assert(stats.block_writes == 0);

        std::vector<int> one{42};
        blocked_merge_sort(one, 4, stats);
        assert(one == std::vector<int>({42}));
        assert(stats.comparisons == 0);
        assert(stats.block_reads == 0);
        assert(stats.block_writes == 0);
    }

    // Caso 2: um único tile — só sort local, sem pass de merge.
    {
        std::vector<int> data{3, 1, 2};
        SortIoStats stats;
        blocked_merge_sort(data, 8, stats);
        assert(data == (std::vector<int>{1, 2, 3}));
        assert(stats.block_reads == 1);
        assert(stats.block_writes == 1);
        assert(stats.comparisons > 0);
    }

    // Caso 3: vários tiles — sort + merge de runs adjacentes.
    {
        expect_sorted({5, 1, 5, -3, 7, 7, 2}, 3);
        expect_sorted({6, 5, 4, 3, 2, 1}, 2);
        expect_sorted({1, 2, 3, 4, 5, 6}, 4);
        expect_sorted({9, 8, 7, 6, 5, 4, 3, 2, 1, 0}, 4);
    }

    // Caso 4: I/O em unidades de tile (n=8, tile=4 → 2+2 na fase sort, 2+2 no merge).
    {
        std::vector<int> data{8, 7, 6, 5, 4, 3, 2, 1};
        SortIoStats stats;
        blocked_merge_sort(data, 4, stats);
        assert(data == (std::vector<int>{1, 2, 3, 4, 5, 6, 7, 8}));
        assert(stats.block_reads == 4);
        assert(stats.block_writes == 4);
        assert(stats.comparisons > 0);
    }

    bool bad_tile = false;
    try {
        std::vector<int> data{1, 2};
        SortIoStats stats;
        blocked_merge_sort(data, 0, stats);
    } catch (const std::invalid_argument&) {
        bad_tile = true;
    }
    assert(bad_tile);

    std::cout << "chris-algorithms tests passed\n";
}
