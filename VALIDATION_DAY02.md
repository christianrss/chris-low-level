# VALIDATION_DAY02 — auditoria pedagógica e executável

Data auditada: 2026-09-04.

## Escopo

Foram auditados os 11 módulos do Day 02:

1. `systems/arena_allocator`
2. `ai/tensor_strides`
3. `algorithms/sorting_research`
4. `quantum/statevector_intro`
5. `os/graphics_reference`
6. `debugger/protocol_v1`
7. `redteam/elf64_triage`
8. `dotnet/csharp_span_arraypool`
9. `dotnet/clr_pe_cli_metadata`
10. `nodejs/typescript_stream_backpressure`
11. `javascript/bytecode_vm_from_scratch`

## Gate pedagógico

Comando:

```bash
python scripts/pedagogy_check_day02.py
```

Resultado observado:

```text
day02 pedagogy check passed: 11 modules, 43 starter TODO mappings
```

O gate exige, para cada TODO de código:

- ID único `TODO [ID]` no starter;
- arquivo equivalente em `solutions/`;
- marcador `PEDAGOGY-SOLUTION: ID` na solução;
- referência do mesmo ID na resolução guiada;
- caminho exato `starter/...` na resolução;
- referência do ID em `TESTES_GUIADOS.md`;
- marcador `PEDAGOGY-TEST: ID` no código de teste real;
- starter + solution com testes registrados no CTest quando CMake é usado;
- ausência de delegação de implementação essencial para o gabarito.

## Correções pedagógicas relevantes

- Os guias de testes deixaram de ser genéricos e agora mapeiam TODO → teste → invariante.
- `graphics_reference`: o compositor completo agora é ensinado na resolução; não há mais “veja o bloco no gabarito”.
- `protocol_v1`: a parte final de `decode_debug_packet` agora contém código exato para payload, FNV-1a, comparação de hash e retorno.
- `javascript/bytecode_vm_from_scratch`: lexer, keywords, statements, precedência e `Op::Add` agora possuem TODOs reais no starter. A resolução não descreve mais como exercício código que já vinha pronto.
- `nodejs/typescript_stream_backpressure`: infraestrutura já fornecida (`Buffer` normalization, `_flush`, demo) é explicitamente identificada como leitura; o TODO real é framing entre chunks. Foram adicionados testes para linha vazia e UTF-8 multibyte dividido entre chunks.
- `dotnet/clr_pe_cli_metadata`: DOS/PE/DataDirectory/RVA helper são explicitamente scaffolding já fornecido; os dois TODOs reais são as traduções CLI RVA e metadata RVA.
- `dotnet/csharp_span_arraypool`: `Dispose` é explicitamente scaffolding fornecido, não exercício escondido; teste observável de acesso após Dispose foi adicionado.
- `redteam/elf64_triage`: testes inválidos agora cobrem classe 32-bit, big-endian e versão inválida além de truncamento/magic.
- `tensor_strides`: teste explícito de view contígua/strides foi adicionado.
- `statevector_intro`: teste explícito de `Z` e preservação de norma foi adicionado.

## Quality gate

Comando:

```bash
python scripts/quality_check.py
```

Resultado observado:

```text
quality files checked: 698
quality check passed
```

## Starter vs solution — módulos portáveis

Nos módulos C++/Python/Node disponíveis neste container, os starters foram configurados/compilados quando aplicável e **falharam por comportamento propositalmente incompleto**. As solutions correspondentes passaram.

Resultados de solution:

- `tensor_strides`: PASS
- `sorting_research`: PASS
- `protocol_v1`: PASS
- `graphics_reference`: PASS
- `statevector_intro`: PASS
- `arena_allocator`: PASS
- `bytecode_vm_from_scratch`: PASS
- `elf64_triage`: PASS (2 scripts de teste)
- `typescript_stream_backpressure`: PASS (4 testes Node)

Exemplos de falha esperada do starter observados:

- tensor: `plain.rows == 2 && plain.cols == 3` ainda falso antes de `D2-TENSOR-VIEW`;
- debugger: `TODO decode`;
- graphics: `TODO index`;
- arena: `TODO allocate`;
- JavaScript: `expected statement` antes de completar lexer/keywords;
- ELF64: `NotImplementedError` nos dois TODOs;
- Node: framing incompleto causa falhas de chunk/delimitador/UTF-8.

## Projetos cumulativos validados

Depois de sincronizar os testes semanticamente melhorados, passaram localmente:

- `projects/chris-tensor`
- `projects/chris-algorithms`
- `projects/chris-debugger`
- `projects/chris-os`
- `projects/chris-qsim`
- `projects/chris-arena`
- `projects/chris-js`
- `projects/chris-node-streaming` — 4/4 testes
- `projects/chris-binary-toolkit` — strings + ELF64 PASS

## Limitação .NET

O SDK .NET não está instalado neste container. Por isso `dotnet/csharp_span_arraypool` e `dotnet/clr_pe_cli_metadata` foram revisados estruturalmente/estaticamente e seus testes foram fortalecidos, mas **não foram executados aqui**. Os guias deixam essa limitação explícita e não fazem claim de execução inexistente.

## Regra para o aluno

Se a resolução citar uma função, variável, TODO ou arquivo que não exista exatamente no starter, pare e trate isso como defeito do material. O objetivo deste gate é impedir que o aluno tenha de adivinhar código ausente.
