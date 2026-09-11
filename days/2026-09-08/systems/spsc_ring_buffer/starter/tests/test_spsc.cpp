#include "spsc.hpp"
#include <cassert>
#include <iostream>
int main(){
 SpscRing q(4); int x=0;
 // PEDAGOGY-TEST: D6-SPSC-PUSH
 assert(q.push(1)&&q.push(2)&&q.push(3)&&q.push(4)); assert(!q.push(5));
 // PEDAGOGY-TEST: D6-SPSC-SIZE
 assert(q.size_approx()==4);
 // PEDAGOGY-TEST: D6-SPSC-POP
 for(int e=1;e<=4;++e){ assert(q.pop(x)); assert(x==e); }
 assert(!q.pop(x)); assert(q.size_approx()==0);
 for(int i=0;i<100;++i){assert(q.push(i));assert(q.pop(x));assert(x==i);}
 std::cout<<"chris-spsc tests passed\n";
}