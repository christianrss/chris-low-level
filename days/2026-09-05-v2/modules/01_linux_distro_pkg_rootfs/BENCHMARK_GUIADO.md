# Benchmark guiado

O benchmark de hoje mede apenas o custo local de instalar um pacote de 4 KiB em diretório temporário. Hipótese: o tempo é dominado por filesystem/metadata, não pelo parse JSON. Faça 2 warm-ups e 9 medições, reporte mediana e não generalize para package managers reais. O resultado executado está em `benchmarks/results-2026-09-05.md`.