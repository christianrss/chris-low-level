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

class Surface {
public:
    Surface(std::size_t width, std::size_t height, Pixel clear = {});

    std::size_t width() const noexcept { return width_; }
    std::size_t height() const noexcept { return height_; }
    Pixel pixel(std::size_t x, std::size_t y) const;
    void set_pixel(std::size_t x, std::size_t y, Pixel value);
    void fill_rect(int x, int y, int width, int height, Pixel value);

private:
    std::size_t index(std::size_t x, std::size_t y) const;
    std::size_t width_ = 0;
    std::size_t height_ = 0;
    std::vector<Pixel> pixels_;
};

struct Layer {
    const Surface* surface = nullptr;
    int x = 0;
    int y = 0;
};

class Compositor {
public:
    static Surface compose(
        std::size_t width,
        std::size_t height,
        Pixel background,
        const std::vector<Layer>& layers);
};
