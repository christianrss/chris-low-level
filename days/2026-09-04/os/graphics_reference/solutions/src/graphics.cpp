#include "graphics.hpp"
#include <algorithm>
#include <stdexcept>

bool Pixel::operator==(const Pixel& other) const noexcept {
    return r == other.r && g == other.g && b == other.b && a == other.a;
}

bool Rect::empty() const noexcept {
    return width <= 0 || height <= 0;
}

std::size_t Rect::area() const noexcept {
    if (empty()) {
        return 0;
    }
    return static_cast<std::size_t>(width) * static_cast<std::size_t>(height);
}

Rect Rect::from_bounds(int x0, int y0, int x1, int y1) noexcept {
    if (x1 <= x0 || y1 <= y0) {
        return {};
    }
    return Rect{x0, y0, x1 - x0, y1 - y0};
}

Rect Rect::intersect(Rect other) const noexcept {
    if (empty() || other.empty()) {
        return {};
    }
    const int x0 = std::max(x, other.x);
    const int y0 = std::max(y, other.y);
    const int x1 = std::min(x + width, other.x + other.width);
    const int y1 = std::min(y + height, other.y + other.height);
    return from_bounds(x0, y0, x1, y1);
}

Rect Rect::unite(Rect other) const noexcept {
    if (empty()) {
        return other;
    }
    if (other.empty()) {
        return *this;
    }
    const int x0 = std::min(x, other.x);
    const int y0 = std::min(y, other.y);
    const int x1 = std::max(x + width, other.x + other.width);
    const int y1 = std::max(y + height, other.y + other.height);
    return from_bounds(x0, y0, x1, y1);
}

void DirtyTracker::clear() noexcept {
    union_ = {};
    has_ = false;
}

// PEDAGOGY-SOLUTION: D2-GFX-DIRTY-RECT
void DirtyTracker::mark_dirty(int x, int y, int width, int height) {
    if (width <= 0 || height <= 0) {
        return;
    }
    const Rect added{x, y, width, height};
    if (!has_ || union_.empty()) {
        union_ = added;
        has_ = true;
        return;
    }
    union_ = union_.unite(added);
}

void DirtyTracker::mark_dirty(Rect r) {
    mark_dirty(r.x, r.y, r.width, r.height);
}

bool DirtyTracker::empty() const noexcept {
    return !has_ || union_.empty();
}

Rect DirtyTracker::dirty_union() const noexcept {
    return empty() ? Rect{} : union_;
}

// PEDAGOGY-SOLUTION: D2-GFX-DIRTY-RECT
Rect DirtyTracker::take_dirty_union() {
    const Rect out = dirty_union();
    clear();
    return out;
}

Surface::Surface(std::size_t width, std::size_t height, Pixel clear)
    : width_(width), height_(height), pixels_(width * height, clear) {
    if (width == 0 || height == 0) {
        throw std::invalid_argument("surface dimensions must be non-zero");
    }
}

// PEDAGOGY-SOLUTION: D2-GFX-INDEX
std::size_t Surface::index(std::size_t x, std::size_t y) const {
    if (x >= width_ || y >= height_) {
        throw std::out_of_range("pixel outside surface");
    }
    return y * width_ + x;
}

Pixel Surface::pixel(std::size_t x, std::size_t y) const {
    return pixels_[index(x, y)];
}

void Surface::set_pixel(std::size_t x, std::size_t y, Pixel value) {
    pixels_[index(x, y)] = value;
}

// PEDAGOGY-SOLUTION: D2-GFX-FILL-RECT
void Surface::fill_rect(int x, int y, int width, int height, Pixel value) {
    if (width <= 0 || height <= 0) {
        return;
    }
    const int x0 = std::max(0, x);
    const int y0 = std::max(0, y);
    const int x1 = std::min(static_cast<int>(width_), x + width);
    const int y1 = std::min(static_cast<int>(height_), y + height);
    if (x0 >= x1 || y0 >= y1) {
        return;
    }
    for (int py = y0; py < y1; ++py) {
        for (int px = x0; px < x1; ++px) {
            set_pixel(static_cast<std::size_t>(px), static_cast<std::size_t>(py), value);
        }
    }
    // PEDAGOGY-SOLUTION: D2-GFX-DIRTY-RECT
    mark_dirty(x0, y0, x1 - x0, y1 - y0);
}

void Surface::mark_dirty(int x, int y, int width, int height) {
    dirty_.mark_dirty(x, y, width, height);
}

void Surface::mark_dirty(Rect r) {
    dirty_.mark_dirty(r);
}

Rect Surface::take_dirty_union() {
    return dirty_.take_dirty_union();
}

Rect Surface::dirty_union() const noexcept {
    return dirty_.dirty_union();
}

bool Surface::has_dirty() const noexcept {
    return !dirty_.empty();
}

static // PEDAGOGY-SOLUTION: D2-GFX-ALPHA-OVER
Pixel alpha_over(Pixel src, Pixel dst) {
    const unsigned alpha = src.a;
    const unsigned inv = 255u - alpha;
    Pixel out;
    out.r = static_cast<std::uint8_t>((src.r * alpha + dst.r * inv + 127u) / 255u);
    out.g = static_cast<std::uint8_t>((src.g * alpha + dst.g * inv + 127u) / 255u);
    out.b = static_cast<std::uint8_t>((src.b * alpha + dst.b * inv + 127u) / 255u);
    out.a = 255;
    return out;
}

static Rect layer_dest_rect(const Layer& layer) {
    if (layer.surface == nullptr) {
        return {};
    }
    return Rect{
        layer.x,
        layer.y,
        static_cast<int>(layer.surface->width()),
        static_cast<int>(layer.surface->height())};
}

static Pixel sample_composed(
    std::size_t px,
    std::size_t py,
    Pixel background,
    const std::vector<Layer>& layers) {
    Pixel out = background;
    for (const auto& layer : layers) {
        if (layer.surface == nullptr) {
            continue;
        }
        const int sx = static_cast<int>(px) - layer.x;
        const int sy = static_cast<int>(py) - layer.y;
        if (sx < 0 || sy < 0 || sx >= static_cast<int>(layer.surface->width()) ||
            sy >= static_cast<int>(layer.surface->height())) {
            continue;
        }
        out = alpha_over(
            layer.surface->pixel(static_cast<std::size_t>(sx), static_cast<std::size_t>(sy)),
            out);
    }
    return out;
}

// PEDAGOGY-SOLUTION: D2-GFX-COMPOSE
Surface Compositor::compose(
    std::size_t width,
    std::size_t height,
    Pixel background,
    const std::vector<Layer>& layers) {
    Surface output(width, height, background);
    const Rect bounds{0, 0, static_cast<int>(width), static_cast<int>(height)};
    for (const auto& layer : layers) {
        if (layer.surface == nullptr) {
            continue;
        }
        for (std::size_t sy = 0; sy < layer.surface->height(); ++sy) {
            for (std::size_t sx = 0; sx < layer.surface->width(); ++sx) {
                const int dx = layer.x + static_cast<int>(sx);
                const int dy = layer.y + static_cast<int>(sy);
                if (dx < 0 || dy < 0 || dx >= static_cast<int>(width) ||
                    dy >= static_cast<int>(height)) {
                    continue;
                }
                const auto ux = static_cast<std::size_t>(dx);
                const auto uy = static_cast<std::size_t>(dy);
                output.set_pixel(
                    ux,
                    uy,
                    alpha_over(layer.surface->pixel(sx, sy), output.pixel(ux, uy)));
            }
        }
        // PEDAGOGY-SOLUTION: D2-GFX-DIRTY-RECT
        const Rect footprint = layer_dest_rect(layer).intersect(bounds);
        if (!footprint.empty()) {
            output.mark_dirty(footprint);
        }
    }
    return output;
}

// PEDAGOGY-SOLUTION: D2-GFX-FRAME-PACE
FrameStats FramePacer::compose_with_damage(
    Surface& target,
    Pixel background,
    const std::vector<Layer>& layers,
    Rect damage) {
    FrameStats stats{};
    const Rect bounds{
        0,
        0,
        static_cast<int>(target.width()),
        static_cast<int>(target.height())};
    const Rect region = damage.intersect(bounds);
    stats.dirty_area = region.area();
    if (region.empty()) {
        return stats;
    }
    for (int py = region.y; py < region.y + region.height; ++py) {
        for (int px = region.x; px < region.x + region.width; ++px) {
            const auto ux = static_cast<std::size_t>(px);
            const auto uy = static_cast<std::size_t>(py);
            target.set_pixel(ux, uy, sample_composed(ux, uy, background, layers));
            ++stats.pixels_touched;
        }
    }
    target.mark_dirty(region);
    return stats;
}

FrameStats FramePacer::compose_with_damage(
    Surface& target,
    Pixel background,
    const std::vector<Layer>& layers,
    DirtyTracker& damage) {
    return compose_with_damage(target, background, layers, damage.take_dirty_union());
}
