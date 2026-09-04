# Benchmark guiado - extrator de strings

**Pergunta:** como o throughput do scanner muda com o tamanho do buffer?

Gere buffers determinísticos de 1 MiB, 8 MiB e 32 MiB contendo sequências ASCII em posições conhecidas. Meça apenas `extract_ascii_strings()`. Registre MB/s e confirme que a quantidade de strings encontrada permanece correta.

Depois use `cProfile` ou um profiler Python para descobrir onde o tempo é gasto antes de otimizar.
