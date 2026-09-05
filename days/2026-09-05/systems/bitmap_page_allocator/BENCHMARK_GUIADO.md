# Benchmark guiado — Systems: bitmap page allocator

Hipótese: first-fit linear fica mais lento quando o bitmap está quase cheio. Após terminar, meça 100 mil ciclos allocate/free em bitmaps de 128 e 8192 páginas; reporte mediana, não apenas um único tempo.
