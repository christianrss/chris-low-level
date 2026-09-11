// PEDAGOGY-TEST: GFX-ART-PHYS-01
// PEDAGOGY-TEST: GFX-ART-TERRAIN-02
// PEDAGOGY-TEST: GFX-ART-TRAIL-03
// PEDAGOGY-TEST: GFX-ART-SW-04
// PEDAGOGY-TEST: GFX-ART-GL-05
// PEDAGOGY-TEST: GFX-ART-D3D-06
// Test cases (TESTES_GUIADOS.md):
// Caso 1: integrate() aplica gravidade e atualiza posição (GFX-ART-PHYS-01).
// Caso 2: terrain_hit() detecta y <= sample(x) (GFX-ART-TERRAIN-02).
// Caso 3: trail_push() acumula pontos da parábola (GFX-ART-TRAIL-03).
// Caso 4: artillery_sw exibe terreno + projétil via DIB (GFX-ART-SW-04).
// Caso 5: artillery_gl mesma cena em ortho OpenGL (GFX-ART-GL-05).
// Caso 6: artillery_d3d apresenta via DXGI (GFX-ART-D3D-06).
#include <cassert>
#include <cmath>
#include "artillery.hpp"

using namespace art2d;

int main() {
    Projectile p{};
    fire(p, 45.0f, 100.0f);
    assert(p.alive);
    assert(std::fabs(p.vel.x - p.vel.y) < 0.01f);

    integrate(p, 0.5f, 9.8f);
    assert(p.pos.x > 0.0f);
    assert(p.pos.y > 0.0f);

    Terrain t;
    t.heights.assign(64, 0.0f);
    t.heights[32] = 50.0f;
    p.pos = {320.0f, 40.0f};
    p.alive = true;
    assert(terrain_hit(p, t));

    Trail trail{};
    trail_push(trail, {1.0f, 2.0f});
    trail_push(trail, {3.0f, 4.0f});
    assert(trail.count == 2);
    return 0;
}