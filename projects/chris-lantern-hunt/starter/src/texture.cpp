#include "texture.hpp"

#include <iostream>

namespace lantern {

unsigned int load_texture_2d(const std::string& path, bool /*srgb_repeat*/) {
    // TODO [LANTERN-TEX-02]: usar stb_image + glTexImage2D + mipmaps.
    std::cerr << "Texture not implemented yet: " << path << '\n';
    return 0;
}

void destroy_texture(unsigned int texture_id) {
    (void)texture_id;
}

} // namespace lantern
