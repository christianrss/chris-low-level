# Benchmark — pipeline_state_object

## Resultados observados

Em CI headless só corre `test_pso`. No Windows, compare FPS de `pso_sw` (raster CPU do triângulo) vs `pso_gl` (draw imediato). O custo dominante no software é o fill scan do triângulo; o cycle de PSO em si é O(1).

## Procedimento
1. Cronometrar 10s de frame loop com e sem `fill_triangle`.
2. Anotar diferença fill vs wire (wire deve ser bem mais barato no CPU).
