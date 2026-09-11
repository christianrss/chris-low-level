// PEDAGOGY-SOLUTION: CAP-DN-HOST-01
// PEDAGOGY-SOLUTION: CAP-DN-HOST-02
// PEDAGOGY-SOLUTION: CAP-DN-HOST-03
namespace Chris.CapstoneInput;

public readonly record struct InputEvent(ushort Type, ushort Code, int Value);

public static class InputHost
{
    public const int EventSize = 24;

    /// PEDAGOGY-SOLUTION: CAP-DN-HOST-01
    public static bool TryParse(ReadOnlySpan<byte> buffer, out InputEvent ev)
    {
        ev = default;
        if (buffer.Length < EventSize) return false;
        ev = new InputEvent(
            BitConverter.ToUInt16(buffer.Slice(16, 2)),
            BitConverter.ToUInt16(buffer.Slice(18, 2)),
            BitConverter.ToInt32(buffer.Slice(20, 4)));
        return true;
    }

    /// PEDAGOGY-SOLUTION: CAP-DN-HOST-02
    public static int CountEvents(ReadOnlySpan<byte> buffer)
    {
        return buffer.Length / EventSize;
    }

    /// PEDAGOGY-SOLUTION: CAP-DN-HOST-03
    public static string Summarize(ReadOnlySpan<byte> buffer)
    {
        int n = CountEvents(buffer);
        return $"events={n}";
    }
}
