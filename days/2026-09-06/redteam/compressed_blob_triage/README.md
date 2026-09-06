# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/blob_triage.py` e localize `TODO [RT-COMP-01..03]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Rode o teste após cada TODO.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Red Team — 2026-09-06 — Compressed blob triage

Lab: **magic → limites → strings** em blobs gzip/zlib (fixtures próprias).

## Estrutura

- `starter/`: TODOs em `blob_triage.py`; `safe_inflate_preview` já implementado; testes em `test_blob_triage.py`.
- `solutions/`: gabarito completo.
- APIs: `detect_compression_magic`, `validate_size_limits`, `extract_ascii_strings`, `safe_inflate_preview`.

## Pré-requisitos

- Python 3.10+ (`gzip`, `zlib`, `re`)

## Caminho recomendado

1. Teoria: magic, zip-bomb mindset, regex ASCII.
2. `RT-COMP-01` — magic.
3. `RT-COMP-02` — limites.
4. `RT-COMP-03` — strings.
5. Conferir gabarito.

## Rodar o starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\redteam\compressed_blob_triage
python starter/test_blob_triage.py
```

## Rodar o gabarito (esperado PASS)

```powershell
python solutions/test_blob_triage.py
```

Saída: `OK blob triage`.

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | RT-COMP-01 | magic gzip |
| 2 | RT-COMP-01 | magic zlib `78 9c` |
| 3 | RT-COMP-02 | limites compressed/uncompressed |
| 4 | RT-COMP-03 | string `SECRET_KEY=abc123` |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-redteam-toolkit` (ou triage util) |
| O que levar | magic + validate + strings com testes |
| Milestone | triage defensivo de blobs |
| Commit sugerido | `feat(redteam): port compressed blob triage from day06` |
