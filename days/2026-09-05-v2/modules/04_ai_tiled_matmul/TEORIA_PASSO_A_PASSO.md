# Teoria passo a passo

## 1. Matmul como núcleo de ML
Camadas lineares e partes de attention reduzem-se a multiplicações de matrizes. Para A de forma MxK e B de forma KxN, cada elemento `C[i,j]` é a soma de `A[i,k] * B[k,j]`.

## 2. Row-major
Os vetores do laboratório são contíguos em row-major. O índice de A é `i*K + k`; de B é `k*N + j`; de C é `i*N + j`. Errar stride produz resultado plausível porém incorreto, por isso usamos fixture conhecida.

## 3. Versão naive
Loops `i,j,k` são fáceis de provar corretos. Antes de otimizar, precisamos de uma baseline de correção.

## 4. Tiling/cache blocking
A versão tiled percorre blocos `ii,kk,jj`. O objetivo é reutilizar regiões menores de A/B/C enquanto ainda estão próximas na hierarquia de cache. O tamanho do tile não é universal; depende de CPU, cache, compilador e forma.

## 5. Benchmark responsável
Uma única execução não prova que tiling é melhor. Use warm-up, várias repetições, mediana e verifique o checksum. O resultado é específico deste ambiente.