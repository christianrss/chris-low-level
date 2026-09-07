# Exercícios — input_event Span

## Fácil

- **DN-INPUT-LAYOUT-01:** Confirme offsets e rode `Caso1`.  
  **Aceite:** `Marshal.SizeOf<InputEvent>() == 24`.

## Médio

- **DN-INPUT-SPAN-02:** Leia `key_a_press.bin`.  
  **Aceite:** `Caso2`, `Caso6` passam.

## Difícil

- **DN-INPUT-HID-03 + PS2-04:** Parsers semânticos.  
  **Aceite:** `dotnet test` 6/6 no starter.

## Desafio

- **DN-INPUT-CH-01:** Parser que ignora `EV_SYN` em stream de 4 eventos.  
  **Aceite:** documente comportamento + teste local.
