# Benchmark guiado — Chris Debugger: protocolo remoto v1

## Hipótese
Escreva uma frase falsificável antes de rodar. Exemplo: "a versão A terá menor custo que B para este workload por causa de X".

## Build
```bash
cmake -S projects/chris-debugger -B build/chris-debugger-bench -DCMAKE_BUILD_TYPE=Release -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build build/chris-debugger-bench --config Release
```

Execute o binário `*_benchmark` produzido pelo CMake.

## Registro
Anote CPU, SO, compilador, build type, input, warm-up, repetições e resultado. Para comparação, use mediana de várias execuções e procure outliers.

## Interpretação
Pergunte se a métrica mede o algoritmo que você queria ou inclui startup, alocação, I/O, cache quente/frio e outras variáveis.
