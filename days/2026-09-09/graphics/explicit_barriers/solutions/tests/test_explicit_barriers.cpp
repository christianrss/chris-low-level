// PEDAGOGY-TEST: GFX-BAR-VALID
// PEDAGOGY-TEST: GFX-BAR-APPLY
// PEDAGOGY-TEST: GFX-BAR-TICK
// Test cases (TESTES_GUIADOS.md):
// Caso 1: can_transition permite so arestas legais (GFX-BAR-VALID).
// Caso 2: apply_barrier falha em ilegal e sucede no caminho feliz (GFX-BAR-APPLY).
// Caso 3: tick_barrier cicla e reseta Present→Undefined (GFX-BAR-TICK).
#include <cassert>
#include "barriers.hpp"

using namespace barr;

int main() {
    assert(can_transition(ResourceState::Undefined, ResourceState::CopyDst));
    assert(!can_transition(ResourceState::Undefined, ResourceState::Present));
    assert(can_transition(ResourceState::Present, ResourceState::RenderTarget));

    Resource r{};
    assert(r.state == ResourceState::Undefined);
    assert(!apply_barrier(r, ResourceState::Present));
    assert(r.state == ResourceState::Undefined);
    assert(apply_barrier(r, ResourceState::CopyDst));
    assert(r.state == ResourceState::CopyDst);

    Resource demo{};
    assert(tick_barrier(demo));
    assert(demo.state == ResourceState::CopyDst);
    assert(tick_barrier(demo));
    assert(demo.state == ResourceState::ShaderRead);
    assert(tick_barrier(demo));
    assert(demo.state == ResourceState::RenderTarget);
    assert(tick_barrier(demo));
    assert(demo.state == ResourceState::Present);
    assert(tick_barrier(demo));
    assert(demo.state == ResourceState::Undefined);
    return 0;
}
