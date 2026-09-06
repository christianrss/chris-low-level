// PEDAGOGY-TEST: GFX-PORTAL-04: verlet rope gravity + length constraint
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `test_verlet_rope` — corda de 5 segmentos com gravidade.
// Caso 2: **Comprimento:** soma dos segmentos permanece ≈ inicial após 60 steps.
// Caso 3: **Queda:** ponto médio desce com gravidade (y diminui).
// Caso 4: **Endpoints:** primeiro e último ponto fixos.
// Caso 5: Valide solutions/ com os mesmos asserts.
#include "verlet.hpp"
#include <cassert>
#include <cmath>
#include <iostream>

int main() {
    VerletRope rope;
    verlet_init_rope(rope, {0.f, 5.f, 0.f}, {4.f, 5.f, 0.f}, 5);
    float initial_len = verlet_total_length(rope);
    Vec3 mid_before = rope.points[2];

    for (int i = 0; i < 60; ++i) {
        verlet_step(rope, {0.f, -9.8f, 0.f}, 1.f / 60.f, 8);
    }

    float final_len = verlet_total_length(rope);
    assert(std::fabs(final_len - initial_len) < 0.15f);
    assert(rope.points[0].y == 5.f);
    assert(rope.points.back().y == 5.f);
    assert(rope.points[2].y < mid_before.y);

    std::cout << "OK verlet rope\n";
    return 0;
}
