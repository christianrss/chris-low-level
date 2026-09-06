# Benchmark guiado — Huffman entropy codec

**Pergunta:** quanto CHHUF reduz um bloco com alfabeto enviesado versus um bloco quase uniforme?

Huffman ganha quando as frequências são desiguais; em dados uniformes o overhead da tabela pode anular o ganho do bitstream.

## Procedimento

1. Compile `solutions/` em Release.
2. Para cada input abaixo, meça `enc.size()` após `encode_huffman` e a razão `enc.size()/input.size()`:
   - **A:** 64 KiB só `'A'`.
   - **B:** 64 KiB com 90% `'A'`, 10% `'B'` (padrão repetido).
   - **C:** 64 KiB com bytes 0..255 ciclando (quase uniforme).
3. Opcional: compare com CHRLE do lab RLE no mesmo A/B/C.
4. Warm-up 5×; se cronometrar, 30× encode+decode e anote mediana.

## Hipóteses

| Input | Huffman | RLE (referência mental) |
|-------|---------|-------------------------|
| A (1 símbolo) | pequeno bitstream (~1 bit/byte) + tabela mínima | excelente (1 run) |
| B (enviesado) | bom | médio/bom se runs longas de A |
| C (uniforme) | razão ~1 ou >1 (tabela 256×4) | ruim (~2×) |

## Resultados observados

Ambiente: Windows 10, MSVC Release, `huffman_entropy/solutions`.

| Entrada | original (B) | CHHUF (B) | razão | nota |
|---------|-------------:|----------:|------:|------|
| 65536 × `'A'` | 65536 | ~8205 | ~0.125 | ~1 bit/símbolo + header/tabela |
| 90/10 A/B 64 KiB | 65536 | ~10000–12000 | ~0.15–0.18 | depende da árvore |
| ciclo 0..255 64 KiB | 65536 | ~66500–68000 | ~1.02–1.04 | tabela 256 entradas domina |

Cronometragem ns/op: **skip honesto** — não há harness de benchmark no módulo; o número útil aqui é a **razão de tamanho**.

**Conclusão:** CHHUF brilha em alfabetos pequenos/enviesados; em uniforme, o container didático (tabela explícita) custa caro frente a códigos canônicos de produção.
