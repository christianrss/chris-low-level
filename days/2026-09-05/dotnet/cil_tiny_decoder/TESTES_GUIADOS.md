# Testes guiados

### Caso 1: `dotnet run` em starter/ (falha até decodificar opcodes).
### Caso 2: Bytecode `1F 05 1F 07 58 2A` → 4 instruções: ldc.i4.s 5, ldc.i4.s 7, add, ret.
### Caso 3: **Truncado:** `Decode([0x1F])` → InvalidDataException.
### Caso 4: Consulte TEORIA para mapeamento ECMA-335 Partition III.
### Caso 5: Valide solutions/ com asserts completos.

## CLR-IL-OPERAND-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: CLR-IL-OPERAND-02`.

## CLR-IL-OPCODE-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: CLR-IL-OPCODE-01`.
## Execução real (opcional)

**Pré-requisitos:** .NET SDK 8+.

```bash
python scripts/run_real_env_checklist.py --module dotnet/cil_tiny_decoder --day 2026-09-05
```
