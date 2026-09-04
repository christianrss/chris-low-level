// PEDAGOGY-SOLUTION: GFX-CAMERA-03
// PEDAGOGY-SOLUTION: GFX-CAMERA-01
// PEDAGOGY-SOLUTION: GFX-CAMERA-02
// PEDAGOGY-SOLUTION: GFX-CULL-01

#include "engine.hpp"

namespace lab3d {

Mat4 Mat4::identity() {
    Mat4 result{};
    result.m[0] = 1.0f;
    result.m[5] = 1.0f;
    result.m[10] = 1.0f;
    result.m[15] = 1.0f;
    return result;
}

Mat4 operator*(const Mat4& a, const Mat4& b) {
    Mat4 result{};

    for (int column = 0; column < 4; ++column) {
        for (int row = 0; row < 4; ++row) {
            float sum = 0.0f;

            for (int k = 0; k < 4; ++k) {
                sum += a.m[k * 4 + row] * b.m[column * 4 + k];
            }

            result.m[column * 4 + row] = sum;
        }
    }

    return result;
}

Vec4 operator*(const Mat4& matrix, const Vec4& vector) {
    return {
        matrix.m[0] * vector.x +
            matrix.m[4] * vector.y +
            matrix.m[8] * vector.z +
            matrix.m[12] * vector.w,

        matrix.m[1] * vector.x +
            matrix.m[5] * vector.y +
            matrix.m[9] * vector.z +
            matrix.m[13] * vector.w,

        matrix.m[2] * vector.x +
            matrix.m[6] * vector.y +
            matrix.m[10] * vector.z +
            matrix.m[14] * vector.w,

        matrix.m[3] * vector.x +
            matrix.m[7] * vector.y +
            matrix.m[11] * vector.z +
            matrix.m[15] * vector.w,
    };
}

Mat4 translate(float x, float y, float z) {
    Mat4 result = Mat4::identity();
    result.m[12] = x;
    result.m[13] = y;
    result.m[14] = z;
    return result;
}

Mat4 scale(float x, float y, float z) {
    Mat4 result{};
    result.m[0] = x;
    result.m[5] = y;
    result.m[10] = z;
    result.m[15] = 1.0f;
    return result;
}

Mat4 rotate_z(float radians) {
    Mat4 result = Mat4::identity();
    const float cosine = std::cos(radians);
    const float sine = std::sin(radians);

    result.m[0] = cosine;
    result.m[4] = -sine;
    result.m[1] = sine;
    result.m[5] = cosine;

    return result;
}

Mat4 rotate_y(float radians) {
    Mat4 result = Mat4::identity();
    const float cosine = std::cos(radians);
    const float sine = std::sin(radians);

    result.m[0] = cosine;
    result.m[8] = sine;
    result.m[2] = -sine;
    result.m[10] = cosine;

    return result;
}

Mat4 perspective(float fov, float aspect, float z_near, float z_far) {
    Mat4 result{};
    const float f = 1.0f / std::tan(fov * 0.5f);

    result.m[0] = f / aspect;
    result.m[5] = f;
    result.m[10] = (z_far + z_near) / (z_near - z_far);
    result.m[11] = -1.0f;
    result.m[14] = (2.0f * z_far * z_near) / (z_near - z_far);

    return result;
}


Mat4 look_at(Vec3 eye, Vec3 target, Vec3 world_up) {
    const Vec3 forward = normalize(target - eye);
    const Vec3 right = normalize(cross(forward, world_up));
    const Vec3 up = cross(right, forward);

    Mat4 result = Mat4::identity();
    result.m[0] = right.x;
    result.m[4] = right.y;
    result.m[8] = right.z;
    result.m[12] = -dot(right, eye);

    result.m[1] = up.x;
    result.m[5] = up.y;
    result.m[9] = up.z;
    result.m[13] = -dot(up, eye);

    result.m[2] = -forward.x;
    result.m[6] = -forward.y;
    result.m[10] = -forward.z;
    result.m[14] = dot(forward, eye);
    return result;
}

Vec3 camera_forward(const CameraState& camera) {
    const float cos_pitch = std::cos(camera.pitch);
    return normalize({
        cos_pitch * std::sin(camera.yaw),
        std::sin(camera.pitch),
        -cos_pitch * std::cos(camera.yaw),
    });
}

Vec3 camera_right(const CameraState& camera) {
    constexpr Vec3 kWorldUp{0.0f, 1.0f, 0.0f};
    return normalize(cross(camera_forward(camera), kWorldUp));
}

Mat4 view_matrix(const CameraState& camera) {
    constexpr Vec3 kWorldUp{0.0f, 1.0f, 0.0f};
    const Vec3 forward = camera_forward(camera);
    return look_at(camera.position, camera.position + forward, kWorldUp);
}

bool screen_triangle_front_facing(float signed_area) {
    return signed_area > 0.0f;
}

void reset_scene(SceneState& scene) {
    scene = SceneState{};
}

void physics_step(SceneState& scene, float delta_time) {
    if (scene.paused) {
        return;
    }

    scene.time += delta_time;

    constexpr float kGravity = -9.81f;
    constexpr float kFloorY = -1.25f;
    constexpr float kRestitution = 0.72f;

    // Semi-implicit Euler: update velocity first, then position.
    scene.body.velocity.y += kGravity * delta_time;
    scene.body.position =
        scene.body.position + scene.body.velocity * delta_time;

    if (scene.body.position.y - scene.body.half_extent < kFloorY) {
        scene.body.position.y = kFloorY + scene.body.half_extent;

        if (scene.body.velocity.y < 0.0f) {
            scene.body.velocity.y =
                -scene.body.velocity.y * kRestitution;
        }

        // Tiny tangential damping so the body slowly loses horizontal energy.
        scene.body.velocity.x *= 0.995f;
    }

    if (scene.body.position.x > 2.2f || scene.body.position.x < 0.4f) {
        scene.body.velocity.x = -scene.body.velocity.x;
    }
}

std::vector<DrawItem> build_draw_list(const SceneState& scene) {
    std::vector<DrawItem> draw_items;
    draw_items.reserve(5);

    // Floor.
    draw_items.push_back({
        translate(0.0f, -1.35f, 0.0f) * scale(3.2f, 0.10f, 2.2f),
        {0.30f, 0.34f, 0.40f},
    });

    // Two-bone hierarchical arm. The child transform inherits the parent.
    const float shoulder_angle = std::sin(scene.time * 1.25f) * 0.75f;
    const float elbow_angle = std::sin(scene.time * 1.85f + 0.65f) * 0.90f;

    const Mat4 shoulder =
        translate(-1.15f, -0.95f, 0.0f) *
        rotate_z(shoulder_angle);

    const Mat4 upper_arm =
        shoulder *
        translate(0.0f, 0.62f, 0.0f) *
        scale(0.24f, 0.62f, 0.24f);

    draw_items.push_back({upper_arm, {0.20f, 0.65f, 0.95f}});

    const Mat4 elbow =
        shoulder *
        translate(0.0f, 1.24f, 0.0f) *
        rotate_z(elbow_angle);

    const Mat4 forearm =
        elbow *
        translate(0.0f, 0.52f, 0.0f) *
        scale(0.20f, 0.52f, 0.20f);

    draw_items.push_back({forearm, {0.95f, 0.55f, 0.22f}});

    const Mat4 hand =
        elbow *
        translate(0.0f, 1.08f, 0.0f) *
        scale(0.30f, 0.16f, 0.30f);

    draw_items.push_back({hand, {0.92f, 0.80f, 0.20f}});

    // Physics body.
    const Mat4 body =
        translate(
            scene.body.position.x,
            scene.body.position.y,
            scene.body.position.z) *
        rotate_y(scene.time * 0.8f) *
        scale(
            scene.body.half_extent,
            scene.body.half_extent,
            scene.body.half_extent);

    draw_items.push_back({body, {0.55f, 0.95f, 0.48f}});

    return draw_items;
}

Mat4 view_matrix() {
    return view_matrix(CameraState{});
}

Mat4 projection_matrix(float aspect) {
    constexpr float kPi = 3.1415926535f;
    return perspective(60.0f * kPi / 180.0f, aspect, 0.1f, 100.0f);
}

} // namespace lab3d
