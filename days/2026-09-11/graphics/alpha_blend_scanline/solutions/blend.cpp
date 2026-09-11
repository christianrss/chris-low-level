#include "blend.hpp"
static uint8_t lerp8(uint8_t d, uint8_t s, uint8_t a) {
    return (uint8_t)((s * a + d * (255 - a) + 127) / 255);
}
void blend_pixel(Pixel &dst, Pixel src) {
    /* PEDAGOGY-SOLUTION: GFX-BLEND-01 */
    uint8_t a = src.a;
    dst.r = lerp8(dst.r, src.r, a);
    dst.g = lerp8(dst.g, src.g, a);
    dst.b = lerp8(dst.b, src.b, a);
    dst.a = (uint8_t)(a + (dst.a * (255 - a) + 127) / 255);
}
void blend_scanline(Pixel *dst, const Pixel *src, int n) {
    /* PEDAGOGY-SOLUTION: GFX-BLEND-02 */
    for (int i = 0; i < n; ++i) blend_pixel(dst[i], src[i]);
}
int blend_coverage(const Pixel *dst, int n, uint8_t min_a) {
    /* PEDAGOGY-SOLUTION: GFX-BLEND-03 */
    int c = 0;
    if (!dst || n < 0) return -1;
    for (int i = 0; i < n; ++i) if (dst[i].a >= min_a) ++c;
    return c;
}
