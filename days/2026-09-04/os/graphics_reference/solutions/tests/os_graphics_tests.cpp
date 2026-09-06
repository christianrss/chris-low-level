// PEDAGOGY-TEST: D2-GFX-INDEX
// PEDAGOGY-TEST: D2-GFX-FILL-RECT
// PEDAGOGY-TEST: D2-GFX-ALPHA-OVER
// PEDAGOGY-TEST: D2-GFX-COMPOSE
// PEDAGOGY-TEST: D2-GFX-DIRTY-RECT
// PEDAGOGY-TEST: D2-GFX-FRAME-PACE
#include "graphics.hpp"
#include <cassert>
#include <iostream>
#include <vector>

static void test_compose_and_fill() {
    const Pixel black{0, 0, 0, 255};
    const Pixel red{255, 0, 0, 255};
    const Pixel blue_half{0, 0, 255, 128};

    Surface base(4, 4, red);
    Surface top(2, 2, blue_half);
    const Surface output = Compositor::compose(
        4,
        4,
        black,
        std::vector<Layer>{{&base, 0, 0}, {&top, 1, 1}});

    assert(output.pixel(0, 0) == red);
    const Pixel mixed = output.pixel(1, 1);
    assert(mixed.r >= 126 && mixed.r <= 128);
    assert(mixed.g == 0);
    assert(mixed.b >= 127 && mixed.b <= 129);

    Surface clipped(3, 3, black);
    clipped.fill_rect(-1, -1, 3, 3, red);
    assert(clipped.pixel(0, 0) == red);
    assert(clipped.pixel(2, 2) == black);
}

static void test_dirty_rect() {
    const Pixel black{0, 0, 0, 255};
    const Pixel red{255, 0, 0, 255};
    const Pixel blue{0, 0, 255, 255};

    Surface s(8, 8, black);
    assert(!s.has_dirty());
    s.fill_rect(2, 2, 3, 3, red);
    Rect d = s.take_dirty_union();
    assert(d.x == 2 && d.y == 2 && d.width == 3 && d.height == 3);
    assert(d.area() == 9);
    assert(!s.has_dirty());
    assert(s.take_dirty_union().empty());

    s.fill_rect(0, 0, 2, 2, red);
    s.fill_rect(5, 5, 2, 2, blue);
    d = s.take_dirty_union();
    assert(d.x == 0 && d.y == 0 && d.width == 7 && d.height == 7);
    assert(d.area() == 49);

    s.fill_rect(-2, -2, 4, 4, red);
    d = s.take_dirty_union();
    assert(d.x == 0 && d.y == 0 && d.width == 2 && d.height == 2);

    DirtyTracker tracker;
    tracker.mark_dirty(1, 1, 2, 2);
    tracker.mark_dirty(4, 0, 1, 1);
    d = tracker.take_dirty_union();
    assert(d.x == 1 && d.y == 0 && d.width == 4 && d.height == 3);
    assert(tracker.empty());

    Surface layer(2, 2, red);
    const Surface composed = Compositor::compose(
        6,
        6,
        black,
        std::vector<Layer>{{&layer, 2, 1}});
    d = composed.dirty_union();
    assert(d.x == 2 && d.y == 1 && d.width == 2 && d.height == 2);
}

static void test_frame_pace() {
    const Pixel black{0, 0, 0, 255};
    const Pixel red{255, 0, 0, 255};
    const Pixel gray{10, 10, 10, 255};

    Surface layer(2, 2, red);
    const std::vector<Layer> layers{{&layer, 3, 3}};

    const Surface full = Compositor::compose(8, 8, black, layers);
    Surface paced(8, 8, black);
    FrameStats stats = FramePacer::compose_with_damage(
        paced, black, layers, Rect{0, 0, 8, 8});
    assert(stats.dirty_area == 64);
    assert(stats.pixels_touched == 64);
    for (std::size_t y = 0; y < 8; ++y) {
        for (std::size_t x = 0; x < 8; ++x) {
            assert(paced.pixel(x, y) == full.pixel(x, y));
        }
    }

    Surface partial(8, 8, gray);
    stats = FramePacer::compose_with_damage(
        partial, black, layers, Rect{3, 3, 2, 2});
    assert(stats.dirty_area == 4);
    assert(stats.pixels_touched == 4);
    assert(partial.pixel(3, 3) == red);
    assert(partial.pixel(4, 4) == red);
    assert(partial.pixel(0, 0) == gray);
    assert(partial.pixel(7, 7) == gray);

    DirtyTracker damage;
    damage.mark_dirty(3, 3, 2, 2);
    Surface from_tracker(8, 8, gray);
    stats = FramePacer::compose_with_damage(from_tracker, black, layers, damage);
    assert(stats.pixels_touched == 4);
    assert(damage.empty());
    assert(from_tracker.pixel(3, 3) == red);
    assert(from_tracker.pixel(0, 0) == gray);
}

int main() {
    test_compose_and_fill();
    test_dirty_rect();
    test_frame_pace();
    std::cout << "chris-os graphics reference tests passed\n";
}
