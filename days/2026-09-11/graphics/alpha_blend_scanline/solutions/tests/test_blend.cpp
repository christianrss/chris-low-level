// PEDAGOGY-TEST: GFX-BLEND-PIXEL
// PEDAGOGY-TEST: GFX-BLEND-SCAN
// PEDAGOGY-TEST: GFX-BLEND-SPRITE
// Test cases (TESTES_GUIADOS.md):
// Caso 1: blend_pixel src-over (GFX-BLEND-PIXEL).
// Caso 2: blend_scanline row (GFX-BLEND-SCAN).
// Caso 3: update_sprite moves (GFX-BLEND-SPRITE).
#include "blend.hpp"
#include <cassert>

int main() {
    using namespace blendlab;
    Pixel dst{0, 0, 0, 255};
    Pixel src{255, 0, 0, 128};
    blend_pixel(dst, src);
    assert(dst.r > 100);

    Pixel line_d[2] = {{0, 0, 0, 255}, {0, 0, 0, 255}};
    Pixel line_s[2] = {{0, 255, 0, 255}, {0, 0, 255, 255}};
    blend_scanline(line_d, line_s, 2);
    assert(line_d[0].g == 255);

    Sprite s{10, 10, 50, -40, 20, 20, {255, 255, 255, 128}};
    update_sprite(s, 0.1f, 0, 0, 100, 100);
    assert(s.x > 10);
    return 0;
}
