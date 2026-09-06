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
    const std::uint64_t tiles =
        static_cast<std::uint64_t>(tiles_covering(begin, end, tile_size));
    if (is_write) {
        stats.block_writes += tiles;
    } else {
        stats.block_reads += tiles;
    }
}

static void sort_tile(
    std::vector<int>& data,
    std::size_t begin,
    std::size_t end,
    SortIoStats& stats) {
    for (std::size_t i = begin + 1; i < end; ++i) {
        const int key = data[i];
        std::size_t j = i;
        while (j > begin) {
            ++stats.comparisons;
            if (data[j - 1] <= key) {
                break;
            }
            data[j] = data[j - 1];
            --j;
        }
        data[j] = key;
    }
}

static void merge_runs(
    const std::vector<int>& src,
    std::size_t begin,
    std::size_t mid,
    std::size_t end,
    std::vector<int>& dst,
    SortIoStats& stats) {
    std::size_t left = begin;
    std::size_t right = mid;
    std::size_t out = begin;
    while (left < mid && right < end) {
        ++stats.comparisons;
        if (src[left] <= src[right]) {
            dst[out++] = src[left++];
        } else {
            dst[out++] = src[right++];
        }
    }
    while (left < mid) {
        dst[out++] = src[left++];
    }
    while (right < end) {
        dst[out++] = src[right++];
    }
}

void blocked_merge_sort(std::vector<int>& data, std::size_t tile_size, SortIoStats& stats) {
    if (tile_size == 0) {
        throw std::invalid_argument("tile_size must be > 0");
    }
    const std::size_t n = data.size();
    if (n <= 1) {
        return;
    }

    for (std::size_t begin = 0; begin < n; begin += tile_size) {
        const std::size_t end = std::min(begin + tile_size, n);
        account_tile_io(stats, begin, end, tile_size, false);
        sort_tile(data, begin, end, stats);
        account_tile_io(stats, begin, end, tile_size, true);
    }

    std::vector<int> scratch(n);
    std::vector<int>* src = &data;
    std::vector<int>* dst = &scratch;
    std::size_t run_len = tile_size;

    while (run_len < n) {
        for (std::size_t begin = 0; begin < n; begin += 2 * run_len) {
            const std::size_t mid = std::min(begin + run_len, n);
            const std::size_t end = std::min(begin + 2 * run_len, n);
            account_tile_io(stats, begin, mid, tile_size, false);
            account_tile_io(stats, mid, end, tile_size, false);
            if (mid >= end) {
                std::copy(src->begin() + static_cast<std::ptrdiff_t>(begin),
                          src->begin() + static_cast<std::ptrdiff_t>(end),
                          dst->begin() + static_cast<std::ptrdiff_t>(begin));
            } else {
                merge_runs(*src, begin, mid, end, *dst, stats);
            }
            account_tile_io(stats, begin, end, tile_size, true);
        }
        std::swap(src, dst);
        run_len *= 2;
    }

    if (src != &data) {
        data.swap(scratch);
    }
}
