# Systems — DEFLATE blocks (RFC 1951 subset)

**Objetivo:** Implementar bitstream LSB-first, blocos stored (`BTYPE=00`) e fixed Huffman só com literais + EOB, com round-trips verificáveis.

## Ordem recomendada

1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md` / `START_HERE.md`
3. `starter/` — localize `TODO [COMP-DEFL-…]`
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis

- `COMP-DEFL-01` — `BitWriter` / `BitReader`
- `COMP-DEFL-02` — encode stored
- `COMP-DEFL-03` — decode stored
- `COMP-DEFL-04` — tabelas fixas + encode fixed
- `COMP-DEFL-05` — decode fixed até EOB

## Pré-requisitos

- CMake 3.16+
- C++17

## Build (starter)

```bash
cmake -S days/2026-09-06/systems/deflate_blocks/starter -B days/2026-09-06/systems/deflate_blocks/starter/build
cmake --build days/2026-09-06/systems/deflate_blocks/starter/build --config Release
ctest --test-dir days/2026-09-06/systems/deflate_blocks/starter/build -C Release --output-on-failure
```

Saída esperada após os TODOs: `OK deflate blocks`.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-compress` |
| O que levar | `bit_stream` + stored/fixed blocks |
| Testes a replicar | nibble `0x1B`, stored `DEFL`, fixed `RFC1951` |
| Milestone | estágio DEFLATE do compressor |
| Commit sugerido | `feat(compress): port DEFLATE blocks from day06 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
