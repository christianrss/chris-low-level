#include "cache.hpp"
#include <stdexcept>
CacheSim::CacheSim(std::size_t l,std::size_t s,std::size_t w):line_size_(l),sets_(s,std::vector<Line>(w)){
 if(!l||!s||!w) throw std::invalid_argument("zero");
}
bool CacheSim::access(std::uint64_t address){
 // TODO [D6-CACHE-DECODE]: block/set/tag.
 // TODO [D6-CACHE-HIT]: encontre hit e atualize LRU.
 // TODO [D6-CACHE-EVICT]: escolha invalid ou LRU no miss.
 (void)address; return false;
}