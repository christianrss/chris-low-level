# Teoria passo a passo — AI/ML Systems: matrix multiplication + tiling

Matmul `C[M,N] = A[M,K] x B[K,N]` executa uma soma de produtos para cada saída. Em row-major, acessar A por linha é local; o acesso ingênuo a B varia pela dimensão K e pode prejudicar cache dependendo da ordem de loops.

Tiling divide M/N/K em blocos pequenos para reutilizar dados carregados em cache. Hoje o foco é equivalência numérica e contagem de operações; performance real será medida depois.
