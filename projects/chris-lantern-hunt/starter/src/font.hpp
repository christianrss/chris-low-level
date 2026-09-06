#pragma once

namespace lantern {

class FontRenderer {
public:
    bool initialize();
    void shutdown();
    void begin_frame(int width, int height);
    void end_frame() const;
    void draw_text(float x, float y, float scale, const char* text, float r, float g, float b) const;
    void draw_bar(float x, float y, float width, float height, float fill, float r, float g, float b) const;

private:
    bool initialized_ = false;
    int width_ = 0;
    int height_ = 0;
};

} // namespace lantern
