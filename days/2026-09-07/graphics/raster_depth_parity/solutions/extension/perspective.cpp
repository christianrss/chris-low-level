// PEDAGOGY-SOLUTION: GFX-PERSP-04
float perspective_z_at(float z0, float w0, float z1, float w1, float t) {
    const float iz0 = (w0 != 0.0f) ? (z0 / w0) : z0;
    const float iz1 = (w1 != 0.0f) ? (z1 / w1) : z1;
    return iz0 * (1.0f - t) + iz1 * t;
}
