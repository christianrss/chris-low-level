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

void DirtyTracker::mark_dirty(int x, int y, int width, int height) {
    // TODO [D2-GFX-DIRTY-RECT]: unir o retangulo ao dirty AABB (ignorar vazio).
    (void)x;
    (void)y;
    (void)width;
    (void)height;
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

Rect DirtyTracker::take_dirty_union() {
    // TODO [D2-GFX-DIRTY-RECT]: devolver a uniao atual e limpar o tracker.
    return {};
}

Surface::Surface(std::size_t width, std::size_t height, Pixel clear)
    : width_(width), height_(height), pixels_(width * height, clear) {
    if (width == 0 || height == 0) {
        throw std::invalid_argument("surface dimensions must be non-zero");
    }
}

std::size_t Surface::index(std::size_t x, std::size_t y) const {
    // TODO [D2-GFX-INDEX]: validar coordenadas e converter (x,y) em indice linear.
    (void)x;
    (void)y;
    throw std::logic_error("TODO index");
}

Pixel Surface::pixel(std::size_t x, std::size_t y) const {
    return pixels_[index(x, y)];
}

void Surface::set_pixel(std::size_t x, std::size_t y, Pixel value) {
    pixels_[index(x, y)] = value;
}

void Surface::fill_rect(int x, int y, int width, int height, Pixel value) {
    // TODO [D2-GFX-FILL-RECT]: recortar o retangulo e preencher pixels validos.
    // TODO [D2-GFX-DIRTY-RECT]: apos o clip, mark_dirty na regiao realmente escrita.
    (void)x;
    (void)y;
    (void)width;
    (void)height;
    (void)value;
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

static Pixel alpha_over(Pixel src, Pixel dst) {
    // TODO [D2-GFX-ALPHA-OVER]: compor src sobre dst com alpha inteiro.
    (void)src;
    return dst;
}

Surface Compositor::compose(
    std::size_t width,
    std::size_t height,
    Pixel background,
    const std::vector<Layer>& layers) {
    // TODO [D2-GFX-COMPOSE]: percorrer layers, aplicar offset/clipping e alpha-over.
    // Ao blit de cada layer, mark_dirty no footprint de destino (D2-GFX-DIRTY-RECT).
    (void)layers;
    return Surface(width, height, background);
}

FrameStats FramePacer::compose_with_damage(
    Surface& target,
    Pixel background,
    const std::vector<Layer>& layers,
    Rect damage) {
    // TODO [D2-GFX-FRAME-PACE]: recompor so a regiao damage; preencher FrameStats.
    (void)target;
    (void)background;
    (void)layers;
    (void)damage;
    return {};
}

FrameStats FramePacer::compose_with_damage(
    Surface& target,
    Pixel background,
    const std::vector<Layer>& layers,
    DirtyTracker& damage) {
    return compose_with_damage(target, background, layers, damage.take_dirty_union());
}
