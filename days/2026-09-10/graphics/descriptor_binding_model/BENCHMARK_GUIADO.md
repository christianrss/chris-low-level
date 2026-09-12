# Benchmark — descriptor_binding_model

## Resultados observados

`bind`/`sample` são O(1). O custo visual é raster de três quads. Compare `desc_sw` vs `desc_gl` em FPS; o rebind periódico não deve aparecer no perfil.

## Procedimento
Cronometrar 5s com e sem o loop de rebind para confirmar que o gargalo é paint, não descriptors.
