#include "state_tracker.hpp"
#include <stdexcept>
void Tracker::register_resource(std::string id,State s){ // TODO [D5-GFX-REGISTER]: registre sem duplicar.
 (void)id;(void)s;
}
bool Tracker::transition(const std::string&id,State after){ // TODO [D5-GFX-TRANSITION]: gere barrier e atualize.
 (void)id;(void)after;return false;
}
std::vector<Barrier> Tracker::flush(){ // TODO [D5-GFX-FLUSH]: devolva lote e limpe pending.
 return {};
}
State Tracker::state(const std::string&id)const{auto it=states_.find(id);if(it==states_.end())throw std::out_of_range("resource");return it->second;}
