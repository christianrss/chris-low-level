#include "cache.hpp"
#include <stdexcept>
CacheSim::CacheSim(std::size_t l,std::size_t s,std::size_t w):line_size_(l),sets_(s,std::vector<Line>(w)){
 if(!l||!s||!w) throw std::invalid_argument("zero");
}
bool CacheSim::access(std::uint64_t address){
 // PEDAGOGY-SOLUTION: D6-CACHE-DECODE
 auto block=address/line_size_; auto si=block%sets_.size(); auto tag=block/sets_.size(); auto& set=sets_[si];
 // PEDAGOGY-SOLUTION: D6-CACHE-HIT
 for(auto& line:set) if(line.valid&&line.tag==tag){++stats_.hits;line.last_used=++tick_;return true;}
 ++stats_.misses;
 // PEDAGOGY-SOLUTION: D6-CACHE-EVICT
 Line* victim=nullptr;
 for(auto& line:set) if(!line.valid){victim=&line;break;}
 if(!victim){victim=&set[0];for(auto& line:set) if(line.last_used<victim->last_used) victim=&line;}
 victim->valid=true;victim->tag=tag;victim->last_used=++tick_;return false;
}