# START HERE — Day 02 (2026-09-04)

1. Leia `README.md` deste diretório para entender as 11 trilhas e a regra de honestidade sobre `chris-os` / `chris-debugger`.
2. Abra `TODO_MAP.md` e escolha o próximo ID pendente **na ordem sugerida** (Systems → AI → Algorithms → Quantum → OS → Debugger → Red Team → .NET → Node → JS VM).
3. Entre no módulo e leia `TEORIA_PASSO_A_PASSO.md` (O quê / Como / Por quê) e `PESQUISA_GUIADA.md`.
4. Faça um **checkpoint conceitual no papel** (trace de 1 caso) **antes** de abrir o starter — igual ao Dia 06: `ctest PASS` sozinho não basta.
5. Trabalhe exclusivamente em `starter/` até os testes passarem (`TODO [ID]`).
6. Consulte `EXERCICIOS.md` para calibrar dificuldade (fácil → médio → difícil).
7. Se travar, use `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` (problema → algoritmo → código → entenda). No JS VM, traces longos estão em `RESOLUCAO_APENDICE.md`.
8. Compare com `solutions/` somente após concluir ou para auditoria final.
9. Execute o benchmark do módulo e registre observações em `BENCHMARK_GUIADO.md` (seção **Resultados observados**).
10. Ao fechar o dia, rode `python scripts/pedagogy_check_day02.py` e `python scripts/quality_check.py` na raiz do repositório.

**Ordem sugerida dos 11 módulos**

| # | Caminho | Foco | Checkpoint no papel (exemplo) |
|---|---------|------|-------------------------------|
| 1 | `systems/arena_allocator` | Memória e alinhamento | `align_up(13,8)` → 16; base desalinhada |
| 2 | `ai/tensor_strides` | Strides e matmul | `at(2,1)` na view transposta |
| 3 | `algorithms/blocked_merge_sort` | Blocked/external merge | trace n=8 tile=4 (I/O + merge) |
| 4 | `quantum/statevector_intro` | State-vector e gates | Bell: H(0)+CNOT → P(00)=P(11)=½ |
| 5 | `os/graphics_reference` | Compositor + dirty-rect | clip fill; dirty AABB; damage vs full frame |
| 6 | `debugger/protocol_v1` | Framing binário | bytes de `0x1234`; ordem decode |
| 7 | `redteam/elf64_triage` | ELF64 Phdr/Shdr/dynsym | Ehdr + um Phdr LOAD + símbolo `lab_main` |
| 8 | `dotnet/csharp_span_arraypool` | Span + ArrayPool | hex do header LE 8 B |
| 9 | `dotnet/clr_pe_cli_metadata` | PE/CLI/BSJB | cadeia DOS→PE→CLI→BSJB |
| 10 | `nodejs/typescript_stream_backpressure` | Streams + framing | backpressure / highWaterMark |
| 11 | `javascript/bytecode_vm_from_scratch` | Lexer/parser/VM | stack `[10,40]` antes do Add → `50` |

Misture dificuldade dentro de cada módulo: exercícios fáceis constroem a base para os TODOs principais.
