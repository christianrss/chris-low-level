using Chris.CapstoneInput;
using Xunit;

namespace Chris.CapstoneInput.Tests;

public class HostTests
{
    // PEDAGOGY-TEST: CAP-DN-HOST-01
    [Fact]
    public void Caso1_TryParse()
    {
        var buf = new byte[24];
        buf[16] = 1; buf[18] = 30; buf[20] = 1;
        Assert.True(InputHost.TryParse(buf, out var ev));
        Assert.Equal((ushort)1, ev.Type);
        Assert.Equal((ushort)30, ev.Code);
    }

    // PEDAGOGY-TEST: CAP-DN-HOST-02
    [Fact]
    public void Caso2_CountEvents()
    {
        Assert.Equal(2, InputHost.CountEvents(new byte[48]));
    }

    // PEDAGOGY-TEST: CAP-DN-HOST-03
    [Fact]
    public void Caso3_Summarize()
    {
        Assert.Equal("events=1", InputHost.Summarize(new byte[24]));
    }
}
