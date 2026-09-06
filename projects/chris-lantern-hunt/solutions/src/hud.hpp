#pragma once

#include "font.hpp"
#include "game.hpp"

namespace lantern {

class HudRenderer {
public:
    void draw(const GameState& state, FontRenderer& font, int width, int height) const;
};

class MenuRenderer {
public:
    void draw_main_menu(const GameState& state, FontRenderer& font, int width, int height) const;
    void draw_paused(FontRenderer& font, int width, int height) const;
    void draw_game_over(bool victory, FontRenderer& font, int width, int height) const;
};

void draw_slime_overlay(float intensity);

} // namespace lantern
