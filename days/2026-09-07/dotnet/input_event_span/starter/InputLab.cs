using System.Runtime.InteropServices;

namespace Chris.InputLab;

/// <summary>Linux evdev <c>input_event</c> — 24 bytes em x86_64 (timeval 16 + type/code/value).</summary>
/// TODO [DN-INPUT-LAYOUT-01]: confirmar offsets Explicit e Size=24 (timeval + type/code/value).
[StructLayout(LayoutKind.Explicit, Size = 24)]
public struct InputEvent
{
    [FieldOffset(0)] public long TimeSec;
    [FieldOffset(8)] public long TimeUsec;
    [FieldOffset(16)] public ushort Type;
    [FieldOffset(18)] public ushort Code;
    [FieldOffset(20)] public int Value;

    public const int StructSize = 24;

    public const ushort EvSyn = 0;
    public const ushort EvKey = 1;
    public const ushort EvRel = 2;

    public const ushort KeyA = 30;
    public const ushort RelX = 0;
    public const ushort RelY = 1;
}

public enum KeyAction
{
    Released = 0,
    Pressed = 1,
    Repeated = 2,
}

public readonly record struct MouseDelta(int Dx, int Dy);

public static class InputEventSpan
{
    /// <summary>Lê um <see cref="InputEvent"/> de 24 bytes no offset dado.</summary>
    /// TODO [DN-INPUT-SPAN-02]
    public static bool TryReadEvent(ReadOnlySpan<byte> buffer, int offset, out InputEvent ev)
    {
        ev = default;
        _ = buffer;
        _ = offset;
        return false;
    }

    /// <summary>Itera eventos de 24 bytes; retorna quantos foram lidos.</summary>
    public static int ReadAll(ReadOnlySpan<byte> buffer, Span<InputEvent> output)
    {
        int count = 0;
        for (int off = 0; off + InputEvent.StructSize <= buffer.Length && count < output.Length; off += InputEvent.StructSize)
        {
            if (!TryReadEvent(buffer, off, out var ev))
            {
                break;
            }
            output[count++] = ev;
        }
        return count;
    }
}

public static class HidKeyboardParser
{
    /// <summary>Interpreta EV_KEY como tecla HID/evdev (boot scancode no campo <c>code</c>).</summary>
    /// TODO [DN-INPUT-HID-03]
    public static bool TryParseKeyPress(InputEvent ev, out ushort scancode, out KeyAction action)
    {
        scancode = 0;
        action = KeyAction.Released;
        _ = ev;
        return false;
    }
}

public static class Ps2MouseParser
{
    /// <summary>Acumula deltas REL_X/REL_Y de um buffer de eventos (mouse PS/2 via evdev).</summary>
    /// TODO [DN-INPUT-PS2-04]
    public static MouseDelta ParseRelativeMotion(ReadOnlySpan<InputEvent> events)
    {
        _ = events;
        return new MouseDelta(0, 0);
    }
}
