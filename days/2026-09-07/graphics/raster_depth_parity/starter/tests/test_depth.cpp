// PEDAGOGY-TEST: GFX-DEPTH-CPU-01
// PEDAGOGY-TEST: GFX-DEPTH-GL-02
// PEDAGOGY-TEST: GFX-DEPTH-PARITY-03
// PEDAGOGY-TEST: GFX-PERSP-04
// Test cases (TESTES_GUIADOS.md):
// Caso 1: DepthBuffer::test aceita menor z e rejeita maior (GFX-DEPTH-CPU-01).
// Caso 2: depth_gl habilita GL_DEPTH_TEST (GFX-DEPTH-GL-02).
// Caso 3: triângulo azul na frente vence vermelho atrás (GFX-DEPTH-PARITY-03).
// Caso 4: perspective_z_at interpola z/w (GFX-PERSP-04).
#include <cassert>
#include "depth_buffer.hpp"
using namespace depth_lab;

int main() {
    DepthBuffer db;
    db.resize(4, 4);
    db.clear(1.0f);
    assert(db.test(1, 1, 0.5f));
    assert(!db.test(1, 1, 0.9f));
    assert(db.test(1, 1, 0.3f));
    return 0;
}