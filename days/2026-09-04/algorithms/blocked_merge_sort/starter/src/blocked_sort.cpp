#include "blocked_sort.hpp"
#include <algorithm>
#include <cstddef>
#include <stdexcept>
#include <utility>

static std::size_t tiles_covering(std::size_t begin, std::size_t end, std::size_t tile_size) {
    if (begin >= end || tile_size == 0) {
        return 0;
    }
    return (end - begin + tile_size - 1) / tile_size;
}

static void account_tile_io(
    SortIoStats& stats,
    std::size_t begin,
    std::size_t end,
    std::size_t tile_size,
    bool is_write) {
    // TODO [D2-BLOCK-IO-STATS]: somar block_reads ou block_writes em unidades de tile.
    (void)stats;
    (void)begin;
    (void)end;
    (void)tile_size;
    (void)is_write;
    (void)tiles_covering;
}

static void sort_tile(
    std::vector<int>& data,
    std::size_t begin,
    std::size_t end,
    SortIoStats& stats) {
    // TODO [D2-BLOCK-SORT-TILE]: ordenar [begin,end) in-place e contar comparisons.
    (void)data;
    (void)begin;
    (void)end;
    (void)stats;
}

static void merge_runs(
    const std::vector<int>& src,
    std::size_t begin,
    std::size_t mid,
    std::size_t end,
    std::vector<int>& dst,
    SortIoStats& stats) {
    // TODO [D2-BLOCK-MERGE-RUN]: mesclar [begin,mid) e [mid,end) em dst[begin,end).
    (void)src;
    (void)begin;
    (void)mid;
    (void)end;
    (void)dst;
    (void)stats;
}

void blocked_merge_sort(std::vector<int>& data, std::size_t tile_size, SortIoStats& stats) {
    // TODO [D2-BLOCK-PASSES]: ordenar tiles e mesclar pares adjacentes ate um unico run.
    (void)data;
    (void)tile_size;
    (void)stats;
    (void)account_tile_io;
    (void)sort_tile;
    (void)merge_runs;
    throw std::logic_error("TODO blocked_merge_sort");
}
