# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/gunzip_transform.js` e `starter/backpressure_metrics.js`; localize `TODO [ND-GZ-01..03]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Rode `node test.js` após cada bloco de TODOs.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Node.js — 2026-09-06 — GunzipTransform

Lab: **Transform + createGunzip + backpressure + métricas** em ESM.

## Estrutura

- `starter/gunzip_transform.js` — classe `GunzipTransform` (TODOs 01/03).
- `starter/backpressure_metrics.js` — demo (TODO 02).
- `starter/test.js` — asserts oficiais.
- `solutions/` — gabarito.

## Pré-requisitos

- Node.js 18+ (stdlib `node:stream`, `node:zlib`, `node:events`)

## Caminho recomendado

1. Teoria: pipe, drain, métricas.
2. `ND-GZ-01` / `ND-GZ-03` — Transform.
3. `ND-GZ-02` — demo backpressure.
4. Conferir gabarito.

## Rodar o starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\nodejs\gunzip_transform\starter
node test.js
```

## Rodar o gabarito (esperado PASS)

```powershell
cd ..\solutions
node test.js
```

Saída: `OK gunzip transform { ... }`.

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | ND-GZ-01 | gunzip stream = raw |
| 2 | ND-GZ-03 | bytesIn / bytesOut |
| 3 | ND-GZ-02 | falseWrites > 0, drains iguais |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-node-streams` (ou tooling gzip) |
| O que levar | `GunzipTransform` + teste de backpressure |
| Milestone | streaming compressão |
| Commit sugerido | `feat(node): port gunzip transform from day06` |
