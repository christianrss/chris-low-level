# Testes guiados — .NET/CLR: tiny CIL decoder

Cobertura projetada no próprio `Program.cs` para `CLR-IL-OPCODE-01` e `CLR-IL-OPERAND-02`: dois `ldc.i4.s`, `add`, `ret`, operand negativo e truncamento. **Não executado** nesta máquina por ausência do SDK .NET; essa limitação deve constar em `VALIDATION_DAY03.md`.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
