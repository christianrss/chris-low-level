# Benchmark guiado

Sem SDK .NET não há benchmark executado. Quando disponível, um benchmark útil deve decodificar o mesmo byte array muitas vezes, separar warm-up/JIT de steady state e evitar medir apenas startup do processo.