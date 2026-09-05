#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>
class PageAllocator{std::size_t page_count_;std::vector<std::uint8_t> bits_;bool is_used(std::size_t)const;void set_used(std::size_t,bool);public:explicit PageAllocator(std::size_t);int allocate();bool free_page(std::size_t);};
