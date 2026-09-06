#include "objectives.hpp"

#include <algorithm>

namespace lantern {

void ObjectiveTracker::reset() {
    // PEDAGOGY-SOLUTION: LANTERN-OBJ-17
    objectives_ = {
        {ObjectiveId::ExploreRooms, "Explore 3 salas distintas", 3, 0, false},
        {ObjectiveId::CollectFood, "Colete 5 comidas", 5, 0, false},
        {ObjectiveId::KillBugs, "Elimine 4 insetos", 4, 0, false},
        {ObjectiveId::ActivateCheckpoint, "Ative um altar (tecla E)", 1, 0, false},
        {ObjectiveId::Escape, "Complete todos os objetivos", 1, 0, false},
    };
}

void ObjectiveTracker::advance_if_needed() {
    for (Objective& objective : objectives_) {
        if (!objective.completed && objective.progress >= objective.target) {
            objective.completed = true;
        }
    }
}

void ObjectiveTracker::on_room_entered(int rooms_visited) {
    if (!objectives_.empty()) {
        objectives_[0].progress = std::min(rooms_visited, objectives_[0].target);
    }
    advance_if_needed();
}

void ObjectiveTracker::on_food_collected(int total) {
    if (objectives_.size() > 1) {
        objectives_[1].progress = std::min(total, objectives_[1].target);
    }
    advance_if_needed();
}

void ObjectiveTracker::on_bug_killed(int total) {
    if (objectives_.size() > 2) {
        objectives_[2].progress = std::min(total, objectives_[2].target);
    }
    advance_if_needed();
}

void ObjectiveTracker::on_checkpoint_activated() {
    if (objectives_.size() > 3) {
        objectives_[3].progress = 1;
    }
    advance_if_needed();
}

void ObjectiveTracker::on_escape_ready(bool ready) {
    if (objectives_.size() > 4) {
        objectives_[4].progress = ready ? 1 : 0;
    }
    advance_if_needed();
}

const Objective* ObjectiveTracker::active_objective() const {
    for (const Objective& objective : objectives_) {
        if (!objective.completed) {
            return &objective;
        }
    }
    return nullptr;
}

bool ObjectiveTracker::all_complete() const {
    for (const Objective& objective : objectives_) {
        if (!objective.completed) {
            return false;
        }
    }
    return !objectives_.empty();
}

} // namespace lantern
