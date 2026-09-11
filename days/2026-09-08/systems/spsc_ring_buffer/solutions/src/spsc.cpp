#include "spsc.hpp"
#include <stdexcept>
SpscRing::SpscRing(std::size_t capacity): storage_(capacity+1) {
 if(capacity==0) throw std::invalid_argument("capacity");
}
bool SpscRing::push(int value){
 // PEDAGOGY-SOLUTION: D6-SPSC-PUSH
 auto head=head_.load(std::memory_order_relaxed);
 auto next=(head+1)%storage_.size();
 if(next==tail_.load(std::memory_order_acquire)) return false;
 storage_[head]=value;
 head_.store(next,std::memory_order_release);
 return true;
}
bool SpscRing::pop(int& out){
 // PEDAGOGY-SOLUTION: D6-SPSC-POP
 auto tail=tail_.load(std::memory_order_relaxed);
 if(tail==head_.load(std::memory_order_acquire)) return false;
 out=storage_[tail];
 tail_.store((tail+1)%storage_.size(),std::memory_order_release);
 return true;
}
std::size_t SpscRing::size_approx() const{
 // PEDAGOGY-SOLUTION: D6-SPSC-SIZE
 auto h=head_.load(std::memory_order_acquire), t=tail_.load(std::memory_order_acquire);
 return h>=t ? h-t : storage_.size()-t+h;
}