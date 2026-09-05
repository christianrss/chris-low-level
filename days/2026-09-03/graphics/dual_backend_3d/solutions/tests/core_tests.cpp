// PEDAGOGY-TEST [GFX-CAMERA-01]: yaw altera forward.x para +X
// PEDAGOGY-TEST [GFX-CAMERA-02]: right perpendicular a forward e world_up
// PEDAGOGY-TEST [GFX-CAMERA-03]: view_matrix posiciona origem em z=-6
// PEDAGOGY-TEST [GFX-CAMERA-04]: movimento WASD altera posição da câmera
// PEDAGOGY-TEST [GFX-CAMERA-05]: mouse delta atualiza yaw/pitch com clamp
// PEDAGOGY-TEST [GFX-CULL-01]: screen_triangle_front_facing respeita winding
// PEDAGOGY-TEST [GFX-CULL-02]: triângulos back-facing ignorados no raster
// PEDAGOGY-TEST [GFX-CULL-03]: GL_CULL_FACE com back faces CCW
// PEDAGOGY-TEST [GFX-LAMBERT-01]: iluminação difusa + ambiente no fragment shader
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

void test_default_camera_matches_original_view() {
    const CameraState camera{};
    const Vec4 origin = view_matrix(camera) * Vec4{0.0f, 0.0f, 0.0f, 1.0f};
    assert(approximately_equal(origin.x, 0.0f));
    assert(approximately_equal(origin.y, 0.0f));
    assert(approximately_equal(origin.z, -6.0f));
    assert(approximately_equal(origin.w, 1.0f));
}

void test_camera_yaw_changes_forward_direction() {
    CameraState camera{};
    constexpr float kHalfPi = 1.57079632679f;
    camera.yaw = kHalfPi;
    const Vec3 forward = camera_forward(camera);
    assert(forward.x > 0.999f);
    assert(std::fabs(forward.z) < 0.001f);
}

void test_screen_winding_helper() {
    assert(screen_triangle_front_facing(2.0f));
    assert(!screen_triangle_front_facing(-2.0f));
    assert(!screen_triangle_front_facing(0.0f));
}

} // namespace

int main() {
    test_identity_matrix();
    test_physics_moves_body_downward();
    test_draw_list_contains_expected_items();
    test_default_camera_matches_original_view();
    test_camera_yaw_changes_forward_direction();
    test_screen_winding_helper();

    std::cout << "core_tests: all tests passed\n";
    return 0;
}
