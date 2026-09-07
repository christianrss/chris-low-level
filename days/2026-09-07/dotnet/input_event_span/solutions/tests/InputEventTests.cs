using System.Runtime.InteropServices;
using Chris.InputLab;
using Xunit;

namespace Chris.InputLab.Tests;

public class InputEventTests
{
    private static string FixturePath(string name)
    {
        return Path.Combine(AppContext.BaseDirectory, "fixtures", name);
    }

    private static byte[] LoadFixture(string name) => File.ReadAllBytes(FixturePath(name));

    // PEDAGOGY-TEST: DN-INPUT-LAYOUT-01
    [Fact]
    public void Caso1_InputEvent_HasExplicitSize24()
    {
        Assert.Equal(24, InputEvent.StructSize);
        Assert.Equal(24, Marshal.SizeOf<InputEvent>());
    }

    // PEDAGOGY-TEST: DN-INPUT-SPAN-02
    [Fact]
    public void Caso2_TryReadEvent_KeyAPress()
    {
        var raw = LoadFixture("key_a_press.bin");
        Assert.True(InputEventSpan.TryReadEvent(raw, 0, out var ev));
        Assert.Equal(InputEvent.EvKey, ev.Type);
        Assert.Equal(InputEvent.KeyA, ev.Code);
        Assert.Equal(1, ev.Value);
        Assert.Equal(1000, ev.TimeSec);
        Assert.Equal(500, ev.TimeUsec);
    }

    // PEDAGOGY-TEST: DN-INPUT-SPAN-02
    [Fact]
    public void Caso3_ReadAll_EventStream()
    {
        var raw = LoadFixture("event_stream.bin");
        Span<InputEvent> buf = stackalloc InputEvent[8];
        int n = InputEventSpan.ReadAll(raw, buf);
        Assert.Equal(3, n);
    }

    // PEDAGOGY-TEST: DN-INPUT-HID-03
    [Fact]
    public void Caso4_HidKeyboard_KeyA()
    {
        var raw = LoadFixture("key_a_press.bin");
        InputEventSpan.TryReadEvent(raw, 0, out var ev);
        Assert.True(HidKeyboardParser.TryParseKeyPress(ev, out var sc, out var act));
        Assert.Equal(InputEvent.KeyA, sc);
        Assert.Equal(KeyAction.Pressed, act);
    }

    // PEDAGOGY-TEST: DN-INPUT-PS2-04
    [Fact]
    public void Caso5_Ps2Mouse_RelativeDeltas()
    {
        var raw = LoadFixture("mouse_rel.bin");
        Span<InputEvent> buf = stackalloc InputEvent[4];
        int n = InputEventSpan.ReadAll(raw, buf);
        var delta = Ps2MouseParser.ParseRelativeMotion(buf[..n]);
        Assert.Equal(5, delta.Dx);
        Assert.Equal(-3, delta.Dy);
    }

    // PEDAGOGY-TEST: DN-INPUT-SPAN-02
    [Fact]
    public void Caso6_TryReadEvent_TruncatedRejected()
    {
        Assert.False(InputEventSpan.TryReadEvent(ReadOnlySpan<byte>.Empty, 0, out _));
        Assert.False(InputEventSpan.TryReadEvent(new byte[10], 0, out _));
    }
}
