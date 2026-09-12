# Teoria passo a passo — explicit_barriers

Laboratório **visual C++** (software Win32 + OpenGL WGL), dual-backend.

## 1. O quê

Transicoes explicitas de ResourceState com validacao; cor de fundo muda a cada barreira aplicada.

## 2. Como — fluxo

```text
core (estado/TODOs) -> software_win32 StretchDIBits
                    -> opengl_win32 SwapBuffers
                    -> mesma cena animada
```

## 3. Tabela de pastas

| Pasta | Papel |
|-------|-------|
| `core/` | lógica testável |
| `software_win32/` | CPU + DIB |
| `opengl_win32/` | WGL + GL legado |
| `tests/` | CTest |

## 4. TODOs

| ID | Papel |
|----|-------|
| `GFX-BAR-VALID` | contrato do assert |
| `GFX-BAR-APPLY` | contrato do assert |
| `GFX-BAR-TICK` | contrato do assert |

## 5. Trace numerico

Execute o Caso 1 do teste no papel antes de editar o starter.

## 6. Por que dual-backend

Por que CPU e GL? Para separar contrato de estado da API de present.

## 7. Por que animacao

Por que mover todo frame? Prova que o loop de mensagem + render esta vivo.

## 8. Por que CTest no core

Por que assert no core? Gates CI sem precisar de janela interativa.

## 9. Invariantes

1. Determinismo do core
2. Mesma cena nos dois backends
3. Nao alterar testes
4. solutions abre janela e apresenta pixels

## 10. Bugs comuns

| Sintoma | Causa | Checagem |
|---------|-------|----------|
| janela preta | clear sem draw | confira render |
| sem movimento | dt=0 | steady_clock |
| teste falha | stub TODO | implemente core |

## 11. Lab vs producao

Recorte pedagogico do mesmo problema de engine/API.

## 12. Checklist

- [ ] Core PASS no CTest
- [ ] software_win32 mostra cena
- [ ] opengl_win32 mostra cena
- [ ] VISUAL-01 ok

## 13. Diagrama de estados

| Frame | Acao |
|-------|------|
| N | simula core |
| N | raster/GL |
| N | present |

## 14. Offsets / layout mental

Framebuffer BGRA little-endian via `0x00RRGGBB` no StretchDIBits top-down.

## 15. Extensao

Opcional: D3D11 Present com a mesma cena (fora do escopo minimo).

## 16. Referencias internas

- `docs/GFX_PEDAGOGY_STANDARD.md`
- `days/2026-09-07/graphics/artillery_trajectory_2d`

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.

## Nota

Mantenha o contrato dos TODOs; nao invente APIs extras no teste.
