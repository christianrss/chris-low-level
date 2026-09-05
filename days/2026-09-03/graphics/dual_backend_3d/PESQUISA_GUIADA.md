# Pesquisa guiada — dual_backend_3d

Use as fontes para entender o mecanismo; não copie implementações prontas.

## Rasterização e barycentrics

Pesquise na documentação/recursos técnicos pelos termos:

- `edge function triangle rasterization`
- `barycentric coordinates rasterization`
- `depth buffer interpolation`

Responda antes de implementar:

1. Por que uma bounding box reduz o trabalho?
2. Por que os três pesos barycentric somam 1?
3. O que muda quando o winding é invertido?

## OpenGL

Consulte a referência OpenGL para:

- `glEnable(GL_DEPTH_TEST)`
- `glEnable(GL_CULL_FACE)`
- `glCullFace`
- `glFrontFace`
- `glDrawArrays`

Responda:

1. Qual parte do pipeline software passa a ser responsabilidade da GPU?
2. O que `GL_CCW` define?
3. Culling acontece antes ou depois de gerar todos os fragmentos?

## Câmera

Pesquise:

- `right handed lookAt matrix`
- `yaw pitch FPS camera`
- `fixed timestep game loop accumulator`

Responda:

1. Por que a view matrix é uma transformação inversa da câmera?
2. Por que pitch é limitado?
3. Por que câmera pode usar `frame_dt`, mas física deve manter `physics_dt` fixo neste laboratório?

## Win32/WGL

Consulte documentação Microsoft para:

- `CreateWindowEx`
- `PeekMessage`
- `WM_MOUSEMOVE`
- `GetAsyncKeyState`
- `ChoosePixelFormat`
- `wglCreateContext`
- `wglGetProcAddress`

Pergunta final: quais responsabilidades pertencem ao Win32, quais ao WGL/OpenGL e quais ao nosso engine?

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
