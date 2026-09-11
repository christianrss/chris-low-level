#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>
struct CacheStats{std::size_t hits{},misses{};};
class CacheSim{
 struct Line{bool valid=false; std::uint64_t tag=0,last_used=0;};
 std::size_t line_size_; std::vector<std::vector<Line>> sets_; std::uint64_t tick_=0; CacheStats stats_;
public:
 CacheSim(std::size_t line_size,std::size_t set_count,std::size_t ways);
 bool access(std::uint64_t address);
 CacheStats stats()const{return stats_;}
};