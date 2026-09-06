// PEDAGOGY-TEST: GFX-PORTAL-05: sphere crosses portal plane and teleports
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `test_sphere_portal` — esfera atravessa portal A e reaparece em B.
// Caso 2: **Velocidade:** componente ao longo do normal é invertida.
// Caso 3: **Raio do portal:** esfera fora do disco não teleporta.
// Caso 4: **Plano:** detecção usa distância signed ao plano do portal.
// Caso 5: Valide solutions/ com os mesmos asserts.
#include "sphere_portal.hpp"
#include <cassert>
#include <cmath>
#include <iostream>

static bool near(float a, float b, float eps = 1e-3f) {
    return std::fabs(a - b) < eps;
}

int main() {
    PortalFrame a{{0.f, 0.f, 0.f}, {0.f, 0.f, 1.f}, {0.f, 1.f, 0.f}};
    PortalFrame b{{0.f, 0.f, 10.f}, {0.f, 0.f, -1.f}, {0.f, 1.f, 0.f}};
    PortalPair pair = make_portal_pair(a, b);

    Sphere sphere{{0.f, 0.f, -0.2f}, 0.3f, {0.f, 0.f, 4.f}};
    assert(sphere_crosses_portal_plane(sphere, a, 2.f));

    bool teleported = try_sphere_teleport(sphere, pair, true, 2.f);
    assert(teleported);
    assert(near(sphere.center.z, 10.2f));
    assert(near(sphere.velocity.z, -4.f));

    Sphere outside{{5.f, 0.f, 0.5f}, 0.3f, {0.f, 0.f, 1.f}};
    assert(!try_sphere_teleport(outside, pair, true, 1.f));

    std::cout << "OK sphere portal\n";
    return 0;
}
