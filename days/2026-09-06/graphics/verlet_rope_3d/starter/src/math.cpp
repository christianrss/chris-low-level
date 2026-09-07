#include "math.hpp"

Mat4 mat4_identity() {
    Mat4 out{};
    out.m[0] = out.m[5] = out.m[10] = out.m[15] = 1.f;
    return out;
}

Mat4 mat4_translate(Vec3 t) {
    Mat4 out = mat4_identity();
    out.m[12] = t.x;
    out.m[13] = t.y;
    out.m[14] = t.z;
    return out;
}

Mat4 mat4_rotate_y(float radians) {
    Mat4 out = mat4_identity();
    float c = std::cos(radians);
    float s = std::sin(radians);
    out.m[0] = c;
    out.m[2] = s;
    out.m[8] = -s;
    out.m[10] = c;
    return out;
}

Mat4 mat4_multiply(const Mat4& a, const Mat4& b) {
    Mat4 out{};
    for (int col = 0; col < 4; ++col) {
        for (int row = 0; row < 4; ++row) {
            float sum = 0.f;
            for (int k = 0; k < 4; ++k) {
                sum += a.m[k * 4 + row] * b.m[col * 4 + k];
            }
            out.m[col * 4 + row] = sum;
        }
    }
    return out;
}

Mat4 mat4_inverse_rigid(const Mat4& m) {
    // TODO [GFX-PORTAL-01]
    (void)m;
    return mat4_identity();
}

Vec3 mat4_transform_point(const Mat4& m, Vec3 p) {
    // TODO [GFX-PORTAL-01]
    (void)m;
    return p;
}

Vec3 mat4_transform_direction(const Mat4& m, Vec3 d) {
    // TODO [GFX-PORTAL-01]
    (void)m;
    return d;
}

Mat4 mat4_perspective(float fov_y_rad, float aspect, float near_z, float far_z) {
    (void)fov_y_rad;
    (void)aspect;
    (void)near_z;
    (void)far_z;
    return mat4_identity();
}

Mat4 mat4_look_at(Vec3 eye, Vec3 target, Vec3 up) {
    (void)eye;
    (void)target;
    (void)up;
    return mat4_identity();
}
