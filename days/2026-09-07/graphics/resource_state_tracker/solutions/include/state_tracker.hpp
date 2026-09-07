#pragma once
#include <string>
#include <unordered_map>
#include <vector>
enum class State{Undefined,CopyDst,ShaderRead,RenderTarget,Present};
struct Barrier{std::string id;State before,after;};
class Tracker{public:void register_resource(std::string id,State s);bool transition(const std::string&id,State after);std::vector<Barrier> flush();State state(const std::string&id)const;private:std::unordered_map<std::string,State> states_;std::vector<Barrier> pending_;};