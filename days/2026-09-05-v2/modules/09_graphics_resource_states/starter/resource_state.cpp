// TODO [GFX-STATE-01]: implement resource state transitions
#include "resource_state.hpp"

bool Tracker::transition(State n) {
  // TODO [GFX-STATE-01]
  (void)n;
  return false;
}

std::string Tracker::vk(State) {
  // TODO [GFX-STATE-01]
  return "";
}

std::string Tracker::d3d12(State) {
  // TODO [GFX-STATE-01]
  return "";
}
