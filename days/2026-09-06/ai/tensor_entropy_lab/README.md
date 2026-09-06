# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/entropy_lab.py` e localize `TODO [AI-ENT-01..03]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Rode o teste após cada TODO.
5. Só então compare com `solutions/`.

---

# Treino Low-Level AI — 2026-09-06 — Tensor entropy lab

Lab: **Shannon + RLE + gzip** em Python stdlib — medir entropia e razões de compressão em tensores/bytes.

## Estrutura

- `starter/`: TODOs em `entropy_lab.py`; testes em `test_entropy_lab.py`.
- `solutions/`: gabarito completo.
- APIs: `shannon_entropy`, `tensor_rle_encode`, `compression_ratio_rle`, `compression_ratio_gzip`.

## Pré-requisitos

- Python 3.10+ (stdlib: `gzip`, `math`, `collections`)

## Caminho recomendado

1. Teoria: H, traces de RLE, envelope gzip.
2. `AI-ENT-01` — Shannon.
3. `AI-ENT-02` — RLE + ratio.
4. `AI-ENT-03` — gzip ratio.
5. Conferir gabarito.

## Rodar o starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\ai\tensor_entropy_lab
python starter/test_entropy_lab.py
```

O stub levanta `NotImplementedError` → falha intencional.

## Rodar o gabarito (esperado PASS)

```powershell
python solutions/test_entropy_lab.py
```

Saída: `OK tensor entropy lab`.

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | AI-ENT-01 | uniforme 4 símbolos → H=2.0 |
| 2 | AI-ENT-02 | RLE `[(7,1000),(3,500)]`, ratio < 0.01 |
| 3 | AI-ENT-03 | gzip < 0.2 e < RLE em `LOWLEVEL`×500 |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-ai-toolkit` |
| O que levar | `shannon_entropy`, RLE didático, helpers de ratio |
| Milestone | métricas de informação / compressão |
| Commit sugerido | `feat(ai-toolkit): port tensor entropy lab from day06` |
