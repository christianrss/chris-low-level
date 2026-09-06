#include "objectives.hpp"

namespace lantern {

void ObjectiveTracker::reset() {
    // TODO [LANTERN-OBJ-17]: inicializar lista ordenada de objetivos.
    objectives_.clear();
}

void ObjectiveTracker::advance_if_needed() {}

void ObjectiveTracker::on_room_entered(int /*rooms_visited*/) {}

void ObjectiveTracker::on_food_collected(int /*total*/) {}

void ObjectiveTracker::on_bug_killed(int /*total*/) {}

void ObjectiveTracker::on_checkpoint_activated() {}

void ObjectiveTracker::on_escape_ready(bool /*ready*/) {}

const Objective* ObjectiveTracker::active_objective() const {
    return nullptr;
}

bool ObjectiveTracker::all_complete() const {
    return false;
}

} // namespace lantern
