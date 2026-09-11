using Chris.PinnedLab;
using Xunit;
public class PinnedTests {
    [Fact]
    public void Sum() {
        // PEDAGOGY-TEST: D8-DN-PIN
        // PEDAGOGY-TEST: D8-DN-LEN
        // PEDAGOGY-TEST: D8-DN-SUM
        Assert.Equal(6, Pinned.SumPinned(new byte[]{1,2,3}));
    }
}
