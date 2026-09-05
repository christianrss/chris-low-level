# Benchmark guiado — Systems: bitmap page allocator

Hipótese: first-fit linear fica mais lento quando o bitmap está quase cheio. Após terminar, meça 100 mil ciclos allocate/free em bitmaps de 128 e 8192 páginas; reporte mediana, não apenas um único tempo.

## Resultados observados

Ambiente: Windows 11, MSVC Release, `solutions/build/Release/test_page.exe`, 5 execuções após warm-up.

| Métrica | Mediana | Notas |
|---------|---------|-------|
| Suite completa (allocate/free/trace) | ~17 ms | ordem de grandeza; rerode localmente |
| Páginas no teste unitário | 128 | ver `test_page_allocator.cpp` |

Valores variam com CPU e flags. Para benchmark de escala (128 vs 8192 páginas), implemente loop dedicado conforme hipótese no topo deste arquivo.
