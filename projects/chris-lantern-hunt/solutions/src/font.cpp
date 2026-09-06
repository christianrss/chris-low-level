#include "font.hpp"

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <GL/gl.h>

#include <cstring>

namespace lantern {

namespace {

// PEDAGOGY-SOLUTION: LANTERN-FONT-13 — fonte bitmap 5x7 embutida (ASCII 32..126).
const unsigned char kGlyphRows = 7;
const unsigned char kGlyphCols = 5;

bool glyph_pixel(char c, int col, int row) {
    static const unsigned char font5x7[][5] = {
        {0x00, 0x00, 0x00, 0x00, 0x00}, // space
        {0x00, 0x00, 0x5F, 0x00, 0x00}, // !
        {0x00, 0x07, 0x00, 0x07, 0x00}, // "
        {0x14, 0x7F, 0x14, 0x7F, 0x14}, // #
        {0x24, 0x2A, 0x7F, 0x2A, 0x12}, // $
        {0x23, 0x13, 0x08, 0x64, 0x62}, // %
        {0x36, 0x49, 0x55, 0x22, 0x50}, // &
        {0x00, 0x05, 0x03, 0x00, 0x00}, // '
        {0x00, 0x1C, 0x22, 0x41, 0x00}, // (
        {0x00, 0x41, 0x22, 0x1C, 0x00}, // )
        {0x14, 0x08, 0x3E, 0x08, 0x14}, // *
        {0x08, 0x08, 0x3E, 0x08, 0x08}, // +
        {0x00, 0x50, 0x30, 0x00, 0x00}, // ,
        {0x08, 0x08, 0x08, 0x08, 0x08}, // -
        {0x00, 0x60, 0x60, 0x00, 0x00}, // .
        {0x20, 0x10, 0x08, 0x04, 0x02}, // /
        {0x3E, 0x51, 0x49, 0x45, 0x3E}, // 0
        {0x00, 0x42, 0x7F, 0x40, 0x00}, // 1
        {0x42, 0x61, 0x51, 0x49, 0x46}, // 2
        {0x21, 0x41, 0x45, 0x4B, 0x31}, // 3
        {0x18, 0x14, 0x12, 0x7F, 0x10}, // 4
        {0x27, 0x45, 0x45, 0x45, 0x39}, // 5
        {0x3C, 0x4A, 0x49, 0x49, 0x30}, // 6
        {0x01, 0x71, 0x09, 0x05, 0x03}, // 7
        {0x36, 0x49, 0x49, 0x49, 0x36}, // 8
        {0x06, 0x49, 0x49, 0x29, 0x1E}, // 9
        {0x00, 0x36, 0x36, 0x00, 0x00}, // :
        {0x00, 0x56, 0x36, 0x00, 0x00}, // ;
        {0x08, 0x14, 0x22, 0x41, 0x00}, // <
        {0x14, 0x14, 0x14, 0x14, 0x14}, // =
        {0x00, 0x41, 0x22, 0x14, 0x08}, // >
        {0x02, 0x01, 0x51, 0x09, 0x06}, // ?
        {0x32, 0x49, 0x79, 0x41, 0x3E}, // @
        {0x7E, 0x11, 0x11, 0x11, 0x7E}, // A
        {0x7F, 0x49, 0x49, 0x49, 0x36}, // B
        {0x3E, 0x41, 0x41, 0x41, 0x22}, // C
        {0x7F, 0x41, 0x41, 0x22, 0x1C}, // D
        {0x7F, 0x49, 0x49, 0x49, 0x41}, // E
        {0x7F, 0x09, 0x09, 0x09, 0x01}, // F
        {0x3E, 0x41, 0x49, 0x49, 0x7A}, // G
        {0x7F, 0x08, 0x08, 0x08, 0x7F}, // H
        {0x00, 0x41, 0x7F, 0x41, 0x00}, // I
        {0x20, 0x40, 0x41, 0x3F, 0x01}, // J
        {0x7F, 0x08, 0x14, 0x22, 0x41}, // K
        {0x7F, 0x40, 0x40, 0x40, 0x40}, // L
        {0x7F, 0x02, 0x0C, 0x02, 0x7F}, // M
        {0x7F, 0x04, 0x08, 0x10, 0x7F}, // N
        {0x3E, 0x41, 0x41, 0x41, 0x3E}, // O
        {0x7F, 0x09, 0x09, 0x09, 0x06}, // P
        {0x3E, 0x41, 0x51, 0x21, 0x5E}, // Q
        {0x7F, 0x09, 0x19, 0x29, 0x46}, // R
        {0x46, 0x49, 0x49, 0x49, 0x31}, // S
        {0x01, 0x01, 0x7F, 0x01, 0x01}, // T
        {0x3F, 0x40, 0x40, 0x40, 0x3F}, // U
        {0x1F, 0x20, 0x40, 0x20, 0x1F}, // V
        {0x3F, 0x40, 0x38, 0x40, 0x3F}, // W
        {0x63, 0x14, 0x08, 0x14, 0x63}, // X
        {0x07, 0x08, 0x70, 0x08, 0x07}, // Y
        {0x61, 0x51, 0x49, 0x45, 0x43}, // Z
    };

    if (c < ' ' || c > 'Z') {
        return false;
    }
    const int index = static_cast<int>(c) - static_cast<int>(' ');
    if (index < 0 || index >= 59) {
        return false;
    }
    const unsigned char col_bits = font5x7[index][col];
    return (col_bits >> row) & 1;
}

} // namespace

bool FontRenderer::initialize() {
    initialized_ = true;
    return true;
}

void FontRenderer::shutdown() {
    initialized_ = false;
}

void FontRenderer::begin_frame(int width, int height) {
    width_ = width;
    height_ = height;

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(width_), static_cast<double>(height_), 0.0, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();

    glDisable(GL_DEPTH_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

void FontRenderer::end_frame() const {
    glDisable(GL_BLEND);
    glEnable(GL_DEPTH_TEST);
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
}

void FontRenderer::draw_bar(float x, float y, float width, float height, float fill, float r, float g,
    float b) const {
    const float clamped = fill < 0.0f ? 0.0f : (fill > 1.0f ? 1.0f : fill);
    glColor4f(0.1f, 0.1f, 0.1f, 0.85f);
    glBegin(GL_QUADS);
    glVertex2f(x, y);
    glVertex2f(x + width, y);
    glVertex2f(x + width, y + height);
    glVertex2f(x, y + height);
    glEnd();

    glColor4f(r, g, b, 0.95f);
    glBegin(GL_QUADS);
    glVertex2f(x, y);
    glVertex2f(x + width * clamped, y);
    glVertex2f(x + width * clamped, y + height);
    glVertex2f(x, y + height);
    glEnd();
}

void FontRenderer::draw_text(float x, float y, float scale, const char* text, float r, float g, float b) const {
    if (text == nullptr) {
        return;
    }

    float cursor_x = x;
    const float pixel = 2.0f * scale;
    glColor4f(r, g, b, 1.0f);

    for (const char* ch = text; *ch != '\0'; ++ch) {
        if (*ch == '\n') {
            cursor_x = x;
            y += (kGlyphRows + 2) * pixel;
            continue;
        }

        for (int row = 0; row < kGlyphRows; ++row) {
            for (int col = 0; col < kGlyphCols; ++col) {
                if (!glyph_pixel(*ch, col, row)) {
                    continue;
                }
                const float px = cursor_x + static_cast<float>(col) * pixel;
                const float py = y + static_cast<float>(row) * pixel;
                glBegin(GL_QUADS);
                glVertex2f(px, py);
                glVertex2f(px + pixel, py);
                glVertex2f(px + pixel, py + pixel);
                glVertex2f(px, py + pixel);
                glEnd();
            }
        }
        cursor_x += (kGlyphCols + 1) * pixel;
    }
}

} // namespace lantern
