#pragma once

#include <cmath>

struct Vec3 {
    float x = 0.f;
    float y = 0.f;
    float z = 0.f;
};

inline Vec3 vec3_add(Vec3 a, Vec3 b) { return {a.x + b.x, a.y + b.y, a.z + b.z}; }
inline Vec3 vec3_sub(Vec3 a, Vec3 b) { return {a.x - b.x, a.y - b.y, a.z - b.z}; }
inline Vec3 vec3_scale(Vec3 v, float s) { return {v.x * s, v.y * s, v.z * s}; }
inline float vec3_dot(Vec3 a, Vec3 b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
inline float vec3_length(Vec3 v) { return std::sqrt(vec3_dot(v, v)); }
inline Vec3 vec3_normalize(Vec3 v) {
    float len = vec3_length(v);
    if (len < 1e-6f) return {0.f, 0.f, 0.f};
    return vec3_scale(v, 1.f / len);
}

// Column-major 4x4 (OpenGL convention).
struct Mat4 {
    float m[16] = {};
};

Mat4 mat4_identity();
Mat4 mat4_translate(Vec3 t);
Mat4 mat4_rotate_y(float radians);
Mat4 mat4_multiply(const Mat4& a, const Mat4& b);
Mat4 mat4_inverse_rigid(const Mat4& m);
Vec3 mat4_transform_point(const Mat4& m, Vec3 p);
Vec3 mat4_transform_direction(const Mat4& m, Vec3 d);
Mat4 mat4_perspective(float fov_y_rad, float aspect, float near_z, float far_z);
Mat4 mat4_look_at(Vec3 eye, Vec3 target, Vec3 up);
