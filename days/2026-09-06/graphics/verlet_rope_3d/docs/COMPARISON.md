# Comparacao: portal wireframe CPU vs GL stencil

| Etapa | software_win32 | opengl (portal_demo) |
|---|---|---|
| Sala | linhas CPU DIB | GL_LINES |
| Corda Verlet | polyline CPU | line strip |
| Esfera | círculo/wire CPU | mesh + lighting |
| Portal | recorte lógico CPU | stencil buffer |
| Física | `portal_core` compartilhado | compartilhado |

Paridade visual: mesma posição de esfera após teleporte (VISUAL-01).
