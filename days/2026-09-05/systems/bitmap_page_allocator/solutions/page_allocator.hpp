#pragma once
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

struct PageBitTrace {
    std::size_t page;
    std::size_t byte_index;
    std::size_t bit_index;
};

PageBitTrace trace_page_to_bit(std::size_t page);

class PageAllocator {
public:
    explicit PageAllocator(std::size_t page_count);
    int allocate();
    bool free_page(std::size_t page);
    bool is_used(std::size_t page) const;
    std::size_t page_count() const { return page_count_; }

private:
    void set_used(std::size_t page, bool used);
    std::size_t page_count_;
    std::vector<std::uint8_t> bits_;
};
