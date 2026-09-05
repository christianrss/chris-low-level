#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>

class PageAllocator {
public:
    explicit PageAllocator(std::size_t page_count);
    int allocate();
    bool free_page(std::size_t page);
    bool is_used(std::size_t page) const;

private:
    void set_used(std::size_t page, bool used);
    std::size_t page_count_;
    std::vector<std::uint8_t> bits_;
};
