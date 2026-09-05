#include "page_allocator.hpp"
PageAllocator::PageAllocator(std::size_t n):page_count_(n),bits_((n+7)/8,0){}
bool PageAllocator::is_used(std::size_t p)const{return p>=page_count_?true:(bits_[p/8]&(1u<<(p%8)))!=0;}
void PageAllocator::set_used(std::size_t p,bool u){auto m=static_cast<std::uint8_t>(1u<<(p%8)); if(u)bits_[p/8]|=m;else bits_[p/8]&=static_cast<std::uint8_t>(~m);}
int PageAllocator::allocate(){/* TODO [SYS-PAGE-ALLOC-01] */return -1;}
bool PageAllocator::free_page(std::size_t p){/* TODO [SYS-PAGE-FREE-02] */return false;}
