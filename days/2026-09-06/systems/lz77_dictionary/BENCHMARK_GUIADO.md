# Benchmark guiado — Systems: LZ77 dictionary codec

**Pergunta:** quanto custa a busca ingenua `O(n · W)` de `find_longest_match` quando a entrada cresce e a janela está cheia?

O benchmark de hoje é um baseline de CPU no encode, não uma medida de taxa de compressão de produção.

1. Compile `solutions/` em Release.
2. Gere entradas determinísticas: texto repetitivo (`"ABC"` × N) e texto quase aleatório.
3. Faça 5 aquecimentos de `encode_lz77` + `decode_lz77`.
4. Meça ≥ 30 rodadas; registre mediana e min/max do encode.
5. Compare N ∈ {1 KiB, 32 KiB, 256 KiB} — observe o cliff quando a janela fica saturada.
6. Anote que I/O de arquivo e alocação de `vector` também entram no tempo se você incluir dump em disco.

**Próximo experimento de pesquisa:** indexar a janela com hash de 3 bytes (estilo zlib) e medir speedup vs busca linear deste lab.

## Resultados observados

Ambiente de referência: preencha após rodar localmente (MSVC/GCC Release).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| Encode 1 KiB repetitivo (mediana) | — | preencher |
| Encode 32 KiB repetitivo (mediana) | — | janela cheia |
| Encode 256 KiB repetitivo (mediana) | — | custo quadraticamente pior |
| Round-trip suite `test_lz77` | < 1 s | smoke, não microbench |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.
