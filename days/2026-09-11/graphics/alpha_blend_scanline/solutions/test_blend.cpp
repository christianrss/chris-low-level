#include "blend.hpp"
#include <cstdio>
static int fail(const char *m) { std::fprintf(stderr, "FAIL %s\n", m); return 1; }
int main() {
    /* PEDAGOGY-TEST: GFX-BLEND-01 */
    Pixel d{0,0,0,255}; Pixel s{255,0,0,128};
    blend_pixel(d, s);
    if (d.r < 120 || d.r > 135) return fail("r~128"); /* 255*128/255 ≈ 128 */
    /* PEDAGOGY-TEST: GFX-BLEND-02 */
    Pixel dst[2] = {{0,0,0,255},{0,0,0,255}};
    Pixel src[2] = {{255,0,0,255},{0,255,0,255}};
    blend_scanline(dst, src, 2);
    if (dst[0].r != 255 || dst[1].g != 255) return fail("scan");
    /* PEDAGOGY-TEST: GFX-BLEND-03 */
    if (blend_coverage(dst, 2, 200) != 2) return fail("cov");
    std::puts("ok"); return 0;
}
