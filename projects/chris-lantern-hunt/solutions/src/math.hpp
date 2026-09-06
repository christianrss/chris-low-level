#pragma once

#include <cmath>
#include <cstring>

namespace lantern {

struct Vec3 {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;

    Vec3() = default;
    Vec3(float px, float py, float pz) : x(px), y(py), z(pz) {}

    Vec3 operator+(const Vec3& other) const {
        return {x + other.x, y + other.y, z + other.z};
    }

    Vec3 operator-(const Vec3& other) const {
        return {x - other.x, y - other.y, z - other.z};
    }

    Vec3& operator-=(const Vec3& other) {
        x -= other.x;
        y -= other.y;
        z -= other.z;
        return *this;
    }

    Vec3 operator*(float scalar) const { return {x * scalar, y * scalar, z * scalar}; }

    Vec3& operator+=(const Vec3& other) {
        x += other.x;
        y += other.y;
        z += other.z;
        return *this;
    }

    float dot(const Vec3& other) const { return x * other.x + y * other.y + z * other.z; }

    Vec3 cross(const Vec3& other) const {
        return {
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x,
        };
    }

    float length() const { return std::sqrt(dot(*this)); }

    Vec3 normalized() const {
        const float len = length();
        if (len < 1e-6f) {
            return {0.0f, 1.0f, 0.0f};
        }
        return *this * (1.0f / len);
    }
};

struct Mat4 {
    float m[16]{};

    static Mat4 identity() {
        Mat4 result{};
        result.m[0] = 1.0f;
        result.m[5] = 1.0f;
        result.m[10] = 1.0f;
        result.m[15] = 1.0f;
        return result;
    }
};

inline Mat4 operator*(const Mat4& a, const Mat4& b) {
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

inline Mat4 translate(float x, float y, float z) {
    Mat4 result = Mat4::identity();
    result.m[12] = x;
    result.m[13] = y;
    result.m[14] = z;
    return result;
}

inline Mat4 scale(float x, float y, float z) {
    Mat4 result{};
    result.m[0] = x;
    result.m[5] = y;
    result.m[10] = z;
    result.m[15] = 1.0f;
    return result;
}

inline Mat4 rotate_y(float radians) {
    Mat4 result = Mat4::identity();
    const float cosine = std::cos(radians);
    const float sine = std::sin(radians);
    result.m[0] = cosine;
    result.m[8] = sine;
    result.m[2] = -sine;
    result.m[10] = cosine;
    return result;
}

inline Mat4 perspective(float fov_y, float aspect, float z_near, float z_far) {
    Mat4 result{};
    const float f = 1.0f / std::tan(fov_y * 0.5f);
    result.m[0] = f / aspect;
    result.m[5] = f;
    result.m[10] = (z_far + z_near) / (z_near - z_far);
    result.m[11] = -1.0f;
    result.m[14] = (2.0f * z_far * z_near) / (z_near - z_far);
    return result;
}

inline Mat4 look_at(const Vec3& eye, const Vec3& center, const Vec3& up) {
    const Vec3 f = (center - eye).normalized();
    const Vec3 s = f.cross(up).normalized();
    const Vec3 u = s.cross(f);

    Mat4 result = Mat4::identity();
    result.m[0] = s.x;
    result.m[4] = s.y;
    result.m[8] = s.z;
    result.m[1] = u.x;
    result.m[5] = u.y;
    result.m[9] = u.z;
    result.m[2] = -f.x;
    result.m[6] = -f.y;
    result.m[10] = -f.z;
    result.m[12] = -s.dot(eye);
    result.m[13] = -u.dot(eye);
    result.m[14] = f.dot(eye);
    return result;
}

struct FpsCamera {
    Vec3 position{0.0f, 1.6f, 0.0f};
    float yaw = 0.0f;
    float pitch = 0.0f;

    Vec3 forward() const {
        const float cos_pitch = std::cos(pitch);
        Vec3 result{
            std::sin(yaw) * cos_pitch,
            std::sin(pitch),
            std::cos(yaw) * cos_pitch,
        };
        return result.normalized();
    }

    Vec3 right() const {
        const Vec3 world_up{0.0f, 1.0f, 0.0f};
        return forward().cross(world_up).normalized();
    }

    Mat4 view_matrix() const {
        return look_at(position, position + forward(), {0.0f, 1.0f, 0.0f});
    }
};

} // namespace lantern
