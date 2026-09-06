#pragma once

#include <string>

namespace lantern {

// LANTERN-TEX-02: carrega PNG via stb_image e cria textura OpenGL.
unsigned int load_texture_2d(const std::string& path, bool srgb_repeat = true);

void destroy_texture(unsigned int texture_id);

} // namespace lantern
