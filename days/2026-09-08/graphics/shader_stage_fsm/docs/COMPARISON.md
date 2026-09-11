# Comparação — shader stage FSM

Lab **headless**: a máquina de estados é a parte testável. Não há janela Win32
neste módulo (regra visual do Dia 07 não se aplica a FSM pura).

| Etapa | CPU / software | OpenGL | Este lab |
|-------|----------------|--------|----------|
| Estado | objeto C++ | `glCompileShader` / program | enumeração + tabela de transições |
| Evidência | printf / assert | framebuffer | `ctest` na tabela |
| Por quê headless? | A transição ilegal é um invariante, não um pixel | pixel vem depois que o PSO está válido | testamos a tabela sem driver GPU |
