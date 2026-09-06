#version 120
uniform sampler2D u_albedo;
uniform sampler2D u_normal_map;
uniform vec3 u_light_pos;
uniform vec3 u_light_dir;
uniform vec3 u_light_color;
uniform vec3 u_view_pos;
uniform float u_ambient;
uniform float u_spot_cutoff;
uniform float u_spot_exponent;
uniform bool u_emissive;

varying vec3 v_world_pos;
varying vec3 v_normal;
varying vec2 v_uv;
varying mat3 v_tbn;

void main() {
    vec3 albedo = texture2D(u_albedo, v_uv).rgb;

    // PEDAGOGY-SOLUTION: LANTERN-NORM-03
    vec3 tangent_normal = texture2D(u_normal_map, v_uv).rgb * 2.0 - 1.0;
    vec3 N = normalize(v_tbn * tangent_normal);

    vec3 L = normalize(u_light_pos - v_world_pos);
    vec3 V = normalize(u_view_pos - v_world_pos);

    // PEDAGOGY-SOLUTION: LANTERN-LIGHT-04 — spotlight estreito + ambiente baixo.

    float theta = dot(-L, normalize(u_light_dir));
    float spot = 0.0;
    if (theta > u_spot_cutoff) {
        spot = pow(theta, u_spot_exponent);
    }

    float diff = max(dot(N, L), 0.0) * spot;
    vec3 lighting = u_ambient + diff * u_light_color;

    if (u_emissive) {
        lighting += vec3(0.35, 0.28, 0.08);
    }

    gl_FragColor = vec4(albedo * lighting, 1.0);
}
