#include "graphics.hpp"
#include <algorithm>
#include <stdexcept>

bool Pixel::operator==(const Pixel& other) const noexcept { return r == other.r && g == other.g && b == other.b && a == other.a; }

Surface::Surface(std::size_t width, std::size_t height, Pixel clear) : width_(width), height_(height), pixels_(width * height, clear) {
    if (width == 0 || height == 0) throw std::invalid_argument("surface dimensions must be non-zero");
}

std::size_t Surface::index(std::size_t x, std::size_t y) const {
    if (x >= width_ || y >= height_) throw std::out_of_range("pixel outside surface");
    return y * width_ + x;
}
Pixel Surface::pixel(std::size_t x, std::size_t y) const { return pixels_[index(x, y)]; }
void Surface::set_pixel(std::size_t x, std::size_t y, Pixel value) { pixels_[index(x, y)] = value; }
void Surface::fill_rect(int x, int y, int width, int height, Pixel value) {
    if (width <= 0 || height <= 0) return;
    const int x0 = std::max(0, x), y0 = std::max(0, y);
    const int x1 = std::min(static_cast<int>(width_), x + width), y1 = std::min(static_cast<int>(height_), y + height);
    for (int py = y0; py < y1; ++py) for (int px = x0; px < x1; ++px) set_pixel(static_cast<std::size_t>(px), static_cast<std::size_t>(py), value);
}

static Pixel alpha_over(Pixel src, Pixel dst) {
    const unsigned alpha = src.a, inv = 255u - alpha;
    Pixel out;
    out.r = static_cast<std::uint8_t>((src.r * alpha + dst.r * inv + 127u) / 255u);
    out.g = static_cast<std::uint8_t>((src.g * alpha + dst.g * inv + 127u) / 255u);
    out.b = static_cast<std::uint8_t>((src.b * alpha + dst.b * inv + 127u) / 255u);
    out.a = 255;
    return out;
}

Surface Compositor::compose(std::size_t width, std::size_t height, Pixel background, const std::vector<Layer>& layers) {
    Surface output(width, height, background);
    for (const auto& layer : layers) {
        if (layer.surface == nullptr) continue;
        for (std::size_t sy = 0; sy < layer.surface->height(); ++sy) for (std::size_t sx = 0; sx < layer.surface->width(); ++sx) {
            const int dx = layer.x + static_cast<int>(sx), dy = layer.y + static_cast<int>(sy);
            if (dx < 0 || dy < 0 || dx >= static_cast<int>(width) || dy >= static_cast<int>(height)) continue;
            const auto ux = static_cast<std::size_t>(dx), uy = static_cast<std::size_t>(dy);
            output.set_pixel(ux, uy, alpha_over(layer.surface->pixel(sx, sy), output.pixel(ux, uy)));
        }
    }
    return output;
}
