#version 120
attribute vec3 a_pos;
attribute vec3 a_normal;
attribute vec2 a_uv;
attribute vec3 a_tangent;

uniform mat4 u_mvp;
uniform mat4 u_model;

varying vec3 v_world_pos;
varying vec3 v_normal;
varying vec2 v_uv;
varying mat3 v_tbn;

void main() {
    vec4 world_pos = u_model * vec4(a_pos, 1.0);
    v_world_pos = world_pos.xyz;

    vec3 T = normalize(mat3(u_model) * a_tangent);
    vec3 N = normalize(mat3(u_model) * a_normal);
    T = normalize(T - dot(T, N) * N);
    vec3 B = cross(N, T);
    v_tbn = mat3(T, B, N);

    v_normal = N;
    v_uv = a_uv;
    gl_Position = u_mvp * vec4(a_pos, 1.0);
}
