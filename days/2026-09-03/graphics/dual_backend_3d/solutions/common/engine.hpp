#pragma once

#include <array>
#include <cmath>
#include <vector>

namespace lab3d {

struct Vec3 {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;

    Vec3 operator+(const Vec3& other) const {
        return {x + other.x, y + other.y, z + other.z};
    }

    Vec3 operator-(const Vec3& other) const {
        return {x - other.x, y - other.y, z - other.z};
    }

    Vec3 operator*(float scalar) const {
        return {x * scalar, y * scalar, z * scalar};
    }
};

inline float dot(Vec3 a, Vec3 b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

inline Vec3 cross(Vec3 a, Vec3 b) {
    return {
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x,
    };
}

inline Vec3 normalize(Vec3 value) {
    const float length = std::sqrt(dot(value, value));
    if (length <= 1.0e-8f) {
        return {};
    }

    return value * (1.0f / length);
}

struct Vec4 {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    float w = 0.0f;
};

struct Mat4 {
    // Column-major layout. This lets the same matrix data be sent directly to
    // OpenGL with transpose = GL_FALSE.
    std::array<float, 16> m{};

    static Mat4 identity();
};

Mat4 operator*(const Mat4& a, const Mat4& b);
Vec4 operator*(const Mat4& matrix, const Vec4& vector);

Mat4 translate(float x, float y, float z);
Mat4 scale(float x, float y, float z);
Mat4 rotate_z(float radians);
Mat4 rotate_y(float radians);
Mat4 perspective(float fov_y_radians, float aspect, float z_near, float z_far);
Mat4 look_at(Vec3 eye, Vec3 target, Vec3 world_up);

struct CameraState {
    Vec3 position{0.0f, 0.0f, 6.0f};
    float yaw = 0.0f;
    float pitch = 0.0f;
};

Vec3 camera_forward(const CameraState& camera);
Vec3 camera_right(const CameraState& camera);
Mat4 view_matrix(const CameraState& camera);

// Because the software viewport flips Y, front-facing CCW triangles in NDC
// arrive with a positive signed area using this lab's edge() convention.
bool screen_triangle_front_facing(float signed_area);

struct Body {
    Vec3 position{1.25f, 1.5f, 0.0f};
    Vec3 velocity{0.35f, 0.0f, 0.0f};
    float half_extent = 0.35f;
};

struct SceneState {
    float time = 0.0f;
    Body body{};
    bool paused = false;
};

struct DrawItem {
    Mat4 model;
    Vec3 color;
};

void reset_scene(SceneState& scene);
void physics_step(SceneState& scene, float delta_time);
std::vector<DrawItem> build_draw_list(const SceneState& scene);
Mat4 view_matrix();
Mat4 projection_matrix(float aspect);

} // namespace lab3d
