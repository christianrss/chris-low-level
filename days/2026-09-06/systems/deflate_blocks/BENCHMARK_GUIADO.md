# Benchmark guiado — Systems: DEFLATE blocks

**Pergunta:** qual o custo relativo de emitir o mesmo payload como bloco stored versus fixed Huffman (só literais)?

Baseline de CPU no encode/decode in-process — não mede gzip completo nem I/O.

1. Compile `solutions/` em Release.
2. Use payloads determinísticos: 4 KiB de `'A'` repetido e 4 KiB quase aleatórios.
3. 5 aquecimentos; ≥ 30 medições de `encode_stored_block`+`decode_stored_blocks` e de `encode_fixed_block`+`decode_fixed_block`.
4. Registre mediana e min/max; compare razão fixed/stored.
5. Anote que fixed literais em texto repetitivo **aumentam** tamanho vs stored (sem LZ77) — o ganho de Huffman só aparece com distribuição enviesada de bytes distintos.
6. Não inclua criação de processo no timer.

**Próximo experimento de pesquisa:** alimentar o fixed block com tokens LZ77 (length/distance) do módulo irmão e medir taxa + throughput vs stored.

## Resultados observados

Ambiente de referência: preencha após rodar localmente (MSVC/GCC Release).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| Stored 4 KiB round-trip (mediana) | — | preencher |
| Fixed 4 KiB round-trip (mediana) | — | literais + EOB |
| Razão tempo fixed/stored | — | tipicamente > 1 |
| Suite `test_deflate` | < 1 s | smoke |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.
