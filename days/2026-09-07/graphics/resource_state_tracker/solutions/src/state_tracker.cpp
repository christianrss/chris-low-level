#include "state_tracker.hpp"
#include <stdexcept>
void Tracker::register_resource(std::string id,State s){ // PEDAGOGY-SOLUTION: D5-GFX-REGISTER
 if(states_.contains(id))throw std::invalid_argument("duplicate resource");states_.emplace(std::move(id),s);
}
bool Tracker::transition(const std::string&id,State after){ // PEDAGOGY-SOLUTION: D5-GFX-TRANSITION
 auto it=states_.find(id);if(it==states_.end())throw std::out_of_range("resource");if(it->second==after)return false;
 pending_.push_back({id,it->second,after});it->second=after;return true;
}
std::vector<Barrier> Tracker::flush(){ // PEDAGOGY-SOLUTION: D5-GFX-FLUSH
 auto out=pending_;pending_.clear();return out;
}
State Tracker::state(const std::string&id)const{auto it=states_.find(id);if(it==states_.end())throw std::out_of_range("resource");return it->second;}
