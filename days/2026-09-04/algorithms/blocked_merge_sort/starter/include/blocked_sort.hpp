#pragma once
#include <cstdint>
#include <vector>

struct SortIoStats {
    std::uint64_t comparisons = 0;
    std::uint64_t block_reads = 0;
    std::uint64_t block_writes = 0;
};

void blocked_merge_sort(std::vector<int>& data, std::size_t tile_size, SortIoStats& stats);
