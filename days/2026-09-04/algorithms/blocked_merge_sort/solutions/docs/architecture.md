# Architecture

`blocked_merge_sort` sorts `tile_size` windows in place, then repeatedly merges adjacent runs through a scratch buffer. `SortIoStats` counts comparisons and tile-granularity reads/writes so the I/O model stays visible without a real filesystem.
