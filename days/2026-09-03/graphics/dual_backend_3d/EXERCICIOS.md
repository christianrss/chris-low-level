# Exercícios — dual backend 3D

## Fácil

- **GFX-MATH-01:** prove que `Mat4::identity()` preserva `Vec4` no teste `test_identity_matrix`.
- **GFX-CAMERA-01:** derive `forward` a partir de yaw/pitch em `engine.cpp`.
- **GFX-CULL-01:** implemente `screen_triangle_front_facing` com área assinada.

## Médio

- **GFX-CAMERA-02 / GFX-CAMERA-03:** construa base right/up/forward e `view_matrix`.
- **GFX-CAMERA-04:** movimento WASD idêntico nos dois backends.
- **GFX-CULL-02:** pule triângulos back-facing no raster software.

## Difícil

- **GFX-CAMERA-05:** mouse look com clamp de pitch em software e OpenGL.
- **GFX-CULL-03:** configure `GL_CULL_FACE` e `glFrontFace(GL_CCW)`.
- **GFX-LAMBERT-01:** fragment shader com normal transformada e luz direcional.

## Desafio

- **GFX-PARITY-01:** capture screenshot software vs GL e compare hash aproximado do centro da tela.
- **GFX-DEPTH-01:** esboce como adicionar Z-buffer sem quebrar a API `DrawItem`.
