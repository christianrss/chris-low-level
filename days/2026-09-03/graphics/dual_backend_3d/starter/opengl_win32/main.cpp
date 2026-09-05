#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <GL/gl.h>

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cmath>

#include "../common/engine.hpp"

using namespace lab3d;

#ifndef GL_ARRAY_BUFFER
#define GL_ARRAY_BUFFER 0x8892
#define GL_STATIC_DRAW 0x88E4
#define GL_VERTEX_SHADER 0x8B31
#define GL_FRAGMENT_SHADER 0x8B30
#define GL_COMPILE_STATUS 0x8B81
#define GL_LINK_STATUS 0x8B82
#endif

using GLsizeiptr = std::ptrdiff_t;
using GLchar = char;

#define DECLARE_GL_FUNCTION(return_type, name, arguments) \
    using name##Proc = return_type(APIENTRY*) arguments;   \
    static name##Proc p##name = nullptr

DECLARE_GL_FUNCTION(void, glGenBuffers, (GLsizei, GLuint*));
DECLARE_GL_FUNCTION(void, glBindBuffer, (GLenum, GLuint));
DECLARE_GL_FUNCTION(void, glBufferData, (GLenum, GLsizeiptr, const void*, GLenum));
DECLARE_GL_FUNCTION(GLuint, glCreateShader, (GLenum));
DECLARE_GL_FUNCTION(void, glShaderSource, (GLuint, GLsizei, const GLchar* const*, const GLint*));
DECLARE_GL_FUNCTION(void, glCompileShader, (GLuint));
DECLARE_GL_FUNCTION(void, glGetShaderiv, (GLuint, GLenum, GLint*));
DECLARE_GL_FUNCTION(void, glGetShaderInfoLog, (GLuint, GLsizei, GLsizei*, GLchar*));
DECLARE_GL_FUNCTION(GLuint, glCreateProgram, (void));
DECLARE_GL_FUNCTION(void, glAttachShader, (GLuint, GLuint));
DECLARE_GL_FUNCTION(void, glLinkProgram, (GLuint));
DECLARE_GL_FUNCTION(void, glGetProgramiv, (GLuint, GLenum, GLint*));
DECLARE_GL_FUNCTION(void, glGetProgramInfoLog, (GLuint, GLsizei, GLsizei*, GLchar*));
DECLARE_GL_FUNCTION(void, glUseProgram, (GLuint));
DECLARE_GL_FUNCTION(GLint, glGetAttribLocation, (GLuint, const GLchar*));
DECLARE_GL_FUNCTION(GLint, glGetUniformLocation, (GLuint, const GLchar*));
DECLARE_GL_FUNCTION(void, glEnableVertexAttribArray, (GLuint));
DECLARE_GL_FUNCTION(
    void,
    glVertexAttribPointer,
    (GLuint, GLint, GLenum, GLboolean, GLsizei, const void*));
DECLARE_GL_FUNCTION(void, glUniformMatrix4fv, (GLint, GLsizei, GLboolean, const GLfloat*));
DECLARE_GL_FUNCTION(void, glUniform3f, (GLint, GLfloat, GLfloat, GLfloat));
DECLARE_GL_FUNCTION(void, glUniform1f, (GLint, GLfloat));

#undef DECLARE_GL_FUNCTION

namespace {

struct Vertex {
    float px;
    float py;
    float pz;
    float nx;
    float ny;
    float nz;
};

constexpr Vertex kCube[] = {
    // -Z
    {-0.5f, -0.5f, -0.5f,  0.0f,  0.0f, -1.0f},
    { 0.5f,  0.5f, -0.5f,  0.0f,  0.0f, -1.0f},
    { 0.5f, -0.5f, -0.5f,  0.0f,  0.0f, -1.0f},
    {-0.5f, -0.5f, -0.5f,  0.0f,  0.0f, -1.0f},
    {-0.5f,  0.5f, -0.5f,  0.0f,  0.0f, -1.0f},
    { 0.5f,  0.5f, -0.5f,  0.0f,  0.0f, -1.0f},

    // +Z
    {-0.5f, -0.5f,  0.5f,  0.0f,  0.0f,  1.0f},
    { 0.5f, -0.5f,  0.5f,  0.0f,  0.0f,  1.0f},
    { 0.5f,  0.5f,  0.5f,  0.0f,  0.0f,  1.0f},
    {-0.5f, -0.5f,  0.5f,  0.0f,  0.0f,  1.0f},
    { 0.5f,  0.5f,  0.5f,  0.0f,  0.0f,  1.0f},
    {-0.5f,  0.5f,  0.5f,  0.0f,  0.0f,  1.0f},

    // -Y
    {-0.5f, -0.5f, -0.5f,  0.0f, -1.0f,  0.0f},
    { 0.5f, -0.5f, -0.5f,  0.0f, -1.0f,  0.0f},
    { 0.5f, -0.5f,  0.5f,  0.0f, -1.0f,  0.0f},
    {-0.5f, -0.5f, -0.5f,  0.0f, -1.0f,  0.0f},
    { 0.5f, -0.5f,  0.5f,  0.0f, -1.0f,  0.0f},
    {-0.5f, -0.5f,  0.5f,  0.0f, -1.0f,  0.0f},

    // +Y
    {-0.5f,  0.5f, -0.5f,  0.0f,  1.0f,  0.0f},
    { 0.5f,  0.5f,  0.5f,  0.0f,  1.0f,  0.0f},
    { 0.5f,  0.5f, -0.5f,  0.0f,  1.0f,  0.0f},
    {-0.5f,  0.5f, -0.5f,  0.0f,  1.0f,  0.0f},
    {-0.5f,  0.5f,  0.5f,  0.0f,  1.0f,  0.0f},
    { 0.5f,  0.5f,  0.5f,  0.0f,  1.0f,  0.0f},

    // +X
    { 0.5f, -0.5f, -0.5f,  1.0f,  0.0f,  0.0f},
    { 0.5f,  0.5f, -0.5f,  1.0f,  0.0f,  0.0f},
    { 0.5f,  0.5f,  0.5f,  1.0f,  0.0f,  0.0f},
    { 0.5f, -0.5f, -0.5f,  1.0f,  0.0f,  0.0f},
    { 0.5f,  0.5f,  0.5f,  1.0f,  0.0f,  0.0f},
    { 0.5f, -0.5f,  0.5f,  1.0f,  0.0f,  0.0f},

    // -X
    {-0.5f, -0.5f, -0.5f, -1.0f,  0.0f,  0.0f},
    {-0.5f,  0.5f,  0.5f, -1.0f,  0.0f,  0.0f},
    {-0.5f,  0.5f, -0.5f, -1.0f,  0.0f,  0.0f},
    {-0.5f, -0.5f, -0.5f, -1.0f,  0.0f,  0.0f},
    {-0.5f, -0.5f,  0.5f, -1.0f,  0.0f,  0.0f},
    {-0.5f,  0.5f,  0.5f, -1.0f,  0.0f,  0.0f},
};

SceneState g_scene;
CameraState g_camera;
POINT g_last_mouse{};
bool g_have_last_mouse = false;
HDC g_device_context = nullptr;
HGLRC g_render_context = nullptr;
int g_width = 1100;
int g_height = 720;
float g_mouse_x = 550.0f;
float g_mouse_y = 360.0f;

GLuint g_program = 0;
GLuint g_vertex_buffer = 0;
GLint g_position_attribute = -1;
GLint g_normal_attribute = -1;
GLint g_mvp_uniform = -1;
GLint g_model_uniform = -1;
GLint g_color_uniform = -1;
GLint g_light_position_uniform = -1;
GLint g_light_direction_uniform = -1;
GLint g_inner_cutoff_uniform = -1;
GLint g_outer_cutoff_uniform = -1;

void* get_gl_symbol(const char* name) {
    void* symbol = reinterpret_cast<void*>(wglGetProcAddress(name));

    // wglGetProcAddress can return sentinel values for unsupported functions.
    if (symbol == nullptr ||
        symbol == reinterpret_cast<void*>(1) ||
        symbol == reinterpret_cast<void*>(2) ||
        symbol == reinterpret_cast<void*>(3) ||
        symbol == reinterpret_cast<void*>(-1)) {

        static HMODULE opengl_module = LoadLibraryA("opengl32.dll");
        symbol = reinterpret_cast<void*>(GetProcAddress(opengl_module, name));
    }

    return symbol;
}

#define LOAD_GL_FUNCTION(name)                                      \
    do {                                                            \
        p##name = reinterpret_cast<name##Proc>(get_gl_symbol(#name)); \
        if (p##name == nullptr) {                                   \
            return false;                                           \
        }                                                           \
    } while (false)

bool load_gl_functions() {
    LOAD_GL_FUNCTION(glGenBuffers);
    LOAD_GL_FUNCTION(glBindBuffer);
    LOAD_GL_FUNCTION(glBufferData);
    LOAD_GL_FUNCTION(glCreateShader);
    LOAD_GL_FUNCTION(glShaderSource);
    LOAD_GL_FUNCTION(glCompileShader);
    LOAD_GL_FUNCTION(glGetShaderiv);
    LOAD_GL_FUNCTION(glGetShaderInfoLog);
    LOAD_GL_FUNCTION(glCreateProgram);
    LOAD_GL_FUNCTION(glAttachShader);
    LOAD_GL_FUNCTION(glLinkProgram);
    LOAD_GL_FUNCTION(glGetProgramiv);
    LOAD_GL_FUNCTION(glGetProgramInfoLog);
    LOAD_GL_FUNCTION(glUseProgram);
    LOAD_GL_FUNCTION(glGetAttribLocation);
    LOAD_GL_FUNCTION(glGetUniformLocation);
    LOAD_GL_FUNCTION(glEnableVertexAttribArray);
    LOAD_GL_FUNCTION(glVertexAttribPointer);
    LOAD_GL_FUNCTION(glUniformMatrix4fv);
    LOAD_GL_FUNCTION(glUniform3f);
    LOAD_GL_FUNCTION(glUniform1f);

    return true;
}

#undef LOAD_GL_FUNCTION

struct Vec4f {
    float x;
    float y;
    float z;
    float w;
};

struct MouseRay {
    Vec3 origin{};
    Vec3 direction{};
    bool valid = false;
};

Vec4f multiply_mat4_vec4(const Mat4& matrix, const Vec4f& v) {
    return {
        matrix.m[0]  * v.x + matrix.m[4]  * v.y +
        matrix.m[8]  * v.z + matrix.m[12] * v.w,

        matrix.m[1]  * v.x + matrix.m[5]  * v.y +
        matrix.m[9]  * v.z + matrix.m[13] * v.w,

        matrix.m[2]  * v.x + matrix.m[6]  * v.y +
        matrix.m[10] * v.z + matrix.m[14] * v.w,

        matrix.m[3]  * v.x + matrix.m[7]  * v.y +
        matrix.m[11] * v.z + matrix.m[15] * v.w
    };
}

Vec3 normalize_vec3(const Vec3& v) {
    const float length_sq =
        v.x * v.x + v.y * v.y + v.z * v.z;

    if (length_sq <= 1.0e-12f) {
        return {0.0f, 0.0f, -1.0f};
    }

    const float inv_length =
        1.0f / std::sqrt(length_sq);

    return {
        v.x * inv_length,
        v.y * inv_length,
        v.z * inv_length
    };
}

bool invert_mat4(const Mat4& input, Mat4& output) {
    // Gauss-Jordan aplicado a [M | I].
    float a[4][8]{};

    // Mat4::m -> matriz convencional [row][col].
    for (int row = 0; row < 4; ++row) {
        for (int col = 0; col < 4; ++col) {
            a[row][col] = input.m[col * 4 + row];
            a[row][4 + col] =
                (row == col) ? 1.0f : 0.0f;
        }
    }

    for (int col = 0; col < 4; ++col) {
        int pivot_row = col;
        float pivot_abs = std::fabs(a[pivot_row][col]);

        for (int row = col + 1; row < 4; ++row) {
            const float candidate =
                std::fabs(a[row][col]);

            if (candidate > pivot_abs) {
                pivot_abs = candidate;
                pivot_row = row;
            }
        }

        if (pivot_abs <= 1.0e-8f) {
            return false;
        }

        if (pivot_row != col) {
            for (int k = 0; k < 8; ++k) {
                std::swap(a[col][k], a[pivot_row][k]);
            }
        }

        const float pivot = a[col][col];
        for (int k = 0; k < 8; ++k) {
            a[col][k] /= pivot;
        }

        for (int row = 0; row < 4; ++row) {
            if (row == col) {
                continue;
            }

            const float factor = a[row][col];
            for (int k = 0; k < 8; ++k) {
                a[row][k] -= factor * a[col][k];
            }
        }
    }

    // Parte direita da matriz aumentada -> output.
    for (int row = 0; row < 4; ++row) {
        for (int col = 0; col < 4; ++col) {
            output.m[col * 4 + row] =
                a[row][4 + col];
        }
    }

    return true;
}

MouseRay build_mouse_ray(
    float mouse_x,
    float mouse_y,
    int width,
    int height,
    const Mat4& projection,
    const Mat4& view) {

    MouseRay result{};

    const float safe_width =
        static_cast<float>(std::max(1, width));
    const float safe_height =
        static_cast<float>(std::max(1, height));

    // PASSO 1: pixels -> NDC.
    const float ndc_x =
        (2.0f * mouse_x / safe_width) - 1.0f;

    // Windows: Y cresce para baixo.
    // NDC: Y cresce para cima.
    const float ndc_y =
        1.0f - (2.0f * mouse_y / safe_height);

    Mat4 inverse_projection{};
    Mat4 inverse_view{};

    if (!invert_mat4(projection, inverse_projection) ||
        !invert_mat4(view, inverse_view)) {
        return result;
    }

    // PASSO 2: ponto correspondente ao cursor em clip space.
    const Vec4f ray_clip{
        ndc_x,
        ndc_y,
        -1.0f,
        1.0f
    };

    // PASSO 3: desfaz a projeção.
    Vec4f ray_eye = multiply_mat4_vec4(
        inverse_projection,
        ray_clip);

    // Queremos uma DIREÇÃO, não uma posição.
    // w = 0 significa vetor/direção em coordenadas homogêneas.
    ray_eye.z = -1.0f;
    ray_eye.w = 0.0f;

    // PASSO 4: direção do view space para world space.
    const Vec4f ray_world4 = multiply_mat4_vec4(
        inverse_view,
        ray_eye);

    result.direction = normalize_vec3({
        ray_world4.x,
        ray_world4.y,
        ray_world4.z
    });

    // PASSO 5: origem do ray = câmera.
    // Em view space a câmera está em (0,0,0,1).
    Vec4f camera_world = multiply_mat4_vec4(
        inverse_view,
        {0.0f, 0.0f, 0.0f, 1.0f});

    if (std::fabs(camera_world.w) > 1.0e-8f) {
        camera_world.x /= camera_world.w;
        camera_world.y /= camera_world.w;
        camera_world.z /= camera_world.w;
    }

    result.origin = {
        camera_world.x,
        camera_world.y,
        camera_world.z
    };

    result.valid = true;
    return result;
}

GLuint compile_shader(GLenum type, const char* source) {
    const GLuint shader = pglCreateShader(type);
    pglShaderSource(shader, 1, &source, nullptr);
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
    const char* vertex_shader_source = R"GLSL(
#version 120
attribute vec3 a_pos;
attribute vec3 a_normal;
uniform mat4 u_mvp;
uniform mat4 u_model;
varying vec3 v_normal;
varying vec3 v_world_position;

void main() {
    vec4 world_position = 
        u_model * vec4(a_pos, 1.0);

    gl_Position = u_mvp * vec4(a_pos, 1.0);

    v_world_position = world_position.xyz;
    v_normal = mat3(u_model) * a_normal;
}
)GLSL";

    const char* fragment_shader_source = R"GLSL(
#version 120
uniform vec3 u_color;
uniform vec3 u_light_position;
uniform vec3 u_light_direction;
uniform float u_inner_cutoff;
uniform float u_outer_cutoff;

varying vec3 v_normal;
varying vec3 v_world_position;

void main() {
    // TODO [GFX-LAMBERT-01]: normalize normal, compute diffuse, add ambient.
    vec3 normal = normalize(v_normal);
    
    // Superficie -> luz: usado no Lambert.
    vec3 to_light =
        u_light_position - v_world_position;
    vec3 surface_to_light = normalize(to_light);
    float diffuse = max(
        dot(normal, surface_to_light),
        0.0f);
    // Luz -> fragmento: usado para saber se o fragmento
    // esta dentro do cone da lanterna
    vec3 light_to_fragment =
        normalize(v_world_position - u_light_position);
    float theta = dot(
        light_to_fragment,
        normalize(u_light_direction));

    float epsilon =
        u_inner_cutoff - u_outer_cutoff;
    float spot = clamp(
        (theta - u_outer_cutoff) / epsilon,
        0.0,
        1.0);

    float ambient = 0.08;
    float lighting = ambient + diffuse * spot;

    gl_FragColor = vec4(
        u_color * lighting,
        1.0);
}
)GLSL";

    const GLuint vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_source);
    const GLuint fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_source);

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

    g_position_attribute = pglGetAttribLocation(g_program, "a_pos");
    g_normal_attribute = pglGetAttribLocation(g_program, "a_normal");
    g_mvp_uniform = pglGetUniformLocation(g_program, "u_mvp");
    g_model_uniform = pglGetUniformLocation(g_program, "u_model");
    g_color_uniform = pglGetUniformLocation(g_program, "u_color");
    g_light_position_uniform = pglGetUniformLocation(g_program, "u_light_position");
    g_light_direction_uniform = pglGetUniformLocation(g_program, "u_light_direction");
    g_inner_cutoff_uniform = pglGetUniformLocation(g_program, "u_inner_cutoff");
    g_outer_cutoff_uniform = pglGetUniformLocation(g_program, "u_outer_cutoff");

    pglGenBuffers(1, &g_vertex_buffer);
    pglBindBuffer(GL_ARRAY_BUFFER, g_vertex_buffer);
    pglBufferData(GL_ARRAY_BUFFER, sizeof(kCube), kCube, GL_STATIC_DRAW);

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
    if (pixel_format == 0) {
        return false;
    }

    if (SetPixelFormat(g_device_context, pixel_format, &descriptor) == FALSE) {
        return false;
    }

    g_render_context = wglCreateContext(g_device_context);
    if (g_render_context == nullptr) {
        return false;
    }

    return wglMakeCurrent(g_device_context, g_render_context) == TRUE;
}

void update_camera_keyboard(float frame_dt) {
    // TODO [GFX-CAMERA-04]: same movement contract as software backend.
    (void)frame_dt;
}

void render_scene() {
    glViewport(0, 0, g_width, g_height);
    glEnable(GL_DEPTH_TEST);
    // TODO [GFX-CULL-03]: enable GL_CULL_FACE, cull back faces, select CCW.
    glClearColor(0.062f, 0.094f, 0.125f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    pglUseProgram(g_program);
    pglBindBuffer(GL_ARRAY_BUFFER, g_vertex_buffer);

    pglEnableVertexAttribArray(static_cast<GLuint>(g_position_attribute));
    pglEnableVertexAttribArray(static_cast<GLuint>(g_normal_attribute));

    pglVertexAttribPointer(
        static_cast<GLuint>(g_position_attribute),
        3,
        GL_FLOAT,
        GL_FALSE,
        sizeof(Vertex),
        reinterpret_cast<void*>(offsetof(Vertex, px)));

    pglVertexAttribPointer(
        static_cast<GLuint>(g_normal_attribute),
        3,
        GL_FLOAT,
        GL_FALSE,
        sizeof(Vertex),
        reinterpret_cast<void*>(offsetof(Vertex, nx)));

    const float aspect =
        static_cast<float>(g_width) /
        static_cast<float>(std::max(1, g_height));
    const Mat4 projection = projection_matrix(aspect);
    const Mat4 view = view_matrix(g_camera);
    const Mat4 view_projection = projection * view;

    const MouseRay mouse_ray = build_mouse_ray(
        g_mouse_x,
        g_mouse_y,
        g_width,
        g_height,
        projection,
        view);

    if (mouse_ray.valid) {
        pglUniform3f(
            g_light_direction_uniform,
            mouse_ray.direction.x,
            mouse_ray.direction.y,
            mouse_ray.direction.z);

        pglUniform3f(
            g_light_position_uniform,
            mouse_ray.origin.x,
            mouse_ray.origin.y,
            mouse_ray.origin.z);

        pglUniform1f(
            g_inner_cutoff_uniform,
            0.9781476f);
        pglUniform1f(
            g_outer_cutoff_uniform,
            0.9510565f);
    }

    for (const DrawItem& item : build_draw_list(g_scene)) {
        const Mat4 model_view_projection = view_projection * item.model;

        pglUniformMatrix4fv(
            g_mvp_uniform,
            1,
            GL_FALSE,
            model_view_projection.m.data());
        pglUniformMatrix4fv(
            g_model_uniform,
            1,
            GL_FALSE,
            item.model.m.data());
        pglUniform3f(
            g_color_uniform,
            item.color.x,
            item.color.y,
            item.color.z);

        glDrawArrays(GL_TRIANGLES, 0, 36);
    }

    SwapBuffers(g_device_context);
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
        case WM_SIZE:
            // Do not call OpenGL here: WM_SIZE can arrive before the WGL context
            // exists. render_scene() applies the viewport once the context is valid.
            g_width = std::max(1, static_cast<int>(LOWORD(lparam)));
            g_height = std::max(1, static_cast<int>(HIWORD(lparam)));
            return 0;

        case WM_KEYDOWN:
            if (wparam == VK_ESCAPE) {
                DestroyWindow(window);
                return 0;
            }

            if (wparam == 'R') {
                reset_scene(g_scene);
                g_camera = CameraState{};
                g_have_last_mouse = false;
                return 0;
            }

            if (wparam == 'P') {
                g_scene.paused = !g_scene.paused;
                return 0;
            }
            break;

        case WM_MOUSEMOVE:
        {
            // TODO [GFX-CAMERA-05]: same yaw/pitch update as software backend.
            const int mouse_x = static_cast<short>(LOWORD(lparam));
            const int mouse_y = static_cast<short>(HIWORD(lparam));

            g_mouse_x = static_cast<float>(std::clamp(
                mouse_x, 0, std::max(0, g_width - 1)));

            g_mouse_y = static_cast<float>(std::clamp(
                mouse_y, 0, std::max(0, g_height - 1)));

            return 0;
        }
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
    WNDCLASSA window_class{};
    window_class.lpfnWndProc = window_proc;
    window_class.hInstance = instance;
    window_class.lpszClassName = "LowLevelOpenGL3D";
    window_class.hCursor = LoadCursorA(nullptr, IDC_ARROW);
    window_class.style = CS_OWNDC;

    if (RegisterClassA(&window_class) == 0) {
        MessageBoxA(nullptr, "RegisterClassA failed.", "Error", MB_ICONERROR);
        return 1;
    }

    HWND window = CreateWindowExA(
        0,
        window_class.lpszClassName,
        "Low-Level 3D - OpenGL API Backend",
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
        MessageBoxA(nullptr, "CreateWindowExA failed.", "Error", MB_ICONERROR);
        return 2;
    }

    if (!initialize_wgl(window)) {
        MessageBoxA(window, "Failed to create WGL/OpenGL context.", "Error", MB_ICONERROR);
        return 3;
    }

    if (!load_gl_functions()) {
        MessageBoxA(
            window,
            "OpenGL 2.0+ functions are unavailable. Check the GPU driver.",
            "Error",
            MB_ICONERROR);
        return 4;
    }

    if (glGetString(GL_VERSION) == nullptr) {
        MessageBoxA(window, "glGetString(GL_VERSION) failed.", "Error", MB_ICONERROR);
        return 5;
    }

    if (!initialize_program()) {
        return 6;
    }

    reset_scene(g_scene);
    g_camera = CameraState{};

    auto previous_time = std::chrono::steady_clock::now();
    double accumulator = 0.0;
    constexpr double kFixedTimeStep = 1.0 / 120.0;

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

        const auto current_time = std::chrono::steady_clock::now();
        double delta_time =
            std::chrono::duration<double>(current_time - previous_time).count();
        previous_time = current_time;

        delta_time = std::min(delta_time, 0.05);
        update_camera_keyboard(static_cast<float>(delta_time));
        accumulator += delta_time;

        while (accumulator >= kFixedTimeStep) {
            physics_step(g_scene, static_cast<float>(kFixedTimeStep));
            accumulator -= kFixedTimeStep;
        }

        render_scene();
        Sleep(1);
    }

    wglMakeCurrent(nullptr, nullptr);

    if (g_render_context != nullptr) {
        wglDeleteContext(g_render_context);
    }

    if (g_device_context != nullptr) {
        ReleaseDC(window, g_device_context);
    }

    return 0;
}
