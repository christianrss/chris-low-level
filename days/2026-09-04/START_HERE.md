# START HERE — Day 02 (2026-09-04)

1. Leia `README.md` deste diretório para entender as 11 trilhas e a regra de honestidade sobre `chris-os` / `chris-debugger`.
2. Abra `TODO_MAP.md` e escolha o próximo ID pendente **na ordem sugerida** (Systems → AI → Algorithms → Quantum → OS → Debugger → Red Team → .NET → Node → JS VM).
3. Entre no módulo correspondente e leia `TEORIA_PASSO_A_PASSO.md` e `PESQUISA_GUIADA.md`.
4. Trabalhe exclusivamente em `starter/` até os testes passarem.
5. Consulte `EXERCICIOS.md` para calibrar dificuldade (fácil → médio → difícil).
6. Se travar, use `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` — mas tente primeiro com `TESTES_GUIADOS.md`.
7. Compare com `solutions/` somente após concluir ou para auditoria final.
8. Execute o benchmark do módulo e registre observações em `BENCHMARK_GUIADO.md` (seção **Resultados observados**).
9. Ao fechar o dia, rode `python scripts/pedagogy_check_day02.py` e `python scripts/quality_check.py` na raiz do repositório.

**Ordem sugerida dos 11 módulos**

| # | Caminho | Foco |
|---|---------|------|
| 1 | `systems/arena_allocator` | Memória e alinhamento |
| 2 | `ai/tensor_strides` | Strides e matmul |
| 3 | `algorithms/sorting_research` | Merge vs quick |
| 4 | `quantum/statevector_intro` | State-vector e gates |
| 5 | `os/graphics_reference` | Compositor RGBA |
| 6 | `debugger/protocol_v1` | Framing binário |
| 7 | `redteam/elf64_triage` | ELF64 defensivo |
| 8 | `dotnet/csharp_span_arraypool` | Span + ArrayPool |
| 9 | `dotnet/clr_pe_cli_metadata` | PE/CLI/BSJB |
| 10 | `nodejs/typescript_stream_backpressure` | Streams + framing |
| 11 | `javascript/bytecode_vm_from_scratch` | Lexer/parser/VM |

Misture dificuldade dentro de cada módulo: exercícios fáceis constroem a base para os TODOs principais.
