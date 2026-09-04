#include "graphics.hpp"
#include <algorithm>
#include <stdexcept>

bool Pixel::operator==(const Pixel& other) const noexcept {
    return r == other.r && g == other.g && b == other.b && a == other.a;
}
Surface::Surface(std::size_t width, std::size_t height, Pixel clear)
    : width_(width), height_(height), pixels_(width * height, clear) {
    if (width == 0 || height == 0) throw std::invalid_argument("surface dimensions must be non-zero");
}
std::size_t Surface::index(std::size_t x, std::size_t y) const {
    // TODO ETAPA 1
    (void)x; (void)y; throw std::logic_error("TODO index");
}
Pixel Surface::pixel(std::size_t x, std::size_t y) const { return pixels_[index(x,y)]; }
void Surface::set_pixel(std::size_t x, std::size_t y, Pixel value) { pixels_[index(x,y)] = value; }
void Surface::fill_rect(int x, int y, int width, int height, Pixel value) {
    // TODO ETAPA 2
    (void)x; (void)y; (void)width; (void)height; (void)value;
}
static Pixel alpha_over(Pixel src, Pixel dst) {
    // TODO ETAPA 3
    (void)src; return dst;
}
Surface Compositor::compose(std::size_t width, std::size_t height, Pixel background,
                            const std::vector<Layer>& layers) {
    // TODO ETAPA 4
    (void)layers; return Surface(width, height, background);
}
