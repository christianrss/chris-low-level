# Benchmark — alpha_blend_scanline

## Resultados observados

CI headless só corre `test_blend`. No Windows compare FPS `blend_sw` (scanline CPU) vs `blend_gl` (blend HW).

## Procedimento
1. Aumentar `w/h` dos sprites e medir frame time.
2. Anotar quando o CPU cai abaixo de 60 FPS.
