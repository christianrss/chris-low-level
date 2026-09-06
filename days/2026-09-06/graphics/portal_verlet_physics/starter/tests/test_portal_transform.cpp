// PEDAGOGY-TEST: GFX-PORTAL-01: Mat4 identity, multiply, transform point
// PEDAGOGY-TEST: GFX-PORTAL-02: portal frame matrices A and B
// PEDAGOGY-TEST: GFX-PORTAL-03: portal_transport A↔B preserves local offset
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `test_portal_transform` — Mat4 e par de portais opostos.
// Caso 2: **Round-trip:** ponto atravessa A→B→A e retorna ao original.
// Caso 3: **Offset local:** (0,0,2) em A aparece a 2 unidades do centro de B.
// Caso 4: **Inversa rígida:** mat4_inverse_rigid ∘ frame == identity.
// Caso 5: Valide solutions/ com os mesmos asserts.
#include "math.hpp"
#include "portal.hpp"
#include <cassert>
#include <cmath>
#include <iostream>

static bool near(float a, float b, float eps = 1e-4f) {
    return std::fabs(a - b) < eps;
}

static bool near_vec(Vec3 a, Vec3 b, float eps = 1e-4f) {
    return near(a.x, b.x, eps) && near(a.y, b.y, eps) && near(a.z, b.z, eps);
}

int main() {
    Mat4 id = mat4_identity();
    Vec3 p{1.f, 2.f, 3.f};
    assert(near_vec(mat4_transform_point(id, p), p));

    Mat4 t = mat4_translate({0.f, 0.f, 10.f});
    Vec3 moved = mat4_transform_point(t, {0.f, 0.f, 2.f});
    assert(near(moved.z, 12.f));

    PortalFrame a{{0.f, 0.f, 0.f}, {0.f, 0.f, 1.f}, {0.f, 1.f, 0.f}};
    PortalFrame b{{0.f, 0.f, 10.f}, {0.f, 0.f, -1.f}, {0.f, 1.f, 0.f}};
    PortalPair pair = make_portal_pair(a, b);

    Vec3 through = portal_transport_position(pair, true, {0.f, 0.f, 2.f});
    assert(near(through.z, 8.f));

    Vec3 back = portal_transport_position(pair, false, through);
    assert(near_vec(back, {0.f, 0.f, 2.f}));

    Vec3 vel = portal_transport_velocity(pair, true, {0.f, 0.f, 5.f});
    assert(near(vel.z, -5.f));

    std::cout << "OK portal transform\n";
    return 0;
}
