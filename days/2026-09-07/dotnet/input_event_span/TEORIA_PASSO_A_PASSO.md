# Teoria passo a passo — input_event Span (.NET)

## 1. O que estamos construindo

Parser de eventos de entrada Linux **evdev** em C# (.NET 8):

- `InputEvent` — struct com `[StructLayout(Explicit, Size=24)]` espelhando `struct input_event` em x86_64
- `InputEventSpan.TryReadEvent` — lê 24 bytes de `ReadOnlySpan<byte>`
- `HidKeyboardParser` — interpreta `EV_KEY` (teclado boot/HID via evdev)
- `Ps2MouseParser` — acumula `EV_REL` REL_X/REL_Y (mouse PS/2 relativo)

TODOs: `DN-INPUT-LAYOUT-01`, `DN-INPUT-SPAN-02`, `DN-INPUT-HID-03`, `DN-INPUT-PS2-04`.

## 2. Por que evdev em C#?

Drivers e daemons de input no Linux leem `/dev/input/event*` como stream de structs fixas. Em .NET, `Span<byte>` permite parsing zero-allocation — padrão usado em telemetria, emuladores e ferramentas cross-platform que consomem dumps de eventos.

## 3. Layout `input_event` (x86_64)

```text
offset | tamanho | campo C
-------|---------|------------------
0..7   | 8       | timeval.tv_sec (long)
8..15  | 8       | timeval.tv_usec (long)
16..17 | 2       | type (__u16)
18..19 | 2       | code (__u16)
20..23 | 4       | value (__s32)
Total: 24 bytes
```

**Atenção:** em ARM32 o layout difere (timeval menor). Este lab fixa **24 bytes** como no ambiente de referência x86_64 do curso.

### Por quê fixar 24 bytes no lab?

O kernel documenta `sizeof(struct input_event)` por arquitetura. Fixar x86_64 evita ambiguidade nos testes e nas fixtures `.bin` — qualquer port para ARM exige revalidar offsets, não misturar layouts no mesmo corpus.

## 4. Tipos de evento (subset)

| Constante | Valor | Uso no lab |
|-----------|-------|------------|
| `EV_SYN` | 0 | sincronização (ignorado nos parsers) |
| `EV_KEY` | 1 | teclado — code = scancode Linux, value 0/1/2 |
| `EV_REL` | 2 | mouse relativo — code REL_X/REL_Y |

`KEY_A` = 30 (scancode Linux/evdev). `REL_X` = 0, `REL_Y` = 1.

## 5. Value em EV_KEY

| value | Significado |
|-------|-------------|
| 0 | released |
| 1 | pressed |
| 2 | repeated (autorepeat) |

## 6. Value em EV_REL

Delta signed (`int`) — movimento relativo desde o último evento.

## 7. Explicit layout em C#

```csharp
[StructLayout(LayoutKind.Explicit, Size = 24)]
public struct InputEvent
{
    [FieldOffset(0)] public long TimeSec;
    [FieldOffset(8)] public long TimeUsec;
    [FieldOffset(16)] public ushort Type;
    [FieldOffset(18)] public ushort Code;
    [FieldOffset(20)] public int Value;
}
```

`Marshal.SizeOf<InputEvent>()` deve retornar 24. Offsets errados desalinham type/code/value.

### Por quê `LayoutKind.Explicit` em vez de `Sequential`?

`Sequential` deixa o runtime inserir padding entre campos. O wire format do kernel não tem padding entre `type` e `code` — `Explicit` força cada campo no offset documentado no header `input.h`.

## 8. Leitura com Span — `BinaryPrimitives`

.NET 8: `BinaryPrimitives.ReadInt64LittleEndian(slice)` aceita `ReadOnlySpan<byte>` — preferível a `BitConverter` que exige `byte[]`.

### Por quê `BinaryPrimitives` e não `BitConverter`?

`BitConverter` aloca ou exige array heap; `ReadOnlySpan<byte>` lê direto do dump sem cópia. Em replay de milhões de eventos, isso mantém o hot path sem pressão no GC.

## 9. Fixture key_a_press.bin

```text
sec=1000, usec=500, type=1, code=30, value=1
```

Hex (24 bytes):

```text
e8 03 00 00 00 00 00 00  f4 01 00 00 00 00 00 00  01 00 1e 00 01 00 00 00
```

## 10. Fixture mouse_rel.bin

Dois eventos: REL_X +5, REL_Y -3 → delta acumulado (5, -3).

## 11. ReadAll

Itera em passos de 24 bytes; para se `TryReadEvent` falhar ou buffer acabar.

## 12. HidKeyboardParser

Filtra `Type == EV_KEY`; valida `Value` em 0..2; retorna scancode e `KeyAction`.

## 13. Ps2MouseParser

Soma valores de `EV_REL` por eixo; ignora outros tipos.

## 14. Diagrama

```text
[dump .bin]
  → TryReadEvent × N
  → HidKeyboardParser (EV_KEY)
  → Ps2MouseParser (EV_REL acumulado)
```

## 15. Erros e contratos

- `TryReadEvent` retorna `false` se `offset + 24 > buffer.Length`
- Parsers retornam `false` ou delta zero quando tipo incompatível

## 16. Relação com hid_keyboard_boot / ps2_mouse_input

Labs futuros no mesmo dia leem protocolo **raw** (boot report / pacote PS/2). Este lab traduz a camada **evdev** já normalizada pelo kernel.

## 17. Invariantes

1. StructSize constante 24.
2. Little-endian para todos os campos numéricos no wire.
3. Não assumir padding implícito — usar Explicit.

## 18. Bugs comuns

- `FieldOffset(16)` para `Code` (errado — code em 18).
- `Size = 16` esquecendo timeval completo.
- Big-endian ao ler `Value`.
- Tratar `EV_SYN` como tecla.

## 19. Depuração

```powershell
Format-Hex fixtures\key_a_press.bin
dotnet test --filter Caso2
```

## 20. Síntese

Você aprende a espelhar um struct de kernel em C# com layout explícito, ler bytes com `Span` sem alocação, e separar parsing wire (SPAN) de semântica (HID/PS2 via evdev).
