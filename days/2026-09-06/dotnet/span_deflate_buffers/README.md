# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/Program.cs` e localize `TODO [DN-SPAN-01..03]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Rode `dotnet run` após completar o parser.
5. Só então compare com `solutions/`.

---

# Treino Low-Level .NET — 2026-09-06 — Span deflate buffers

Lab: **DEFLATE stored block** com `ReadOnlySpan<byte>` — header, LEN/NLEN, inflate.

## Estrutura

- `starter/`: TODOs em `Program.cs` (`DeflateStored`); `BuildStoredBlock` + `Main` prontos.
- `solutions/`: gabarito completo.
- Projeto: `Chris.IlLab.csproj` (`net8.0`).

## Pré-requisitos

- .NET 8 SDK

## Caminho recomendado

1. Teoria: layout 5+LEN, BTYPE, complemento.
2. `DN-SPAN-01` / `DN-SPAN-03` — `ReadStoredHeader`.
3. `DN-SPAN-02` — `InflateStored`.
4. Conferir gabarito.

## Rodar o starter (esperado FAIL até implementar)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\dotnet\span_deflate_buffers\starter
dotnet run
```

Stub: `NotImplementedException`.

## Rodar o gabarito (esperado PASS)

```powershell
cd ..\solutions
dotnet run
```

Saída: `OK deflate stored`.

## O que o Main cobre

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | DN-SPAN-01/02/03 | inflate `"LOWLEVEL"` |
| 2 | DN-SPAN-01 | truncado 3 bytes → `InvalidDataException` |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-il-lab` (ou compress .NET) |
| O que levar | `DeflateStored` + asserts de truncamento |
| Milestone | parsers Span / DEFLATE |
| Commit sugerido | `feat(il-lab): port span deflate stored from day06` |
