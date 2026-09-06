# Benchmark guiado — Span deflate buffers

**Pergunta:** como o tempo de `InflateStored` escala com LEN, e quanto overhead o header/validação adiciona vs um `Buffer.BlockCopy` cru?

## Procedimento

1. `dotnet run -c Release` no `solutions/` (ou harness scratch).
2. Para LEN ∈ {1024, 65536, 1_048_576}, monte stored block (BFINAL=1) com payload constante.
3. Cronometre 100–1000 inflates; registre mediana.
4. Opcional: compare com copiar o payload já fatiado (sem parse) — isolamento do custo de validação.

## Hipóteses

| LEN | Comportamento |
|-----|----------------|
| 1 KiB | custo fixo do header domina |
| 64 KiB+ | O(LEN) da cópia domina |
| Validação NLEN | O(1), ruído vs cópia grande |

## Resultados observados

Ambiente: Windows 10, .NET 8, lab `span_deflate_buffers/solutions`.

| LEN | nota |
|----:|------|
| 1024 | parse + copy; timing fino ambiente-dependente |
| 65536 | throughput ≈ memcpy |
| 1 MiB | idem; skip microbenchmark se JIT/GC ruidoso |

**Skip honesto** de números absolutos sem harness dedicado no repo. Conclusão qualitativa: para stored, **a cópia é o custo**; a validação LEN/NLEN é o que você não pode “otimizar embora”.

**Conclusão:** use Span para evitar cópias extras do input; nunca pule NLEN por performance.
