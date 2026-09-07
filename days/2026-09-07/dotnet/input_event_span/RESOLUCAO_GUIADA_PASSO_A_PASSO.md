# Resolução guiada passo a passo — .NET / input_event Span

Trabalhe em `days/2026-09-07/dotnet/input_event_span/starter/`. Implemente os quatro TODOs em `starter/InputLab.cs` na ordem LAYOUT → SPAN → HID → PS2.

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | O que substituir |
|---------|-----------------|-----------------|------------------|
| `DN-INPUT-LAYOUT-01` | `starter/InputLab.cs` | struct `InputEvent` | validar offsets e `Size = 24` |
| `DN-INPUT-SPAN-02` | `starter/InputLab.cs` | `InputEventSpan.TryReadEvent` | stub que retorna `false` |
| `DN-INPUT-HID-03` | `starter/InputLab.cs` | `HidKeyboardParser.TryParseKeyPress` | stub que retorna `false` |
| `DN-INPUT-PS2-04` | `starter/InputLab.cs` | `Ps2MouseParser.ParseRelativeMotion` | stub que retorna `(0,0)` |

## Baseline

Antes de editar, confirme que o starter falha nos casos de parsing:

```powershell
cd days/2026-09-07/dotnet/input_event_span/starter/tests
dotnet test
```

**Esperado:** FAIL — `TryReadEvent` retorna `false`, parsers retornam stub. Confirme fixture com `Format-Hex ..\fixtures\key_a_press.bin` (primeiros 8 bytes = `sec=1000` LE).

---

## DN-INPUT-LAYOUT-01 — struct 24 bytes

### Onde colocar (LAYOUT-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/InputLab.cs` |
| Função / âncora | comentário `TODO [DN-INPUT-LAYOUT-01]` na struct `InputEvent` |
| Substituir | offsets incorretos ou `Size` ausente — complete `FieldOffset` e constantes |
| Não mexer | testes, fixtures, parsers (ainda stubs) |

### 1. O problema (LAYOUT-01)

O starter pode ter offsets trocados ou `Size` menor que 24. Sem layout correto, `TryReadEvent` lê `type`/`code`/`value` em posições erradas e todos os testes downstream falham silenciosamente.

### Escreva o código (LAYOUT-01)

Valide ou complete a struct:

```csharp
[StructLayout(LayoutKind.Explicit, Size = 24)]
public struct InputEvent
{
    [FieldOffset(0)] public long TimeSec;
    [FieldOffset(8)] public long TimeUsec;
    [FieldOffset(16)] public ushort Type;
    [FieldOffset(18)] public ushort Code;
    [FieldOffset(20)] public int Value;
    public const int StructSize = 24;
    // constantes EV_*, KEY_A, REL_* conforme starter
}
```

### Por que funciona (LAYOUT-01)

`Explicit` + `FieldOffset` espelha o header Linux; `Size=24` impede padding extra do runtime.

### Verifique (LAYOUT-01)

```powershell
dotnet test --filter Caso1
```

**Esperado:** `Marshal.SizeOf<InputEvent>() == 24` e offsets conferem com a tabela da teoria.

### Debug (LAYOUT-01)

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| `SizeOf` ≠ 24 | `Size` omitido ou offsets sobrepostos | revise `FieldOffset` 16/18/20 |
| Caso2 falha com type errado | `Code` em offset 16 | mova `Code` para 18 |

---

## DN-INPUT-SPAN-02 — TryReadEvent

### Onde colocar (SPAN-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/InputLab.cs` |
| Função / âncora | `InputEventSpan.TryReadEvent` — `TODO [DN-INPUT-SPAN-02]` |
| Substituir | corpo stub que sempre retorna `false` |
| Não mexer | struct `InputEvent` após LAYOUT validado |

### 1. O problema (SPAN-02)

Fixtures `.bin` são streams de 24 bytes por evento. Sem `TryReadEvent`, não há conversão wire → struct; HID e PS2 não recebem dados.

### Escreva o código (SPAN-02)

Adicione `using System.Buffers.Binary;` e substitua o stub:

```csharp
public static bool TryReadEvent(ReadOnlySpan<byte> buffer, int offset, out InputEvent ev)
{
    ev = default;
    if (offset < 0 || offset + InputEvent.StructSize > buffer.Length)
        return false;
    var slice = buffer.Slice(offset, InputEvent.StructSize);
    ev = new InputEvent {
        TimeSec = BinaryPrimitives.ReadInt64LittleEndian(slice),
        TimeUsec = BinaryPrimitives.ReadInt64LittleEndian(slice.Slice(8)),
        Type = BinaryPrimitives.ReadUInt16LittleEndian(slice.Slice(16)),
        Code = BinaryPrimitives.ReadUInt16LittleEndian(slice.Slice(18)),
        Value = BinaryPrimitives.ReadInt32LittleEndian(slice.Slice(20)),
    };
    return true;
}
```

### Por que funciona (SPAN-02)

Cada campo lê exatamente seu tamanho em LE; bounds checados antes do slice.

### Verifique (SPAN-02)

```powershell
dotnet test --filter Caso2
dotnet test --filter Caso3
dotnet test --filter Caso6
```

**Esperado:** `key_a_press.bin` → type=1, code=30, value=1; buffer truncado rejeitado.

### Debug (SPAN-02)

| Sintoma | Causa | Ação |
|---------|-------|------|
| value sempre 0 | slice errado em offset 20 | confira `Slice(20)` para `Value` |
| Caso6 não falha | bounds check ausente | teste `offset + 24 > Length` |

---

## DN-INPUT-HID-03 — teclado EV_KEY

### Onde colocar (HID-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/InputLab.cs` |
| Função / âncora | `HidKeyboardParser.TryParseKeyPress` — `TODO [DN-INPUT-HID-03]` |
| Substituir | stub que retorna `false` |
| Não mexer | `TryReadEvent` |

### 1. O problema (HID-03)

Eventos `EV_KEY` carregam scancode Linux e estado press/release/repeat. O parser deve filtrar tipo e validar `value` em 0..2 antes de expor `KeyAction`.

### Escreva o código (HID-03)

```csharp
public static bool TryParseKeyPress(InputEvent ev, out ushort scancode, out KeyAction action)
{
    scancode = 0;
    action = KeyAction.Released;
    if (ev.Type != InputEvent.EvKey) return false;
    scancode = ev.Code;
    if (ev.Value < 0 || ev.Value > 2) return false;
    action = (KeyAction)ev.Value;
    return true;
}
```

### Por que funciona (HID-03)

evdev já normalizou HID boot para `EV_KEY`; `code` é o scancode Linux (`KEY_A=30`).

### Verifique (HID-03)

```powershell
dotnet test --filter Caso4
```

**Esperado:** `KEY_A` press detectado com `action=Pressed`.

### Debug (HID-03)

| Sintoma | Causa | Ação |
|---------|-------|------|
| sempre `false` | comparou com tipo errado | use `InputEvent.EvKey` (1) |
| value inválido aceito | falta checagem 0..2 | rejeite antes do cast |

---

## DN-INPUT-PS2-04 — mouse relativo

### Onde colocar (PS2-04)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/InputLab.cs` |
| Função / âncora | `Ps2MouseParser.ParseRelativeMotion` — `TODO [DN-INPUT-PS2-04]` |
| Substituir | stub que retorna `new MouseDelta(0, 0)` |
| Não mexer | parsers de teclado |

### 1. O problema (PS2-04)

Mouse via evdev emite `EV_REL` com deltas por eixo. Múltiplos eventos no mesmo buffer devem **somar** — fixture `mouse_rel.bin` espera delta (5, -3).

### Escreva o código (PS2-04)

```csharp
public static MouseDelta ParseRelativeMotion(ReadOnlySpan<InputEvent> events)
{
    int dx = 0, dy = 0;
    foreach (var ev in events)
    {
        if (ev.Type != InputEvent.EvRel) continue;
        if (ev.Code == InputEvent.RelX) dx += ev.Value;
        else if (ev.Code == InputEvent.RelY) dy += ev.Value;
    }
    return new MouseDelta(dx, dy);
}
```

### Por que funciona (PS2-04)

PS/2 via evdev emite pares `EV_REL`; somar permite buffers com múltiplos micro-movimentos.

### Verifique (PS2-04)

```powershell
dotnet test --filter Caso5
```

**Esperado:** delta acumulado `(5, -3)` na fixture `mouse_rel.bin`.

### Debug (PS2-04)

| Sintoma | Causa | Ação |
|---------|-------|------|
| dy=0 | ignorou `RelY` | branch `ev.Code == InputEvent.RelY` |
| delta parcial | não somou | use `+=` não `=` |

---

## Relatório de resolução

| Campo | Preencher |
|-------|-----------|
| TODOs concluídos | DN-INPUT-LAYOUT-01, DN-INPUT-SPAN-02, DN-INPUT-HID-03, DN-INPUT-PS2-04 |
| `dotnet test` starter | PASS / FAIL |
| Hex depurado | offset do `value` em key_a_press |
| Dúvidas | |

Checklist final:
- [ ] `Marshal.SizeOf<InputEvent>() == 24`
- [ ] LE em todos os campos
- [ ] KEY_A press detectado
- [ ] delta (5, -3) no mouse
- [ ] truncado rejeitado

Fim da resolução guiada input_event Span.
