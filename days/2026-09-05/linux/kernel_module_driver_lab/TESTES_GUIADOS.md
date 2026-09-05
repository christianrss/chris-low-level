# Testes guiados — Linux kernel: lifecycle de char device + módulo real para revisão

`ctest` valida `KMOD-MODEL-OPEN-01` com open/double-open/release e `KMOD-MODEL-IO-02` com write/read/truncamento. `KMOD-SOURCE-REVIEW-03` é validado por presença dos símbolos esperados e pelo checklist de revisão, não por carregamento do módulo.

O módulo real fica explicitamente **não executado** nesta entrega.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
