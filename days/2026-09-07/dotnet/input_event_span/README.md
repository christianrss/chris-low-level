# Ordem de estudo — input_event Span (.NET)

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/InputLab.cs` e localize `TODO [DN-INPUT-LAYOUT-01..PS2-04]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`.
4. Rode `dotnet test` em `starter/tests/` após cada TODO.
5. Confira `solutions/` depois de tentar.

---

# Treino Low-Level .NET — 2026-09-07 — evdev InputEvent + Span parsers

Lab: struct `input_event` Linux (layout **Explicit 24 bytes**) + leitura via `ReadOnlySpan<byte>` + interpretação de teclado HID (`EV_KEY`) e mouse PS/2 relativo (`EV_REL`).

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `starter/` | `Chris.InputLab.csproj`, `InputLab.cs`, `tests/` |
| `solutions/` | gabarito |
| `fixtures/` | dumps binários de 24 bytes (`key_a_press.bin`, etc.) |

## Pré-requisitos

- .NET 8 SDK
- Noções de `StructLayout`, `Span<T>`, evdev (`linux/input.h`)

## TODOs

| ID | API |
|----|-----|
| `DN-INPUT-LAYOUT-01` | `InputEvent` Explicit 24B |
| `DN-INPUT-SPAN-02` | `InputEventSpan.TryReadEvent` |
| `DN-INPUT-HID-03` | `HidKeyboardParser.TryParseKeyPress` |
| `DN-INPUT-PS2-04` | `Ps2MouseParser.ParseRelativeMotion` |

## Testes starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-07\dotnet\input_event_span\starter\tests
dotnet test
```

## Testes gabarito (esperado PASS)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-07\dotnet\input_event_span\solutions\tests
dotnet test
```

## Cobertura

| Caso | ID | Assert |
|------|-----|--------|
| 1 | DN-INPUT-LAYOUT-01 | `Marshal.SizeOf<InputEvent>() == 24` |
| 2–3 | DN-INPUT-SPAN-02 | leitura fixture + stream |
| 4 | DN-INPUT-HID-03 | KEY_A pressed |
| 5 | DN-INPUT-PS2-04 | REL_X=+5, REL_Y=-3 |
| 6 | DN-INPUT-SPAN-02 | buffer truncado rejeitado |
