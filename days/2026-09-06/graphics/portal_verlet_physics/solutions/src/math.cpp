// PEDAGOGY-SOLUTION: GFX-PORTAL-01
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
    Vec3 right = {m.m[0], m.m[1], m.m[2]};
    Vec3 up = {m.m[4], m.m[5], m.m[6]};
    Vec3 forward = {m.m[8], m.m[9], m.m[10]};
    Vec3 pos = {m.m[12], m.m[13], m.m[14]};

    Mat4 inv = mat4_identity();
    inv.m[0] = right.x;
    inv.m[1] = up.x;
    inv.m[2] = forward.x;
    inv.m[4] = right.y;
    inv.m[5] = up.y;
    inv.m[6] = forward.y;
    inv.m[8] = right.z;
    inv.m[9] = up.z;
    inv.m[10] = forward.z;
    inv.m[12] = -vec3_dot(right, pos);
    inv.m[13] = -vec3_dot(up, pos);
    inv.m[14] = -vec3_dot(forward, pos);
    return inv;
}

Vec3 mat4_transform_point(const Mat4& m, Vec3 p) {
    float x = m.m[0] * p.x + m.m[4] * p.y + m.m[8] * p.z + m.m[12];
    float y = m.m[1] * p.x + m.m[5] * p.y + m.m[9] * p.z + m.m[13];
    float z = m.m[2] * p.x + m.m[6] * p.y + m.m[10] * p.z + m.m[14];
    return {x, y, z};
}

Vec3 mat4_transform_direction(const Mat4& m, Vec3 d) {
    float x = m.m[0] * d.x + m.m[4] * d.y + m.m[8] * d.z;
    float y = m.m[1] * d.x + m.m[5] * d.y + m.m[9] * d.z;
    float z = m.m[2] * d.x + m.m[6] * d.y + m.m[10] * d.z;
    return {x, y, z};
}

Mat4 mat4_perspective(float fov_y_rad, float aspect, float near_z, float far_z) {
    Mat4 out{};
    const float f = 1.f / std::tan(fov_y_rad * 0.5f);
    out.m[0] = f / aspect;
    out.m[5] = f;
    out.m[10] = (far_z + near_z) / (near_z - far_z);
    out.m[11] = -1.f;
    out.m[14] = (2.f * far_z * near_z) / (near_z - far_z);
    return out;
}

Mat4 mat4_look_at(Vec3 eye, Vec3 target, Vec3 up) {
    Vec3 f = vec3_normalize(vec3_sub(target, eye));
    Vec3 r = vec3_normalize({f.y * up.z - f.z * up.y, f.z * up.x - f.x * up.z, f.x * up.y - f.y * up.x});
    Vec3 u = {r.y * f.z - r.z * f.y, r.z * f.x - r.x * f.z, r.x * f.y - r.y * f.x};

    Mat4 out = mat4_identity();
    out.m[0] = r.x;
    out.m[1] = u.x;
    out.m[2] = -f.x;
    out.m[4] = r.y;
    out.m[5] = u.y;
    out.m[6] = -f.y;
    out.m[8] = r.z;
    out.m[9] = u.z;
    out.m[10] = -f.z;
    out.m[12] = -vec3_dot(r, eye);
    out.m[13] = -vec3_dot(u, eye);
    out.m[14] = vec3_dot(f, eye);
    return out;
}
