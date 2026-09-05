# Benchmark guiado - core 3D

**Pergunta:** quanto custa atualizar física + construir a lista de desenho sem a API gráfica?

O benchmark portátil executa muitos `physics_step()` e `build_draw_list()` em Release. Ele mede o core compartilhado e evita custo de janela/GPU.

Depois, no Windows, crie benchmarks separados para:

- tempo de frame no software renderer;
- tempo CPU de submissão OpenGL;
- tempo GPU com ferramenta adequada;
- número de objetos/triângulos escalado progressivamente.

Nunca compare FPS sem registrar resolução, número de triângulos e hardware.

## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| Core update | ~163 ns/iter | 1M iterations |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.