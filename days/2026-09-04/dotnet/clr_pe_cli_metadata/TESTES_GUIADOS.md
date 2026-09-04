# Testes guiados
A fixture em `starter/tests/.../Program.cs` cria um PE32+ mínimo em memória:
- `e_lfanew = 0x80`;
- section VA `0x2000`, raw pointer `0x200`;
- CLI RVA `0x2100` → offset `0x300`;
- metadata RVA `0x2200` → offset `0x400`;
- `BSJB` em `0x400`.

Isso permite testar o mapeamento sem depender de um assembly externo. Também teste `new byte[64]`: deve falhar com `InvalidDataException`.
