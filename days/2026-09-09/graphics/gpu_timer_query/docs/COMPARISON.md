# Comparação — GPU timer query (simulação headless)

Lab **headless**: a máquina de estados / timer simulado é o artefato testável.
Não há janela Win32 obrigatória neste módulo (FSM/timer, não pixels).

| Etapa | Software (CPU) | OpenGL | Este lab |
|-------|----------------|--------|----------|
| medição / estado | perf_counter / FSM | timer query / PSO | simulação determinística |
| validação | asserts unitários | frame dump / debug group | `PEDAGOGY-TEST` |
| CI | sempre | GPU nem sempre | headless PASS |
