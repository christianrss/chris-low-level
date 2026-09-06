# Systems — LZ77 dictionary codec (CHLZ7)

**Objetivo:** Implementar busca de match na janela 32 KiB, encode/decode de tokens literais/match e round-trip verificável no formato didático `CHLZ7`.

## Ordem recomendada

1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. `starter/` — localize `TODO [COMP-LZ77-…]`
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis

- `COMP-LZ77-01` — janela `LZ77_WINDOW_SIZE`
- `COMP-LZ77-02` — longest match ≥ `LZ77_MIN_MATCH`
- `COMP-LZ77-03` — `encode_lz77` (header + tokens)
- `COMP-LZ77-04` — `decode_lz77` (sliding window na saída)

## Pré-requisitos

- CMake 3.16+
- C++20 (MSVC / GCC / Clang)

## Build (starter)

```bash
cmake -S days/2026-09-06/systems/lz77_dictionary/starter -B days/2026-09-06/systems/lz77_dictionary/starter/build
cmake --build days/2026-09-06/systems/lz77_dictionary/starter/build --config Release
ctest --test-dir days/2026-09-06/systems/lz77_dictionary/starter/build -C Release --output-on-failure
```

Saída esperada após implementar os TODOs: `OK lz77`.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-compress` |
| O que levar | `find_longest_match` + codec CHLZ7 |
| Testes a replicar | round-trip + magic inválido |
| Milestone | estágio dicionário antes de DEFLATE |
| Commit sugerido | `feat(compress): port LZ77 dictionary from day06 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
