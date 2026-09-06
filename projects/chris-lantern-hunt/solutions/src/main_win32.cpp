#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <GL/gl.h>

#include "audio.hpp"
#include "checkpoint.hpp"
#include "font.hpp"
#include "game.hpp"
#include "hud.hpp"
#include "math.hpp"
#include "texture.hpp"

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

namespace {

constexpr float kPi = 3.1415926535f;

#ifndef GL_ARRAY_BUFFER
#define GL_ARRAY_BUFFER 0x8892
#define GL_STATIC_DRAW 0x88E4
#define GL_VERTEX_SHADER 0x8B31
#define GL_FRAGMENT_SHADER 0x8B30
#define GL_COMPILE_STATUS 0x8B81
#define GL_LINK_STATUS 0x8B82
#define GL_TEXTURE0 0x84C0
#define GL_TEXTURE1 0x84C1
#endif

struct Vertex {
    float px, py, pz;
    float nx, ny, nz;
    float u, v;
    float tx, ty, tz;
};

// Cube with per-face UVs and tangents for normal mapping.
const Vertex kCubeVertices[] = {
    // -Z
    {-0.5f, -0.5f, -0.5f, 0, 0, -1, 0, 0, 1, 0, 0},
    {0.5f, 0.5f, -0.5f, 0, 0, -1, 1, 1, 1, 0, 0},
    {0.5f, -0.5f, -0.5f, 0, 0, -1, 1, 0, 1, 0, 0},
    {-0.5f, -0.5f, -0.5f, 0, 0, -1, 0, 0, 1, 0, 0},
    {-0.5f, 0.5f, -0.5f, 0, 0, -1, 0, 1, 1, 0, 0},
    {0.5f, 0.5f, -0.5f, 0, 0, -1, 1, 1, 1, 0, 0},

    // +Z
    {-0.5f, -0.5f, 0.5f, 0, 0, 1, 0, 0, -1, 0, 0},
    {0.5f, -0.5f, 0.5f, 0, 0, 1, 1, 0, -1, 0, 0},
    {0.5f, 0.5f, 0.5f, 0, 0, 1, 1, 1, -1, 0, 0},
    {-0.5f, -0.5f, 0.5f, 0, 0, 1, 0, 0, -1, 0, 0},
    {0.5f, 0.5f, 0.5f, 0, 0, 1, 1, 1, -1, 0, 0},
    {-0.5f, 0.5f, 0.5f, 0, 0, 1, 0, 1, -1, 0, 0},

    // -Y floor
    {-0.5f, -0.5f, -0.5f, 0, -1, 0, 0, 0, 1, 0, 0},
    {0.5f, -0.5f, -0.5f, 0, -1, 0, 1, 0, 1, 0, 0},
    {0.5f, -0.5f, 0.5f, 0, -1, 0, 1, 1, 1, 0, 0},
    {-0.5f, -0.5f, -0.5f, 0, -1, 0, 0, 0, 1, 0, 0},
    {0.5f, -0.5f, 0.5f, 0, -1, 0, 1, 1, 1, 0, 0},
    {-0.5f, -0.5f, 0.5f, 0, -1, 0, 0, 1, 1, 0, 0},

    // +Y
    {-0.5f, 0.5f, -0.5f, 0, 1, 0, 0, 0, 1, 0, 0},
    {0.5f, 0.5f, 0.5f, 0, 1, 0, 1, 1, 1, 0, 0},
    {0.5f, 0.5f, -0.5f, 0, 1, 0, 1, 0, 1, 0, 0},
    {-0.5f, 0.5f, -0.5f, 0, 1, 0, 0, 0, 1, 0, 0},
    {-0.5f, 0.5f, 0.5f, 0, 1, 0, 0, 1, 1, 0, 0},
    {0.5f, 0.5f, 0.5f, 0, 1, 0, 1, 1, 1, 0, 0},

    // +X
    {0.5f, -0.5f, -0.5f, 1, 0, 0, 0, 0, 0, 0, 1},
    {0.5f, 0.5f, -0.5f, 1, 0, 0, 0, 1, 0, 0, 1},
    {0.5f, 0.5f, 0.5f, 1, 0, 0, 1, 1, 0, 0, 1},
    {0.5f, -0.5f, -0.5f, 1, 0, 0, 0, 0, 0, 0, 1},
    {0.5f, 0.5f, 0.5f, 1, 0, 0, 1, 1, 0, 0, 1},
    {0.5f, -0.5f, 0.5f, 1, 0, 0, 1, 0, 0, 0, 1},

    // -X
    {-0.5f, -0.5f, -0.5f, -1, 0, 0, 1, 0, 0, 0, -1},
    {-0.5f, 0.5f, 0.5f, -1, 0, 0, 0, 1, 0, 0, -1},
    {-0.5f, 0.5f, -0.5f, -1, 0, 0, 1, 1, 0, 0, -1},
    {-0.5f, -0.5f, -0.5f, -1, 0, 0, 1, 0, 0, 0, -1},
    {-0.5f, -0.5f, 0.5f, -1, 0, 0, 0, 0, 0, 0, -1},
    {-0.5f, 0.5f, 0.5f, -1, 0, 0, 0, 1, 0, 0, -1},
};

using GLsizeiptr = ptrdiff_t;
using GLchar = char;

#define DECLARE_GL_FUNCTION(name) using name##Proc = void(*)();
#define LOAD_GL_TYPED(name, signature) \
    using name##Proc = signature; \
    name##Proc p##name = nullptr;

LOAD_GL_TYPED(glGenBuffers, void(APIENTRY*)(GLsizei, GLuint*))
LOAD_GL_TYPED(glBindBuffer, void(APIENTRY*)(GLenum, GLuint))
LOAD_GL_TYPED(glBufferData, void(APIENTRY*)(GLenum, GLsizeiptr, const void*, GLenum))
LOAD_GL_TYPED(glCreateShader, GLuint(APIENTRY*)(GLenum))
LOAD_GL_TYPED(glShaderSource, void(APIENTRY*)(GLuint, GLsizei, const GLchar**, const GLint*))
LOAD_GL_TYPED(glCompileShader, void(APIENTRY*)(GLuint))
LOAD_GL_TYPED(glGetShaderiv, void(APIENTRY*)(GLuint, GLenum, GLint*))
LOAD_GL_TYPED(glGetShaderInfoLog, void(APIENTRY*)(GLuint, GLsizei, GLsizei*, GLchar*))
LOAD_GL_TYPED(glCreateProgram, GLuint(APIENTRY*)())
LOAD_GL_TYPED(glAttachShader, void(APIENTRY*)(GLuint, GLuint))
LOAD_GL_TYPED(glLinkProgram, void(APIENTRY*)(GLuint))
LOAD_GL_TYPED(glGetProgramiv, void(APIENTRY*)(GLuint, GLenum, GLint*))
LOAD_GL_TYPED(glGetProgramInfoLog, void(APIENTRY*)(GLuint, GLsizei, GLsizei*, GLchar*))
LOAD_GL_TYPED(glUseProgram, void(APIENTRY*)(GLuint))
LOAD_GL_TYPED(glGetAttribLocation, GLint(APIENTRY*)(GLuint, const GLchar*))
LOAD_GL_TYPED(glGetUniformLocation, GLint(APIENTRY*)(GLuint, const GLchar*))
LOAD_GL_TYPED(glEnableVertexAttribArray, void(APIENTRY*)(GLuint))
LOAD_GL_TYPED(glVertexAttribPointer, void(APIENTRY*)(GLuint, GLint, GLenum, GLboolean, GLsizei, const void*))
LOAD_GL_TYPED(glUniformMatrix4fv, void(APIENTRY*)(GLint, GLsizei, GLboolean, const GLfloat*))
LOAD_GL_TYPED(glUniform3f, void(APIENTRY*)(GLint, GLfloat, GLfloat, GLfloat))
LOAD_GL_TYPED(glUniform1f, void(APIENTRY*)(GLint, GLfloat))
LOAD_GL_TYPED(glUniform1i, void(APIENTRY*)(GLint, GLint))
LOAD_GL_TYPED(glActiveTexture, void(APIENTRY*)(GLenum))
LOAD_GL_TYPED(glUniformMatrix3fv, void(APIENTRY*)(GLint, GLsizei, GLboolean, const GLfloat*))

lantern::GameState g_game;
lantern::AudioEngine g_audio;
lantern::FontRenderer g_font;
lantern::HudRenderer g_hud;
lantern::MenuRenderer g_menu;

HDC g_device_context = nullptr;
HGLRC g_render_context = nullptr;
int g_width = 1280;
int g_height = 720;

GLuint g_program = 0;
GLuint g_vertex_buffer = 0;

GLuint g_floor_albedo = 0;
GLuint g_floor_normal = 0;
GLuint g_wall_albedo = 0;
GLuint g_wall_normal = 0;
GLuint g_bug_albedo = 0;
GLuint g_bug_normal = 0;
GLuint g_water_albedo = 0;
GLuint g_water_normal = 0;

bool g_keys[256]{};
bool g_mouse_captured = true;
int g_last_mouse_x = 0;
int g_last_mouse_y = 0;
bool g_shoot_pressed = false;
bool g_moved_this_frame = false;

std::string g_asset_root;

std::string join_path(const std::string& a, const std::string& b) {
    if (a.empty()) {
        return b;
    }
    if (a.back() == '/' || a.back() == '\\') {
        return a + b;
    }
    return a + "/" + b;
}

void* get_gl_symbol(const char* name) {
    void* symbol = reinterpret_cast<void*>(wglGetProcAddress(name));
    if (symbol == nullptr || symbol == reinterpret_cast<void*>(1) || symbol == reinterpret_cast<void*>(2) ||
        symbol == reinterpret_cast<void*>(3) || symbol == reinterpret_cast<void*>(-1)) {
        static HMODULE opengl_module = LoadLibraryA("opengl32.dll");
        symbol = reinterpret_cast<void*>(GetProcAddress(opengl_module, name));
    }
    return symbol;
}

bool load_gl_functions() {
#define LOAD(name) \
    p##name = reinterpret_cast<name##Proc>(get_gl_symbol(#name)); \
    if (p##name == nullptr) { \
        return false; \
    }

    LOAD(glGenBuffers);
    LOAD(glBindBuffer);
    LOAD(glBufferData);
    LOAD(glCreateShader);
    LOAD(glShaderSource);
    LOAD(glCompileShader);
    LOAD(glGetShaderiv);
    LOAD(glGetShaderInfoLog);
    LOAD(glCreateProgram);
    LOAD(glAttachShader);
    LOAD(glLinkProgram);
    LOAD(glGetProgramiv);
    LOAD(glGetProgramInfoLog);
    LOAD(glUseProgram);
    LOAD(glGetAttribLocation);
    LOAD(glGetUniformLocation);
    LOAD(glEnableVertexAttribArray);
    LOAD(glVertexAttribPointer);
    LOAD(glUniformMatrix4fv);
    LOAD(glUniform3f);
    LOAD(glUniform1f);
    LOAD(glUniform1i);
    LOAD(glActiveTexture);
    LOAD(glUniformMatrix3fv);
    return true;
#undef LOAD
}

std::string read_text_file(const std::string& path) {
    std::ifstream file(path, std::ios::binary);
    if (!file) {
        return {};
    }
    std::ostringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

GLuint compile_shader(GLenum type, const std::string& source) {
    const char* src = source.c_str();
    const GLuint shader = pglCreateShader(type);
    pglShaderSource(shader, 1, &src, nullptr);
    pglCompileShader(shader);

    GLint compiled = GL_FALSE;
    pglGetShaderiv(shader, GL_COMPILE_STATUS, &compiled);
    if (compiled == GL_FALSE) {
        char log[2048]{};
        pglGetShaderInfoLog(shader, sizeof(log), nullptr, log);
        MessageBoxA(nullptr, log, "Shader compile error", MB_ICONERROR);
        return 0;
    }
    return shader;
}

bool initialize_program() {
#ifdef LANTERN_SHADER_DIR
    const std::string vert_src = read_text_file(join_path(LANTERN_SHADER_DIR, "scene.vert.glsl"));
    const std::string frag_src = read_text_file(join_path(LANTERN_SHADER_DIR, "scene.frag.glsl"));
#else
    const std::string vert_src = read_text_file("src/shaders/scene.vert.glsl");
    const std::string frag_src = read_text_file("src/shaders/scene.frag.glsl");
#endif

    const std::string& vert = vert_src;
    const std::string& frag = frag_src;

    if (vert.empty() || frag.empty()) {
        MessageBoxA(nullptr, "Shader files not found.", "Error", MB_ICONERROR);
        return false;
    }

    const GLuint vertex_shader = compile_shader(GL_VERTEX_SHADER, vert);
    const GLuint fragment_shader = compile_shader(GL_FRAGMENT_SHADER, frag);
    if (vertex_shader == 0 || fragment_shader == 0) {
        return false;
    }

    g_program = pglCreateProgram();
    pglAttachShader(g_program, vertex_shader);
    pglAttachShader(g_program, fragment_shader);
    pglLinkProgram(g_program);

    GLint linked = GL_FALSE;
    pglGetProgramiv(g_program, GL_LINK_STATUS, &linked);
    if (linked == GL_FALSE) {
        char log[2048]{};
        pglGetProgramInfoLog(g_program, sizeof(log), nullptr, log);
        MessageBoxA(nullptr, log, "Program link error", MB_ICONERROR);
        return false;
    }

    pglGenBuffers(1, &g_vertex_buffer);
    pglBindBuffer(GL_ARRAY_BUFFER, g_vertex_buffer);
    pglBufferData(GL_ARRAY_BUFFER, sizeof(kCubeVertices), kCubeVertices, GL_STATIC_DRAW);
    return true;
}

bool initialize_wgl(HWND window) {
    g_device_context = GetDC(window);
    if (g_device_context == nullptr) {
        return false;
    }

    PIXELFORMATDESCRIPTOR descriptor{};
    descriptor.nSize = sizeof(descriptor);
    descriptor.nVersion = 1;
    descriptor.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER;
    descriptor.iPixelType = PFD_TYPE_RGBA;
    descriptor.cColorBits = 32;
    descriptor.cDepthBits = 24;
    descriptor.iLayerType = PFD_MAIN_PLANE;

    const int pixel_format = ChoosePixelFormat(g_device_context, &descriptor);
    if (pixel_format == 0 || SetPixelFormat(g_device_context, pixel_format, &descriptor) == FALSE) {
        return false;
    }

    g_render_context = wglCreateContext(g_device_context);
    if (g_render_context == nullptr) {
        return false;
    }

    return wglMakeCurrent(g_device_context, g_render_context) == TRUE;
}

bool load_textures() {
    const std::string tex_root = join_path(g_asset_root, "textures");
    g_floor_albedo = lantern::load_texture_2d(join_path(tex_root, "floor_albedo.png"));
    g_floor_normal = lantern::load_texture_2d(join_path(tex_root, "floor_nrm.png"));
    g_wall_albedo = lantern::load_texture_2d(join_path(tex_root, "wall_albedo.png"));
    g_wall_normal = lantern::load_texture_2d(join_path(tex_root, "wall_nrm.png"));
    g_bug_albedo = lantern::load_texture_2d(join_path(tex_root, "bug_albedo.png"));
    g_bug_normal = lantern::load_texture_2d(join_path(tex_root, "bug_nrm.png"));
    g_water_albedo = lantern::load_texture_2d(join_path(tex_root, "water_albedo.png"));
    g_water_normal = lantern::load_texture_2d(join_path(tex_root, "water_nrm.png"));

    return g_floor_albedo && g_floor_normal && g_wall_albedo && g_wall_normal && g_bug_albedo && g_bug_normal &&
           g_water_albedo && g_water_normal;
}

void bind_material(lantern::SurfaceKind surface) {
    GLuint albedo = g_wall_albedo;
    GLuint normal = g_wall_normal;

    switch (surface) {
    case lantern::SurfaceKind::Floor:
        albedo = g_floor_albedo;
        normal = g_floor_normal;
        break;
    case lantern::SurfaceKind::Bug:
        albedo = g_bug_albedo;
        normal = g_bug_normal;
        break;
    case lantern::SurfaceKind::Food:
        albedo = g_bug_albedo;
        normal = g_bug_normal;
        break;
    case lantern::SurfaceKind::Water:
        albedo = g_water_albedo;
        normal = g_water_normal;
        break;
    case lantern::SurfaceKind::Slime:
        albedo = g_bug_albedo;
        normal = g_bug_normal;
        break;
    case lantern::SurfaceKind::Altar:
        albedo = g_floor_albedo;
        normal = g_floor_normal;
        break;
    case lantern::SurfaceKind::Wall:
    default:
        break;
    }

    pglActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, albedo);
    pglActiveTexture(GL_TEXTURE1);
    glBindTexture(GL_TEXTURE_2D, normal);
}

void render_scene(HWND window) {
    glViewport(0, 0, g_width, g_height);
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.01f, 0.01f, 0.02f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    if (g_game.screen == lantern::GameScreen::MainMenu) {
        g_menu.draw_main_menu(g_game, g_font, g_width, g_height);
        SwapBuffers(g_device_context);
        return;
    }

    if (g_game.screen == lantern::GameScreen::Paused) {
        // still draw world dimly optional - skip for clarity
        g_menu.draw_paused(g_font, g_width, g_height);
        SwapBuffers(g_device_context);
        return;
    }

    if (g_game.screen == lantern::GameScreen::GameOver || g_game.screen == lantern::GameScreen::Victory) {
        g_menu.draw_game_over(g_game.screen == lantern::GameScreen::Victory, g_font, g_width, g_height);
        SwapBuffers(g_device_context);
        return;
    }

    const float aspect = static_cast<float>(g_width) / static_cast<float>(std::max(1, g_height));
    const lantern::Mat4 projection =
        lantern::perspective(70.0f * kPi / 180.0f, aspect, 0.05f, 200.0f);
    const lantern::Mat4 view = g_game.camera.view_matrix();
    const lantern::Mat4 view_projection = projection * view;

    pglUseProgram(g_program);
    pglBindBuffer(GL_ARRAY_BUFFER, g_vertex_buffer);

    const GLint pos_attr = pglGetAttribLocation(g_program, "a_pos");
    const GLint normal_attr = pglGetAttribLocation(g_program, "a_normal");
    const GLint uv_attr = pglGetAttribLocation(g_program, "a_uv");
    const GLint tangent_attr = pglGetAttribLocation(g_program, "a_tangent");

    pglEnableVertexAttribArray(pos_attr);
    pglEnableVertexAttribArray(normal_attr);
    pglEnableVertexAttribArray(uv_attr);
    pglEnableVertexAttribArray(tangent_attr);

    const GLsizei stride = static_cast<GLsizei>(sizeof(Vertex));
    pglVertexAttribPointer(pos_attr, 3, GL_FLOAT, GL_FALSE, stride, reinterpret_cast<void*>(offsetof(Vertex, px)));
    pglVertexAttribPointer(
        normal_attr, 3, GL_FLOAT, GL_FALSE, stride, reinterpret_cast<void*>(offsetof(Vertex, nx)));
    pglVertexAttribPointer(uv_attr, 2, GL_FLOAT, GL_FALSE, stride, reinterpret_cast<void*>(offsetof(Vertex, u)));
    pglVertexAttribPointer(
        tangent_attr, 3, GL_FLOAT, GL_FALSE, stride, reinterpret_cast<void*>(offsetof(Vertex, tx)));

    const GLint mvp_uniform = pglGetUniformLocation(g_program, "u_mvp");
    const GLint model_uniform = pglGetUniformLocation(g_program, "u_model");
    const GLint albedo_uniform = pglGetUniformLocation(g_program, "u_albedo");
    const GLint normal_uniform = pglGetUniformLocation(g_program, "u_normal_map");
    const GLint light_pos_uniform = pglGetUniformLocation(g_program, "u_light_pos");
    const GLint light_dir_uniform = pglGetUniformLocation(g_program, "u_light_dir");
    const GLint light_color_uniform = pglGetUniformLocation(g_program, "u_light_color");
    const GLint view_pos_uniform = pglGetUniformLocation(g_program, "u_view_pos");
    const GLint ambient_uniform = pglGetUniformLocation(g_program, "u_ambient");
    const GLint cutoff_uniform = pglGetUniformLocation(g_program, "u_spot_cutoff");
    const GLint exponent_uniform = pglGetUniformLocation(g_program, "u_spot_exponent");
    const GLint emissive_uniform = pglGetUniformLocation(g_program, "u_emissive");

    // LANTERN-LIGHT-04: lanterna estreita + ambiente escuro.
    const lantern::Vec3 light_pos = g_game.camera.position;
    const lantern::Vec3 light_dir = g_game.camera.forward();
    pglUniform3f(light_pos_uniform, light_pos.x, light_pos.y, light_pos.z);
    pglUniform3f(light_dir_uniform, light_dir.x, light_dir.y, light_dir.z);
    pglUniform3f(light_color_uniform, 1.0f, 0.92f, 0.72f);
    pglUniform3f(view_pos_uniform, g_game.camera.position.x, g_game.camera.position.y, g_game.camera.position.z);
    pglUniform1f(ambient_uniform, 0.03f);
    pglUniform1f(cutoff_uniform, 0.92f);
    pglUniform1f(exponent_uniform, 48.0f);

    pglUniform1i(albedo_uniform, 0);
    pglUniform1i(normal_uniform, 1);

    for (const lantern::DrawCommand& command : lantern::build_draw_list(g_game)) {
        const lantern::Mat4 mvp = view_projection * command.model;
        pglUniformMatrix4fv(mvp_uniform, 1, GL_FALSE, mvp.m);
        pglUniformMatrix4fv(model_uniform, 1, GL_FALSE, command.model.m);
        pglUniform1i(emissive_uniform, command.emissive ? 1 : 0);
        bind_material(command.surface);
        glDrawArrays(GL_TRIANGLES, 0, 36);
    }

    pglUseProgram(0);
    lantern::draw_slime_overlay(g_game.slime_overlay);
    g_hud.draw(g_game, g_font, g_width, g_height);

    if (g_game.won) {
        SetWindowTextA(window, "Lantern Hunt - VITORIA!");
    }

    SwapBuffers(g_device_context);
}

void capture_mouse(HWND window, bool capture) {
    g_mouse_captured = capture;
    if (capture) {
        RECT rect;
        GetClientRect(window, &rect);
        POINT center{rect.right / 2, rect.bottom / 2};
        ClientToScreen(window, &center);
        SetCursorPos(center.x, center.y);
        ShowCursor(FALSE);
        g_last_mouse_x = center.x;
        g_last_mouse_y = center.y;
    } else {
        ShowCursor(TRUE);
    }
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
    case WM_SIZE:
        g_width = std::max(1, static_cast<int>(LOWORD(lparam)));
        g_height = std::max(1, static_cast<int>(HIWORD(lparam)));
        return 0;

    case WM_KEYDOWN:
        g_keys[wparam & 0xFF] = true;
        if (wparam == VK_ESCAPE) {
            if (g_game.screen == lantern::GameScreen::Playing) {
                g_game.screen = lantern::GameScreen::Paused;
                capture_mouse(window, false);
            } else if (g_game.screen == lantern::GameScreen::Paused) {
                g_game.screen = lantern::GameScreen::Playing;
                capture_mouse(window, true);
            } else {
                g_game.quit_requested = true;
                PostQuitMessage(0);
            }
            return 0;
        }
        if (wparam == VK_RETURN) {
            if (g_game.screen == lantern::GameScreen::MainMenu) {
                if (g_game.menu_selection == 0) {
                    lantern::game_reset(g_game, 42u);
                    capture_mouse(window, true);
                } else if (g_game.menu_selection == 1) {
                    const auto seed = static_cast<std::uint32_t>(
                        std::chrono::steady_clock::now().time_since_epoch().count());
                    lantern::game_reset(g_game, seed);
                    capture_mouse(window, true);
                } else {
                    g_game.quit_requested = true;
                    PostQuitMessage(0);
                }
            } else if (g_game.screen == lantern::GameScreen::GameOver || g_game.screen == lantern::GameScreen::Victory) {
                g_game.screen = lantern::GameScreen::MainMenu;
                g_game.menu_selection = 0;
                capture_mouse(window, false);
            }
            return 0;
        }
        if (wparam == 'E') {
            g_game.interact_pressed = true;
            return 0;
        }
        if (wparam == 'R') {
            if (g_game.screen == lantern::GameScreen::Playing) {
                lantern::game_respawn_to_checkpoint(g_game);
            }
            return 0;
        }
        if (g_game.screen == lantern::GameScreen::MainMenu) {
            if (wparam == VK_UP || wparam == 'W') {
                g_game.menu_selection = (g_game.menu_selection + 2) % 3;
            }
            if (wparam == VK_DOWN || wparam == 'S') {
                g_game.menu_selection = (g_game.menu_selection + 1) % 3;
            }
        }
        break;

    case WM_KEYUP:
        g_keys[wparam & 0xFF] = false;
        break;

    case WM_LBUTTONDOWN:
        g_shoot_pressed = true;
        g_audio.play_shoot();
        return 0;

    case WM_MOUSEMOVE:
        if (g_mouse_captured) {
            const int x = LOWORD(lparam);
            const int y = HIWORD(lparam);
            const float sensitivity = 0.0035f;
            g_game.camera.yaw += static_cast<float>(x - g_width / 2) * sensitivity;
            g_game.camera.pitch += static_cast<float>(y - g_height / 2) * sensitivity;
            g_game.camera.pitch = std::max(-1.45f, std::min(1.45f, g_game.camera.pitch));

            POINT center{g_width / 2, g_height / 2};
            ClientToScreen(window, &center);
            SetCursorPos(center.x, center.y);
        }
        return 0;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    default:
        break;
    }

    return DefWindowProcA(window, message, wparam, lparam);
}

} // namespace

int WINAPI WinMain(HINSTANCE instance, HINSTANCE, LPSTR, int) {
#ifdef LANTERN_ASSET_ROOT
    g_asset_root = LANTERN_ASSET_ROOT;
#else
    g_asset_root = "assets";
#endif

    WNDCLASSA window_class{};
    window_class.lpfnWndProc = window_proc;
    window_class.hInstance = instance;
    window_class.lpszClassName = "ChrisLanternHunt";
    window_class.hCursor = LoadCursorA(nullptr, IDC_ARROW);
    window_class.style = CS_OWNDC;

    if (RegisterClassA(&window_class) == 0) {
        MessageBoxA(nullptr, "RegisterClassA failed.", "Error", MB_ICONERROR);
        return 1;
    }

    HWND window = CreateWindowExA(
        0,
        window_class.lpszClassName,
        "Lantern Hunt - Chris Low-Level Graphics",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        g_width,
        g_height,
        nullptr,
        nullptr,
        instance,
        nullptr);

    if (window == nullptr) {
        return 2;
    }

    if (!initialize_wgl(window) || !load_gl_functions() || !initialize_program() || !load_textures()) {
        MessageBoxA(window, "Graphics init failed.", "Error", MB_ICONERROR);
        return 3;
    }

    const std::string audio_root = join_path(g_asset_root, "audio");
    g_audio.initialize(
        join_path(audio_root, "ambient_dark.wav"),
        join_path(audio_root, "footstep.wav"),
        join_path(audio_root, "shoot_marble.wav"));
    g_font.initialize();

    g_game.screen = lantern::GameScreen::MainMenu;
    g_game.menu_selection = 0;
    capture_mouse(window, false);

    auto previous_time = std::chrono::steady_clock::now();
    MSG message{};
    bool running = true;

    while (running) {
        while (PeekMessageA(&message, nullptr, 0, 0, PM_REMOVE)) {
            if (message.message == WM_QUIT) {
                running = false;
                break;
            }
            TranslateMessage(&message);
            DispatchMessageA(&message);
        }

        const auto now = std::chrono::steady_clock::now();
        const float delta = static_cast<float>(std::chrono::duration<double>(now - previous_time).count());
        previous_time = now;

        const bool move_forward = g_keys['W'] || g_keys[VK_UP];
        const bool move_back = g_keys['S'] || g_keys[VK_DOWN];
        const bool move_left = g_keys['A'] || g_keys[VK_LEFT];
        const bool move_right = g_keys['D'] || g_keys[VK_RIGHT];

        if (g_game.screen == lantern::GameScreen::Playing) {
            g_moved_this_frame = move_forward || move_back || move_left || move_right;
            if (g_moved_this_frame) {
                g_audio.play_footstep();
            }

            lantern::game_update(g_game, std::min(delta, 0.05f), move_forward, move_back, move_left, move_right,
                g_shoot_pressed);
            g_shoot_pressed = false;
            g_audio.update_movement_cooldown(delta);
        }

        render_scene(window);
        Sleep(1);
    }

    g_audio.shutdown();

    wglMakeCurrent(nullptr, nullptr);
    if (g_render_context != nullptr) {
        wglDeleteContext(g_render_context);
    }
    if (g_device_context != nullptr) {
        ReleaseDC(window, g_device_context);
    }

    return 0;
}
