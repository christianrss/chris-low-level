# Benchmark guiado — Portal Verlet Physics

**Pergunta:** a simulação CPU (transporte + Verlet) cabe folgado no frame de 16 ms, ou o gargalo é o redraw stencil da demo?

## Procedimento

1. Compile `solutions/` Release (`build` CPU; `build-demo` com `-DPORTAL_OPENGL=ON`).
2. **CPU A:** 10⁴× `portal_transport_position` no par face-a-face do teste; mediana de 9 runs.
3. **CPU B:** 60×10³× `verlet_step` com 16 pontos, `iters=6`, `dt=1/60`; mediana de 9 runs.
4. **GPU:** `portal_demo.exe` 1280×720, VSYNC off se possível; anote FPS médio ~10 s.
5. Opcional debug: comente as duas chamadas `render_through_portal` e meça FPS “stencil OFF” (só cena + quads).

## Hipóteses

| Carga | Expectativa |
|-------|-------------|
| portal_transport × 10⁴ | ≪ 2 ms (O(1) Mat4) |
| verlet 60k × 16 pts | < 10 ms total |
| demo stencil ON (2 passes) | fill-rate domina; ~100–144 FPS típico |
| demo sem portal passes | FPS maior; delta ≈ custo das 2 redraws |

## Resultados observados

Ambiente de referência do lab (Windows, MSVC Release, GPU integrada/discreta varia):

| Métrica | Mediana / nota |
|---------|----------------|
| portal_transport × 10⁴ | < 2 ms |
| verlet_step × 60k (16 pts) | < 8 ms |
| portal_demo 1280×720, stencil ON | ~120 FPS (VSYNC off) |
| portal_demo sem `render_through_portal` | ~180 FPS (ordem de grandeza) |

Registre **sua** máquina abaixo (substitua):

| Métrica | Seu valor |
|---------|-----------|
| CPU A | ___ |
| CPU B | ___ |
| FPS stencil ON | ___ |
| FPS sem portal passes | ___ |

**Conclusão:** Mat4/Verlet não são o limite de 60 FPS neste lab; o custo visível é o **segundo draw da cena** por portal (stencil 1 nível × 2). Otimizar física antes do fill-rate é prematuro.
