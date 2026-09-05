# Testes guiados — AI/ML Systems: matrix multiplication + tiling

`AI-MM-NAIVE-01`: produto 2x3 por 3x2. `AI-MM-TILED-02`: compara tiled vs naive em dimensões que não são múltiplas do tile (3x5x4), evitando um falso sucesso apenas em blocos perfeitos.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
