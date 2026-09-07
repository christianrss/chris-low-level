#include "state_tracker.hpp"
#include <cassert>
#include <iostream>
int main(){Tracker t;
// PEDAGOGY-TEST: D5-GFX-REGISTER
t.register_resource("tex",State::Undefined);bool dup=false;try{t.register_resource("tex",State::Undefined);}catch(...){dup=true;}assert(dup);
// PEDAGOGY-TEST: D5-GFX-TRANSITION
assert(t.transition("tex",State::CopyDst));assert(t.transition("tex",State::ShaderRead));assert(!t.transition("tex",State::ShaderRead));
// PEDAGOGY-TEST: D5-GFX-FLUSH
auto b=t.flush();assert(b.size()==2);assert(t.flush().empty());assert(t.state("tex")==State::ShaderRead);
std::cout<<"chris-gfx-state tests passed\n";}