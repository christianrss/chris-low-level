# Testes guiados — input_event Span

## Caso 1 — layout 24B (DN-INPUT-LAYOUT-01)

`StructSize` e `Marshal.SizeOf` == 24.

## Caso 2 — key A (DN-INPUT-SPAN-02)

Fixture `key_a_press.bin`: type=1, code=30, value=1, sec=1000.

## Caso 3 — stream (SPAN-02)

`event_stream.bin` → 3 eventos via `ReadAll`.

## Caso 4 — HID (DN-INPUT-HID-03)

`KeyAction.Pressed`, scancode 30.

## Caso 5 — PS/2 rel (DN-INPUT-PS2-04)

`mouse_rel.bin` → Dx=5, Dy=-3.

## Caso 6 — truncado (SPAN-02)

Buffer 10 bytes → `TryReadEvent` false.

## Depuração

```powershell
dotnet test --filter Caso2 --verbosity normal
```
