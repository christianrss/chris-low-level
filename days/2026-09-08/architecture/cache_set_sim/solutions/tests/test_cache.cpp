#include "cache.hpp"
#include <cassert>
#include <iostream>
int main(){
 CacheSim direct(64,2,1), two(64,2,2);
 // PEDAGOGY-TEST: D6-CACHE-DECODE
 assert(!direct.access(0)); assert(!direct.access(128));
 // PEDAGOGY-TEST: D6-CACHE-HIT
 assert(!direct.access(0)); auto ds=direct.stats(); assert(ds.hits==0&&ds.misses==3);
 // PEDAGOGY-TEST: D6-CACHE-EVICT
 assert(!two.access(0));assert(!two.access(128));assert(two.access(0)); auto ts=two.stats();assert(ts.hits==1);
 std::cout<<"chris-cache-sim tests passed\n";
}