#include "blend.hpp"
void blend_pixel(Pixel &dst, Pixel src) {
    /* TODO [GFX-BLEND-01]: src-over: out = src + dst*(1-src.a/255) per channel */
    (void)dst; (void)src;
}
void blend_scanline(Pixel *dst, const Pixel *src, int n) {
    /* TODO [GFX-BLEND-02]: blend n pixels */
    (void)dst; (void)src; (void)n;
}
int blend_coverage(const Pixel *dst, int n, uint8_t min_a) {
    /* TODO [GFX-BLEND-03]: count pixels with a >= min_a */
    (void)dst; (void)n; (void)min_a; return -1;
}
