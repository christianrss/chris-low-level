#include "hud.hpp"

namespace lantern {

void draw_slime_overlay(float /*intensity*/) {
    // TODO [LANTERN-SLIME-11]: fullscreen tint verde com blend.
}

void HudRenderer::draw(const GameState& /*state*/, FontRenderer& /*font*/, int /*width*/, int /*height*/) const {
    // TODO [LANTERN-HUD-14]: vida, respiração, objetivo ativo, contador comida.
}

void MenuRenderer::draw_main_menu(const GameState& /*state*/, FontRenderer& /*font*/, int /*width*/, int /*height*/) const {
    // TODO [LANTERN-MENU-15]: Jogar / Jogar aleatório / Sair.
}

void MenuRenderer::draw_paused(FontRenderer& /*font*/, int /*width*/, int /*height*/) const {
    // TODO [LANTERN-MENU-15]
}

void MenuRenderer::draw_game_over(bool /*victory*/, FontRenderer& /*font*/, int /*width*/, int /*height*/) const {
    // TODO [LANTERN-MENU-15]
}

} // namespace lantern
