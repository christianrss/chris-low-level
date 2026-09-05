# Teoria passo a passo — Systems: bitmap page allocator

Kernels gerenciam memória física em unidades de páginas. Um modelo simples usa um bitmap: bit 0 = livre, bit 1 = ocupado. Para 128 páginas precisamos de 16 bytes. A tradução é `byte = page / 8`, `bit = page % 8`.

O objetivo não é copiar o buddy allocator do Linux; é dominar o menor mecanismo que torna visível a relação entre índice de página, bit e lifetime.
