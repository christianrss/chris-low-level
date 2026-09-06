# Benchmark guiado — RLE byte codec

**Pergunta:** em quais entradas CHRLE reduz tamanho, e em quais aumenta?

RLE não compete com Huffman/LZ em texto geral; o benchmark serve para ver o efeito do padrão de runs, não para crownear throughput absoluto.

## Procedimento

1. Compile `solutions/` em Release.
2. Meça `enc.size()` vs `input.size()` para três classes:
   - **A:** 64 KiB de byte constante (`0x00`).
   - **B:** 64 KiB alternando `0x00`/`0xFF` a cada byte.
   - **C:** 64 KiB pseudo-aleatório (PRNG fixo, seed documentada).
3. Opcional: cronometre 100 encodes+decodes e registre mediana em ms.
4. Anote razão `compressed / original` (menor que 1 = ganho).

## Hipóteses

| Classe | Razão esperada (ordem de grandeza) |
|--------|-------------------------------------|
| A (run única / poucas) | ≪ 1 (header ~9 B + poucos pares) |
| B (sem runs longas) | > 1 (cerca de 2× no payload + header) |
| C (aleatório) | > 1 |

## Resultados observados

Ambiente: Windows 10, MSVC (Release), lab `rle_byte_codec/solutions`.

| Entrada | original (B) | comprimido (B) | razão | nota |
|---------|-------------:|---------------:|------:|------|
| 65536 × `0x00` | 65536 | 527 | ~0.008 | `ceil(65536/255)=258` pares + 9 header |
| 65536× alt 00/FF | 65536 | 131081 | ~2.00 | count=1 cada byte |
| PRNG 64 KiB | 65536 | ~131000 | ~2.0 | skip de cronometragem fina |

Throughput de encode/decode em 64 KiB: **skip honesto** neste lab (sem harness de timing dedicado no repo); o resultado útil é a **razão de tamanho**, não ns/op.

**Conclusão:** use RLE quando o domínio garante runs (máscaras, scans, padding); não use como codec universal de texto.
