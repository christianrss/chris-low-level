#pragma once
#include <string>
enum class State{CopyDst,ShaderRead,RenderTarget,Present};
class Tracker{State s_;public:explicit Tracker(State s):s_(s){}State state()const{return s_;}bool transition(State);static std::string vk(State);static std::string d3d12(State);};
