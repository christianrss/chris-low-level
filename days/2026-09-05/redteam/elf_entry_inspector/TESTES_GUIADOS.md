# Testes guiados — Red Team seguro: ELF entry-point inspector

`RT-ELF-HDR-01`: rejeita magic errado, ELF32 e big-endian. `RT-ELF-ENTRY-02`: fixture sintética retorna entry `0x401000` e machine x86-64 (62).

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
