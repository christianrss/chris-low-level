#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>

struct Pixel {
    std::uint8_t r = 0;
    std::uint8_t g = 0;
    std::uint8_t b = 0;
    std::uint8_t a = 255;

    bool operator==(const Pixel& other) const noexcept;
};

struct Rect {
    int x = 0;
    int y = 0;
    int width = 0;
    int height = 0;

    bool empty() const noexcept;
    std::size_t area() const noexcept;
    Rect intersect(Rect other) const noexcept;
    Rect unite(Rect other) const noexcept;
    static Rect from_bounds(int x0, int y0, int x1, int y1) noexcept;
};

class DirtyTracker {
public:
    void clear() noexcept;
    void mark_dirty(int x, int y, int width, int height);
    void mark_dirty(Rect r);
    bool empty() const noexcept;
    Rect dirty_union() const noexcept;
    Rect take_dirty_union();

private:
    Rect union_{};
    bool has_ = false;
};

class Surface {
public:
    Surface(std::size_t width, std::size_t height, Pixel clear = {});

    std::size_t width() const noexcept { return width_; }
    std::size_t height() const noexcept { return height_; }
    Pixel pixel(std::size_t x, std::size_t y) const;
    void set_pixel(std::size_t x, std::size_t y, Pixel value);
    void fill_rect(int x, int y, int width, int height, Pixel value);

    void mark_dirty(int x, int y, int width, int height);
    void mark_dirty(Rect r);
    Rect take_dirty_union();
    Rect dirty_union() const noexcept;
    bool has_dirty() const noexcept;

private:
    std::size_t index(std::size_t x, std::size_t y) const;
    std::size_t width_ = 0;
    std::size_t height_ = 0;
    std::vector<Pixel> pixels_;
    DirtyTracker dirty_;
};

struct Layer {
    const Surface* surface = nullptr;
    int x = 0;
    int y = 0;
};

struct FrameStats {
    std::size_t pixels_touched = 0;
    std::size_t dirty_area = 0;
};

class Compositor {
public:
    static Surface compose(
        std::size_t width,
        std::size_t height,
        Pixel background,
        const std::vector<Layer>& layers);
};

class FramePacer {
public:
    static FrameStats compose_with_damage(
        Surface& target,
        Pixel background,
        const std::vector<Layer>& layers,
        Rect damage);

    static FrameStats compose_with_damage(
        Surface& target,
        Pixel background,
        const std::vector<Layer>& layers,
        DirtyTracker& damage);
};
