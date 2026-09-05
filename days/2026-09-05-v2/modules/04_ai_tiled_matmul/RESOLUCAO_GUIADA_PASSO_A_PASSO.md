# Resolução guiada passo a passo

Abra `starter/matmul.cpp`.

## Baseline - AI-MM-NAIVE-01
```cpp
for (size_t i=0; i<M; ++i)
  for (size_t j=0; j<N; ++j) {
    float sum=0;
    for (size_t k=0; k<K; ++k)
      sum += A[i*K+k] * B[k*N+j];
    C[i*N+j]=sum;
  }
```

Primeiro faça apenas a naive e rode o teste. Isso cria uma baseline confiável.

## Tiled - AI-MM-TILED-02
Crie C zerada e percorra blocos `ii`, `kk`, `jj`. Dentro de cada bloco, percorra `i`, `k`, `j`; use `std::min(inicio+tile, dimensão)` nos limites. Acumule em `C[i*N+j]`. Valide `tile != 0`.

Build/test:
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Depois compare cada saída tiled com naive usando tolerância `1e-5`. Debugue primeiro índices/strides, depois limites dos blocos.

## Mapa de consistência auditada
- `AI-MM-NAIVE-01` - starter -> resolução -> teste -> solution.
- `AI-MM-TILED-02` - starter -> resolução -> teste -> solution.
