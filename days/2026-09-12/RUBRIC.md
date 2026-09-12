# Rubrica — clvm_xdbg (2026-09-12)

Preencha com evidência: arquivo, teste, comando, trace ou resultado.
Estado final sem evidência não recebe pontuação.

## Hard gates

- [ ] Todos os testes obrigatórios da solution passam.
- [ ] O starter falha exatamente nos grupos declarados (`systems/clvm_xdbg`).
- [ ] Nenhum teste obrigatório ficou `SKIP` ou `NOT RUN`.
- [ ] Trust boundaries (parse, opcode, stacks, `mem_in_bounds`) implementados.
- [ ] Mutantes `MUTANT-NO-BOUNDS` e `MUTANT-OPSIZE` rejeitados.

## Pontuação

| Categoria | Máximo | Evidência | Pontos |
|-----------|-------:|-----------|-------:|
| Modelo mental, traces e invariantes | 15 | paper-trace add2 (PC 0/5/10/13/15, call=[13]) | |
| Implementação funcional | 30 | `hex`/`disasm`/`step` até `prints=[8]` | |
| Robustez e limites | 20 | casos 11–15; STORE 254 | |
| Testes e mutantes | 15 | `run_mutant_check.py` | |
| Integração e API | 10 | REPL `break`/`continue`; só `starter/src/**` | |
| Benchmark e interpretação | 5 | `benchmarks/results.json` median/p95 | |
| Síntese técnica | 5 | xdbg views vs x64dbg; por que não anexar processo | |
| **Total** | **100** | | |

**Aprovação:** 75 e todos os hard gates.
**Excelência:** 90 e todos os hard gates.
