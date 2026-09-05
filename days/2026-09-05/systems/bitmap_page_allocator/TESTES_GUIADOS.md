# Testes guiados — Systems: bitmap page allocator

`SYS-PAGE-ALLOC-01`: aloca páginas 0,1,2 em ordem e esgota um allocator pequeno. `SYS-PAGE-FREE-02`: libera página, reutiliza o slot e rejeita double-free.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
