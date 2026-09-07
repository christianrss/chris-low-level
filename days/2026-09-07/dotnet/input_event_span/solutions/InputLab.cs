// PEDAGOGY-SOLUTION: DN-INPUT-LAYOUT-01
// PEDAGOGY-SOLUTION: DN-INPUT-SPAN-02
// PEDAGOGY-SOLUTION: DN-INPUT-HID-03
// PEDAGOGY-SOLUTION: DN-INPUT-PS2-04
using System.Buffers.Binary;
using System.Runtime.InteropServices;

namespace Chris.InputLab;

/// <summary>Linux evdev <c>input_event</c> — 24 bytes em x86_64 (timeval 16 + type/code/value).</summary>
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
    public static bool TryReadEvent(ReadOnlySpan<byte> buffer, int offset, out InputEvent ev)
    {
        ev = default;
        if (offset < 0 || offset + InputEvent.StructSize > buffer.Length)
        {
            return false;
        }

        var slice = buffer.Slice(offset, InputEvent.StructSize);
        ev = new InputEvent
        {
            TimeSec = BinaryPrimitives.ReadInt64LittleEndian(slice),
            TimeUsec = BinaryPrimitives.ReadInt64LittleEndian(slice.Slice(8)),
            Type = BinaryPrimitives.ReadUInt16LittleEndian(slice.Slice(16)),
            Code = BinaryPrimitives.ReadUInt16LittleEndian(slice.Slice(18)),
            Value = BinaryPrimitives.ReadInt32LittleEndian(slice.Slice(20)),
        };
        return true;
    }

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
    public static bool TryParseKeyPress(InputEvent ev, out ushort scancode, out KeyAction action)
    {
        scancode = 0;
        action = KeyAction.Released;
        if (ev.Type != InputEvent.EvKey)
        {
            return false;
        }

        scancode = ev.Code;
        if (ev.Value < 0 || ev.Value > 2)
        {
            return false;
        }

        action = (KeyAction)ev.Value;
        return true;
    }
}

public static class Ps2MouseParser
{
    public static MouseDelta ParseRelativeMotion(ReadOnlySpan<InputEvent> events)
    {
        int dx = 0;
        int dy = 0;
        foreach (var ev in events)
        {
            if (ev.Type != InputEvent.EvRel)
            {
                continue;
            }

            if (ev.Code == InputEvent.RelX)
            {
                dx += ev.Value;
            }
            else if (ev.Code == InputEvent.RelY)
            {
                dy += ev.Value;
            }
        }

        return new MouseDelta(dx, dy);
    }
}
