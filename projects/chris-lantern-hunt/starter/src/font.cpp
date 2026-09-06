#include "font.hpp"

namespace lantern {

bool FontRenderer::initialize() {
    // TODO [LANTERN-FONT-13]: carregar stb_truetype ou atlas bitmap.
    initialized_ = true;
    return true;
}

void FontRenderer::shutdown() {
    initialized_ = false;
}

void FontRenderer::begin_frame(int width, int height) {
    // TODO [LANTERN-FONT-13]: configurar projeção ortográfica para HUD.
    width_ = width;
    height_ = height;
}

void FontRenderer::end_frame() const {
    // TODO [LANTERN-FONT-13]
}

void FontRenderer::draw_text(float /*x*/, float /*y*/, float /*scale*/, const char* /*text*/, float /*r*/, float /*g*/,
    float /*b*/) const {
    // TODO [LANTERN-FONT-13]: desenhar quads por glyph com blend alpha.
}

void FontRenderer::draw_bar(float /*x*/, float /*y*/, float /*width*/, float /*height*/, float /*fill*/, float /*r*/,
    float /*g*/, float /*b*/) const {
    // Barras usadas pelo HUD — ver LANTERN-HUD-14 em hud.cpp.
}

} // namespace lantern
