#pragma once

#include <cstdint>
#include <vector>

namespace lantern {

enum class ObjectiveId {
    ExploreRooms,
    CollectFood,
    KillBugs,
    ActivateCheckpoint,
    Escape,
};

struct Objective {
    ObjectiveId id = ObjectiveId::ExploreRooms;
    const char* description = "";
    int target = 0;
    int progress = 0;
    bool completed = false;
};

class ObjectiveTracker {
public:
    void reset();
    void on_room_entered(int rooms_visited);
    void on_food_collected(int total);
    void on_bug_killed(int total);
    void on_checkpoint_activated();
    void on_escape_ready(bool ready);

    const Objective* active_objective() const;
    bool all_complete() const;
    const std::vector<Objective>& all() const { return objectives_; }

private:
    std::vector<Objective> objectives_;
    void advance_if_needed();
};

} // namespace lantern
