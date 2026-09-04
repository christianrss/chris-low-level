#include <cassert>
#include <cmath>
#include <iostream>

#include "engine.hpp"

using namespace lab3d;

namespace {

bool approximately_equal(float a, float b, float epsilon = 1.0e-4f) {
    return std::fabs(a - b) <= epsilon;
}

void test_identity_matrix() {
    const Mat4 identity = Mat4::identity();
    const Vec4 input{1.0f, 2.0f, 3.0f, 1.0f};
    const Vec4 output = identity * input;

    assert(approximately_equal(output.x, input.x));
    assert(approximately_equal(output.y, input.y));
    assert(approximately_equal(output.z, input.z));
    assert(approximately_equal(output.w, input.w));
}

void test_physics_moves_body_downward() {
    SceneState scene{};
    reset_scene(scene);

    const float initial_y = scene.body.position.y;
    physics_step(scene, 1.0f / 120.0f);

    assert(scene.body.position.y < initial_y);
}

void test_draw_list_contains_expected_items() {
    SceneState scene{};
    reset_scene(scene);

    const auto draw_list = build_draw_list(scene);
    assert(draw_list.size() == 5);
}

} // namespace

int main() {
    test_identity_matrix();
    test_physics_moves_body_downward();
    test_draw_list_contains_expected_items();

    std::cout << "core_tests: all tests passed\n";
    return 0;
}
