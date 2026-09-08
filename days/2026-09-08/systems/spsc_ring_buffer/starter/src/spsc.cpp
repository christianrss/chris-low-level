#include "spsc.hpp"
#include <stdexcept>
SpscRing::SpscRing(std::size_t capacity): storage_(capacity+1) {
 if(capacity==0) throw std::invalid_argument("capacity");
}
bool SpscRing::push(int value){
 // TODO [D6-SPSC-PUSH]: publique item com acquire/release.
 (void)value; return false;
}
bool SpscRing::pop(int& out){
 // TODO [D6-SPSC-POP]: consuma item mantendo ordem FIFO.
 (void)out; return false;
}
std::size_t SpscRing::size_approx() const{
 // TODO [D6-SPSC-SIZE]: compute distância circular.
 return 0;
}