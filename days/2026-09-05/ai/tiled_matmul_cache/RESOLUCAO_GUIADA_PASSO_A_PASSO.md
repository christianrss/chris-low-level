# Resolução guiada passo a passo — AI/ML Systems: matrix multiplication + tiling

Em `starter/matmul.cpp`, implemente `matmul_naive` com loops `i,j,k` e índice row-major `row*cols+col`.
```cpp
for(size_t i=0;i<M;++i) for(size_t j=0;j<N;++j){ float sum=0; for(size_t k=0;k<K;++k) sum += A[i*K+k]*B[k*N+j]; C[i*N+j]=sum; }
```
Depois implemente `matmul_tiled` zerando C e usando blocos `ii,kk,jj`, com limites `min(block_start+tile, dimension)`. Dentro, acumule em C.

Teste intermediário: primeiro deixe tiled chamando naive para confirmar fixtures; depois substitua pela versão bloqueada. Debugue comparando cada `C[index]` com tolerância `1e-5`.

## Mapa de consistência auditada
- `AI-MM-NAIVE-01` — starter → resolução → teste → solution.
- `AI-MM-TILED-02` — starter → resolução → teste → solution.
