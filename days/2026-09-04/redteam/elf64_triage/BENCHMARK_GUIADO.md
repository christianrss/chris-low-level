# Benchmark guiado — ELF64 triage

O benchmark mede somente parsing de header ELF64 em bytes já na memória.

Execute pelo menos cinco vezes, registre Python, CPU e SO e use a mediana de `headers/s`.

Não compare diretamente com `readelf` como se fizessem o mesmo trabalho; `readelf` analisa muito mais estruturas.
