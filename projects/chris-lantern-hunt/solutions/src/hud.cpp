#include "hud.hpp"

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <GL/gl.h>

#include <cstdio>

namespace lantern {

void draw_slime_overlay(float intensity) {
    // PEDAGOGY-SOLUTION: LANTERN-SLIME-11
    if (intensity <= 0.01f) {
        return;
    }

    const float alpha = intensity * 0.45f;
    glDisable(GL_DEPTH_TEST);
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();

    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glColor4f(0.1f, 0.55f, 0.15f, alpha);
    glBegin(GL_QUADS);
    glVertex2f(0.0f, 0.0f);
    glVertex2f(1.0f, 0.0f);
    glVertex2f(1.0f, 1.0f);
    glVertex2f(0.0f, 1.0f);
    glEnd();

    glDisable(GL_BLEND);
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
    glEnable(GL_DEPTH_TEST);
}

void HudRenderer::draw(const GameState& state, FontRenderer& font, int width, int height) const {
    // PEDAGOGY-SOLUTION: LANTERN-HUD-14
    font.begin_frame(width, height);

    font.draw_bar(20.0f, static_cast<float>(height) - 40.0f, 220.0f, 18.0f, state.player.health / 100.0f, 0.85f,
        0.2f, 0.2f);
    font.draw_text(24.0f, static_cast<float>(height) - 58.0f, 1.0f, "VIDA", 1.0f, 1.0f, 1.0f);

    if (state.player.water != WaterState::None) {
        font.draw_bar(20.0f, static_cast<float>(height) - 78.0f, 220.0f, 18.0f, state.player.breath / 100.0f,
            0.2f, 0.5f, 0.95f);
        font.draw_text(24.0f, static_cast<float>(height) - 96.0f, 1.0f, "RESPIRACAO", 0.8f, 0.9f, 1.0f);
    }

    char food_line[64];
    std::snprintf(food_line, sizeof(food_line), "COMIDA %d/%d", state.food_collected, kFoodToWin);
    font.draw_text(20.0f, 20.0f, 1.2f, food_line, 1.0f, 0.9f, 0.5f);

    if (const Objective* active = state.objectives.active_objective()) {
        font.draw_text(20.0f, 48.0f, 1.1f, active->description, 0.95f, 0.95f, 0.95f);
    }

    if (state.player.swimming) {
        font.draw_text(20.0f, 74.0f, 1.0f, "MODO: NATACAO", 0.4f, 0.8f, 1.0f);
    } else if (state.player.slime_slow > 0.1f) {
        font.draw_text(20.0f, 74.0f, 1.0f, "MODO: GOSMA", 0.4f, 1.0f, 0.4f);
    }

    font.end_frame();
}

void MenuRenderer::draw_main_menu(const GameState& state, FontRenderer& font, int width, int height) const {
    // PEDAGOGY-SOLUTION: LANTERN-MENU-15
    font.begin_frame(width, height);
    font.draw_text(static_cast<float>(width) * 0.32f, 120.0f, 2.0f, "LANTERN HUNT", 1.0f, 0.92f, 0.6f);

    const char* items[] = {"Jogar (seed 42)", "Jogar aleatorio", "Sair"};
    for (int i = 0; i < 3; ++i) {
        const float y = 260.0f + static_cast<float>(i) * 48.0f;
        const float r = state.menu_selection == i ? 1.0f : 0.7f;
        const float g = state.menu_selection == i ? 1.0f : 0.7f;
        font.draw_text(180.0f, y, 1.4f, items[i], r, g, 0.9f);
    }

    font.draw_text(120.0f, static_cast<float>(height) - 60.0f, 1.0f, "Setas/W/S: navegar  Enter: confirmar", 0.6f,
        0.6f, 0.6f);
    font.end_frame();
}

void MenuRenderer::draw_paused(FontRenderer& font, int width, int height) const {
    font.begin_frame(width, height);
    font.draw_text(static_cast<float>(width) * 0.38f, 200.0f, 1.8f, "PAUSADO", 1.0f, 1.0f, 1.0f);
    font.draw_text(200.0f, 280.0f, 1.2f, "Esc: continuar", 0.8f, 0.8f, 0.8f);
    font.end_frame();
}

void MenuRenderer::draw_game_over(bool victory, FontRenderer& font, int width, int height) const {
    font.begin_frame(width, height);
    if (victory) {
        font.draw_text(static_cast<float>(width) * 0.30f, 220.0f, 2.0f, "VITORIA!", 0.3f, 1.0f, 0.4f);
    } else {
        font.draw_text(static_cast<float>(width) * 0.28f, 220.0f, 2.0f, "GAME OVER", 1.0f, 0.3f, 0.3f);
    }
    font.draw_text(180.0f, 300.0f, 1.2f, "Enter: menu principal", 0.9f, 0.9f, 0.9f);
    font.end_frame();
}

} // namespace lantern
