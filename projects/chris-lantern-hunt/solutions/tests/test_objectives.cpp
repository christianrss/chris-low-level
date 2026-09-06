#include "../src/objectives.hpp"

#include <cassert>
#include <iostream>

int main() {
    // PEDAGOGY-TEST: LANTERN-OBJ-17 — progressão de objetivos
    lantern::ObjectiveTracker tracker;
    tracker.reset();

    tracker.on_room_entered(1);
    tracker.on_room_entered(2);
    tracker.on_room_entered(3);
    assert(tracker.all()[0].completed);

    tracker.on_food_collected(5);
    tracker.on_bug_killed(4);
    tracker.on_checkpoint_activated();
    tracker.on_escape_ready(true);

    assert(tracker.all_complete());

    std::cout << "test_objectives: PASS\n";
    return 0;
}
