namespace Chris.CapstoneInput;

public readonly record struct InputEvent(ushort Type, ushort Code, int Value);

public static class InputHost
{
    public const int EventSize = 24;

    /// TODO [CAP-DN-HOST-01]: parse one 24-byte evdev record
    public static bool TryParse(ReadOnlySpan<byte> buffer, out InputEvent ev)
    {
        ev = default;
        return false;
    }

    /// TODO [CAP-DN-HOST-02]: count complete events in buffer
    public static int CountEvents(ReadOnlySpan<byte> buffer)
    {
        return 0;
    }

    /// TODO [CAP-DN-HOST-03]: host pipeline summary string
    public static string Summarize(ReadOnlySpan<byte> buffer)
    {
        return string.Empty;
    }
}
