#include "state_tracker.hpp"
#include <chrono>
#include <iostream>
int main(){using C=std::chrono::steady_clock;Tracker t;t.register_resource("x",State::Undefined);auto s=C::now();for(int i=0;i<1000000;i++){t.transition("x",(i&1)?State::CopyDst:State::ShaderRead);if((i%1024)==0)t.flush();}t.flush();auto e=C::now();std::cout<<"1m_transitions_ms="<<std::chrono::duration<double,std::milli>(e-s).count()<<"\n";}